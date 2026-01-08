from data import AppleMaps, Course, EvenWeeks, Geo, OddWeeks, School, Weeks

# 定位信息的设置请参考 README.md
# 品学楼地图 = AppleMaps("UESTC.ics")
AH = "Angell Hall, 435 S State St, Ann Arbor, MI 48109, United States"
CHRYS = "Chrysler Center, 2121 Bonisteel Blvd, Ann Arbor, MI 48109, United States"
DOW = "Dow Building, 2301 Bonisteel Blvd, Ann Arbor, MI 48109, United States"
EECS = "Electrical & Computer Engineering Building, 1301 Beal Ave, Ann Arbor, MI 48109, United States"
EH = "East Hall, 530 Church St, Ann Arbor, MI 48109, United States"
FMCRB = "Robotics Building, 2505 Hayward St, Ann Arbor, MI 48109, United States"
FXB = "Francois-Xavier Bagnoud Building, 1320 Beal Ave, Ann Arbor, MI 48109, United States"
GGBL = "G.G. Brown Building, 2350 Hayward St, Ann Arbor, MI 48109, United States"
LCSIB = "Leinweber Computer Science and Information Building, 2200 Hayward St, Ann Arbor, MI 48109, United States"
# 立人楼B = Geo("电子科技大学清水河校区立人楼B区", 30.748903, 103.931567)

school = School(
    duration=30,  # 每节课时间为 30 分钟
    timetable=[
        (8, 00),
        (8, 30),
        (9, 00),
        (9, 30),
        (10, 00),
        (10, 30),
        (11, 00),
        (11, 30),
        (12, 00),
        (12, 30),
        (13, 00),
        (13, 30),
        (14, 00),
        (14, 30),
        (15, 00),
        (15, 30),
        (16, 00),
        (16, 30),
        (17, 00),
        (17, 30),
    ],
    start=(2026, 1, 5),  # 开学第一周当周周一至周日以内的任意日期
    courses=[
        Course(
            "ASTRO 127 Naked Eye Astronomy",
            "Major Stevens",
            "AH 3118",
            AH,
            weekday=[2, 4],
            start_date=(2026, 3, 9),
            end_date=(2026, 4, 21),
            start_time=(11, 0),
            end_time=(12, 0),
        ),
        Course(
            "EECS 373 Intro Embed Sys Des [LEC]",
            "Junyi Zhu",
            "LCSIB 1355",
            LCSIB,
            weekday=[2, 4],
            start_date=(2026, 1, 7),
            end_date=(2026, 4, 21),
            start_time=(15, 0),
            end_time=(16, 30),
        ),
        Course(
            "EECS 373 Intro Embed Sys Des [LAB]",
            "",
            "EECS 2334",
            EECS,
            weekday=3,
            start_date=(2026, 1, 7),
            end_date=(2026, 4, 21),
            start_time=(15, 0),
            end_time=(18, 0),
        ),
        Course(
            "EECS 445 Intro Machine Learn [LEC]",
            "Sindhu Kutty",
            "CHRYS 220",
            CHRYS,
            weekday=[2, 4],
            start_date=(2026, 1, 7),
            end_date=(2026, 4, 21),
            start_time=(12, 0),
            end_time=(13, 30),
        ),
        Course(
            "EECS 445 Intro Machine Learn [DIS]",
            "",
            "DOW 1017",
            DOW,
            weekday=[5],
            start_date=(2026, 1, 7),
            end_date=(2026, 4, 21),
            start_time=(10, 30),
            end_time=(11, 30),
        ),
        Course(
            "EECS 461 Embedded Control [LEC]",
            "Jeffrey Cook",
            "EECS 1500",
            EECS,
            weekday=[2, 4],
            start_date=(2026, 1, 7),
            end_date=(2026, 4, 21),
            start_time=(9, 00),
            end_time=(10, 30),
        ),
        Course(
            "EECS 461 Embedded Control [LAB]",
            "Sean Pasek",
            "EECS 4342",
            EECS,
            weekday=[1],
            start_date=(2026, 1, 7),
            end_date=(2026, 4, 21),
            start_time=(15, 00),
            end_time=(18, 00),
        ),
        Course(
            "EECS 568 Mobile Robotics",
            "Maani Ghaffari, Chankyo Kim, Tsimafei Lazouski",
            "FXB 1109",
            FXB,
            weekday=[1, 3],
            start_date=(2026, 1, 7),
            end_date=(2026, 4, 21),
            start_time=(13, 30),
            end_time=(15, 00),
        ),
        Course(
            "EECS 568 Mobile Robotics",
            "Maani Ghaffari, Chankyo Kim, Tsimafei Lazouski",
            "FMCRB 1060",
            FMCRB,
            weekday=[5],
            start_date=(2026, 1, 7),
            end_date=(2026, 4, 21),
            start_time=(13, 30),
            end_time=(14, 30),
        ),
    ],
)

with open("Timetable.ics", "w", encoding="utf-8") as w:
    w.write(school.generate())
