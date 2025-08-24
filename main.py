from data import AppleMaps, Course, EvenWeeks, Geo, OddWeeks, School, Weeks

# 定位信息的设置请参考 README.md
# 品学楼地图 = AppleMaps("UESTC.ics")
CHRYS = "Chrysler Center, 2121 Bonisteel Blvd, Ann Arbor, MI 48109, USA"
DOW = "Dow Building, 2301 Bonisteel Blvd, Ann Arbor, MI 48109, USA"
EH = "East Hall, 530 Church St, Ann Arbor, MI 48109, USA"
FXB = "Francois-Xavier Bagnoud Building, 1320 Beal Ave, Ann Arbor, MI 48109, USA"
GGBL = "G.G. Brown Building, 2350 Hayward St, Ann Arbor, MI 48109, USA"
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
    start=(2025, 8, 25),  # 开学第一周当周周一至周日以内的任意日期
    courses=[
        *[
            Course(
                "EECS 281 Data Structures and Algorithms [LEC]",
                "Marcus Darden, David Paoletti, Hector Garcia-Ramirez",
                "CHRYS 220",
                CHRYS,
                weekday,
                Weeks(1, 16),
                [6, 7, 8],
            )
            for weekday in (2, 4)
        ],
        *[
            Course(
                "EECS 281 Data Structures and Algorithms [LAB]",
                "",
                "DOW 3150",
                DOW,
                5,
                Weeks(1, 16),
                [i for i in range(16, 20)],
            )
        ],
        *[
            Course(
                "EECS 370 Intro Computer Org [LEC]",
                "Yatin Manerkar",
                "CHRYS 220",
                CHRYS,
                weekday,
                Weeks(1, 16),
                [15, 16, 17],
            )
            for weekday in (2, 4)
        ],
        *[
            Course(
                "EECS 370 Intro Computer Org [LAB]",
                "",
                "FXB 1008",
                FXB,
                1,
                Weeks(1, 16),
                [2, 3, 4, 5],
            ),
        ],
        *[
            Course(
                "MECHENG 235 Thermodynamics I",
                "Angela Violi",
                "GGBL 1571",
                GGBL,
                weekday,
                Weeks(1, 16),
                [12, 13, 14],
            )
            for weekday in (2, 4)
        ],
        *[
            Course(
                "MECHENG 360 Dynamic Sys",
                "Uduak Inyang-Udoh",
                "CHRYS133",
                CHRYS,
                weekday,
                Weeks(1, 16),
                [2, 3, 4, 5],
            )
            for weekday in (2, 4)
        ],
        *[
            Course(
                "STATS 425 Intro Probability",
                "Reynold Fregoli",
                "EH 1068",
                EH,
                weekday,
                Weeks(1, 16),
                [13, 14],
            )
            for weekday in (1, 3, 5)
        ]
    ]
)

with open("Timetable.ics", "w", encoding="utf-8") as w:
    w.write(school.generate())
