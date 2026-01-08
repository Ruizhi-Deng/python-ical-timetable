import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from hashlib import md5
from typing import Any, List


def EvenWeeks(start: int, end: int) -> list[int]:
    """
    返回偶数周列表
    如 even_week(1, 4) -> [2, 4]
    """
    return [i for i in range(start, end + 1) if not i % 2]


def OddWeeks(start: int, end: int) -> list[int]:
    """
    返回奇数周列表：
    如 odd_week(1, 4) -> [1, 3]
    """
    return [i for i in range(start, end + 1) if i % 2]


def Weeks(start: int, end: int) -> list[int]:
    """
    返回周数列表：
    如 week(1, 3) -> [1, 2, 3]
    """
    return list(range(start, end + 1))


# def WeekDays(start: int, end: int) -> list[int]:
#     """
#     返回每天列表：
#     如 week(1, 3) -> [1, 2, 3]
#     """
#     return list(range(start, end + 1))


@dataclass
class Course:
    # code: str
    name: str
    teacher: str
    classroom: str
    location: Any
    weekday: int | list[int] | None = None  # 周几，可以是单个数字或列表（两种方式通用）
    # 方式一：使用周数和课节
    weeks: list[int] | None = None
    indexes: list[int] | None = None
    # 方式二：使用具体日期和时间
    start_date: tuple[int, int, int] | None = None  # (year, month, day)
    end_date: tuple[int, int, int] | None = None  # (year, month, day)
    start_time: tuple[int, int] | None = None  # (hour, minute)
    end_time: tuple[int, int] | None = None  # (hour, minute)
    details: str = ""

    def title(self) -> str:
        """
        每一次课程日历项的标题
        """
        return f"{self.name}"

    def description(self) -> str:
        """
        每一次课程日历项目的介绍信息
        """
        return f"Lecturer: {self.teacher}\\n{self.details}"


