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
    weekday: int
    weeks: list[int]
    indexes: list[int]
    details: str = ""

    def title(self) -> str:
        """
        每一次课程日历项的标题：
        如希望传递「当前是第几周」这样的参数，可在这里预留格式化变量，并在 School.generate() 函数中修改
        """
        return f"{self.name}"
        # return f"{self.code} - {self.name}"

    def description(self) -> str:
        """
        每一次课程日历项目的介绍信息：
        如希望传递「当前是第几周」这样的参数，可在这里预留格式化变量，并在 School.generate() 函数中修改
        """
        return f"教师：{self.teacher}\\n{self.details}"


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
        assert self.timetable, "请设置课程对应时间"
        assert len(self.start) >= 3, "请设置开学第一周日期"
        assert self.courses, "请填写课程列表"
        self.timetable.insert(0, (0, 0))
        self.start_dt = datetime(*self.start[:3])
        self.start_dt -= timedelta(days=self.start_dt.weekday())  # 让日期回到周一

    def time(self, week: int, weekday: int, index: int, plus: bool = False) -> datetime:
        """
        Calculates the datetime for a specific class session based on the week, weekday, and timetable index.

        Args:
            week (int): The week number (1-based).
            weekday (int): The day of the week (1-based, e.g., 1 for Monday).
            index (int): The index in the timetable indicating the class period.
            plus (bool, optional): If True, adds the class duration to the start time. Defaults to False.

        Returns:
            datetime: The calculated datetime for the class session.
        """
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

            # Sort weeks and compute recurrence
            weeks = sorted(course.weeks)
            first_week = weeks[0]
            # last_week = weeks[-1]
            count = len(weeks)
            # Determine interval
            diffs = [weeks[i] - weeks[i - 1] for i in range(1, len(weeks))]
            interval = diffs[0] if diffs and all(d == diffs[0] for d in diffs) else 1
            # Map weekday
            day_map = {1: "MO", 2: "TU", 3: "WE", 4: "TH", 5: "FR", 6: "SA", 7: "SU"}
            byday = day_map.get(course.weekday, "MO")
            # Build RRULE
            rrule_parts = [f"FREQ=WEEKLY", f"BYDAY={byday}"]
            if interval > 1:
                rrule_parts.append(f"INTERVAL={interval}")
            rrule_parts.append(f"COUNT={count}")
            rrule = ";".join(rrule_parts)

            # DTSTART and DTEND based on first occurrence
            dtstart = self.time(first_week, course.weekday, course.indexes[0])
            dtend = self.time(first_week, course.weekday, course.indexes[-1], True)

            # UID per course
            uid_input = (
                f"{course.title()}-{first_week}-{course.weekday}-{course.indexes[0]}"
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