@dataclass
class School:
    duration: int
    timetable: List[tuple[int, int]]
    start: tuple[int, int, int]
    courses: List[Course]

    # In US
    HEADERS = [
        "BEGIN:VCALENDAR",
        "METHOD:PUBLISH",
        "VERSION:2.0",
        "X-WR-CALNAME:TIMETABLE",
        "X-WR-TIMEZONE:America/Detroit",
        "CALSCALE:GREGORIAN",
        "BEGIN:VTIMEZONE",
        "TZID:America/Detroit",
        "X-LIC-LOCATION:America/Detroit",
        "END:VTIMEZONE",
    ]
    FOOTERS = ["END:VCALENDAR"]

    def __post_init__(self) -> None:
        assert self.courses, "请填写课程列表"
        # 两种方式都支持，初始化可选参数
        if self.timetable:
            self.timetable.insert(0, (0, 0))
        if self.start:
            assert len(self.start) >= 3, "请设置开学第一周日期"
            self.start_dt = datetime(*self.start[:3])
            self.start_dt -= timedelta(days=self.start_dt.weekday())  # 让日期回到周一
        else:
            self.start_dt = None

    def time(self, week: int, weekday: int, index: int, plus: bool = False) -> datetime:
        """
        Calculates the datetime for a specific class session based on the week, weekday, and timetable index.
        此方法保留用于向后兼容，新方法应使用 Course 中的日期和时间。

        Args:
            week (int): The week number (1-based).
            weekday (int): The day of the week (1-based, e.g., 1 for Monday).
            index (int): The index in the timetable indicating the class period.
            plus (bool, optional): If True, adds the class duration to the start time. Defaults to False.

        Returns:
            datetime: The calculated datetime for the class session.
        """
        if not self.start_dt or not self.timetable:
            raise ValueError("使用旧的时间计算方式需要设置 start 和 timetable")
        date = self.start_dt + timedelta(weeks=week - 1, days=weekday - 1)
        dt = date.replace(
            hour=self.timetable[index][0], minute=self.timetable[index][1]
        )
        return dt + timedelta(minutes=self.duration if plus else 0)

    def generate(self) -> str:
        runtime = datetime.now()
        lines: List[str] = []
        # Prepare common headers
        lines.extend(self.HEADERS)

        for course in self.courses:
            # Normalize location
            if not course.location:
                loc_lines = [f"LOCATION:{course.classroom}"]
            elif isinstance(course.location, str):  
                # add \ before commas for ical format
                loc_lines = [
                    f"LOCATION:{(course.classroom + ", " + course.location).replace(',', r'\,')}"
                ]
            elif hasattr(course.location, "result"):
                loc_lines = course.location.result()
            else:
                loc_lines = []

            # 判断使用哪种方式（方式一：周数+课节 vs 方式二：日期+时间）
            if course.start_date and course.start_time and course.end_time:
                # 方式二：具体日期和时间
                start_date = datetime(*course.start_date)
                start_time = datetime.combine(start_date.date(), datetime.min.time()).replace(
                    hour=course.start_time[0], minute=course.start_time[1]
                )
                end_time = datetime.combine(start_date.date(), datetime.min.time()).replace(
                    hour=course.end_time[0], minute=course.end_time[1]
                )
                dtstart = start_time
                dtend = end_time

                # 计算重复规则
                if course.end_date and course.weekday:
                    end_date = datetime(*course.end_date)
                    day_map = {1: "MO", 2: "TU", 3: "WE", 4: "TH", 5: "FR", 6: "SA", 7: "SU"}
                    weekdays = course.weekday if isinstance(course.weekday, list) else [course.weekday]
                    byday = ",".join([day_map.get(d, "MO") for d in sorted(weekdays)])
                    rrule = f"FREQ=WEEKLY;BYDAY={byday};UNTIL={end_date:%Y%m%d}"
                elif course.weekday:
                    day_map = {1: "MO", 2: "TU", 3: "WE", 4: "TH", 5: "FR", 6: "SA", 7: "SU"}
                    weekdays = course.weekday if isinstance(course.weekday, list) else [course.weekday]
                    byday = ",".join([day_map.get(d, "MO") for d in sorted(weekdays)])
                    end_date = start_date + timedelta(days=365)
                    rrule = f"FREQ=WEEKLY;BYDAY={byday};UNTIL={end_date:%Y%m%d}"
                else:
                    rrule = None

                uid_input = f"{course.title()}-{course.classroom}-{course.start_date}-{course.start_time}"
                uid = md5(uid_input.encode()).hexdigest()

                # Build VEVENT
                vevent = [
                    "BEGIN:VEVENT",
                    f"SUMMARY:{course.title()}",
                    f"DESCRIPTION:{course.description()}",
                    f"DTSTART;TZID=America/Detroit:{dtstart:%Y%m%dT%H%M%S}",
                    f"DTEND;TZID=America/Detroit:{dtend:%Y%m%dT%H%M%S}",
                ]
                
                if rrule:
                    vevent.append(f"RRULE:{rrule}")
                
                vevent.extend([
                    f"DTSTAMP:{runtime:%Y%m%dT%H%M%SZ}",
                    f"UID:{uid}",
                    *loc_lines,
                    "END:VEVENT",
                ])
                
                # Fold lines at 75 chars as per RFC2445
                for line in vevent:
                    first = True
                    while line:
                        prefix = "" if first else " "
                        lines.append(prefix + line[:72])
                        line = line[72:]
                        first = False

            elif course.weekday is not None and course.weeks and course.indexes:
                # 方式一：周数 + 课节
                if not self.start_dt or not self.timetable:
                    raise ValueError("使用方式一（周数+课节）需要设置 start 和 timetable")
                
                # 处理 weekday 可以是单个值或列表
                weekdays = course.weekday if isinstance(course.weekday, list) else [course.weekday]
                
                for wd in weekdays:
                    weeks = sorted(course.weeks)
                    first_week = weeks[0]
                    count = len(weeks)
                    diffs = [weeks[i] - weeks[i - 1] for i in range(1, len(weeks))]
                    interval = diffs[0] if diffs and all(d == diffs[0] for d in diffs) else 1
                    day_map = {1: "MO", 2: "TU", 3: "WE", 4: "TH", 5: "FR", 6: "SA", 7: "SU"}
                    byday = day_map.get(wd, "MO")
                    
                    rrule_parts = [f"FREQ=WEEKLY", f"BYDAY={byday}"]
                    if interval > 1:
                        rrule_parts.append(f"INTERVAL={interval}")
                    rrule_parts.append(f"COUNT={count}")
                    rrule = ";".join(rrule_parts)

                    dtstart = self.time(first_week, wd, course.indexes[0])
                    dtend = self.time(first_week, wd, course.indexes[-1], True)

                    uid_input = (
                        f"{course.title()}-{first_week}-{wd}-{course.indexes[0]}"
                    )
                    uid = md5(uid_input.encode()).hexdigest()
                    
                    # Build VEVENT
                    vevent = [
                        "BEGIN:VEVENT",
                        f"SUMMARY:{course.title()}",
                        f"DESCRIPTION:{course.description()}",
                        f"DTSTART;TZID=America/Detroit:{dtstart:%Y%m%dT%H%M%S}",
                        f"DTEND;TZID=America/Detroit:{dtend:%Y%m%dT%H%M%S}",
                        f"RRULE:{rrule}",
                        f"DTSTAMP:{runtime:%Y%m%dT%H%M%SZ}",
                        f"UID:{uid}",
                        *loc_lines,
                        "END:VEVENT",
                    ]
                    
                    # Fold lines at 75 chars as per RFC2445
                    for line in vevent:
                        first = True
                        while line:
                            prefix = "" if first else " "
                            lines.append(prefix + line[:72])
                            line = line[72:]
                            first = False
            else:
                raise ValueError(
                    f"课程 '{course.name}' 定义不完整。需要使用以下方式之一:\n"
                    "方式一：weekday, weeks, indexes\n"
                    "方式二：start_date, start_time, end_time"
                )

        # Append footer
        lines.extend(self.FOOTERS)
        return "\n".join(lines)


@dataclass
class Geo:
    """
    仅提供坐标和地点名称的地点信息：
    name: 地点名称，lat：纬度，lon：经度
    """

    name: str
    lat: float | str
    lon: float | str

    @property
    def geo(self) -> str:
        return f"GEO:{self.lat};{self.lon}"

    def result(self) -> list[str]:
        return [f"LOCATION:{self.name}", self.geo]


class AppleMaps:
    """
    Apple Maps 地点信息：
    传入预先准备好的 ics 文件地址，自动分析
    """

    KEYS = ["SUMMARY", "LOCATION", "X-APPLE-STRUCTURED-LOCATION"]

    def __init__(self, calendar: str) -> None:
        self.locations: dict[str, dict[str, str]] = {}
        with open(calendar, encoding="utf-8") as r:
            c = r.read()
        for i in re.findall(r"(?<=BEGIN:VEVENT)[\s\S]*?(?=END:VEVENT)", c):
            self.generate(i)

    def generate(self, event: str) -> None:
        lines = event.split("\n")
        for i, e in enumerate(lines):
            if not e.startswith(" "):
                continue
            d = i - 1
            while not lines[d]:
                d -= 1
            lines[d] += e.removeprefix(" ")
            lines[i] = ""
        data = {k: next((i for i in lines if i.startswith(k)), "") for k in self.KEYS}
        if not all(data.values()):
            return
        title = data.pop("SUMMARY").removeprefix("SUMMARY:").strip()
        geo = re.findall(r"geo:([\d.]+),([\d.]+)", data["X-APPLE-STRUCTURED-LOCATION"])
        if geo:
            data["GEO"] = Geo(title, geo[0][0], geo[0][1]).geo
        self.locations[title] = data

    def __getitem__(self, key: str) -> list[str]:
        try:
            return list(self.locations[key].values())
        except KeyError:
            ke = KeyError(f"没有找到 {key!r} 的 Apple Maps 信息")
            try:
                ke.add_note(f"已在日历文件中记录的地点有: {', '.join(self.locations)}")
            except AttributeError:
                pass
            raise ke from None
