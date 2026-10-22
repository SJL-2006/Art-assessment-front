"""学生端 / 教师端 Mock 数据。

用纯 Python 字典组织，后端暂不落库；前端通过 /api/... 接口拉取。
"""
from datetime import date, timedelta


# ======================== 公共数据 ========================

# 侧边栏菜单（学生端 / 教师端） —— 按 Excel 功能模块归纳
STUDENT_SIDEBAR = [
    {
        "group": "班级",
        "items": [
            {"key": "class", "title": "我的班级", "path": "/student/class", "icon": "users"},
        ],
    },
    {
        "group": "测评练习",
        "items": [
            {"key": "music-practice", "title": "音乐测评练习", "path": "/student/practice/music", "icon": "music"},
            {"key": "art-practice", "title": "美术测评练习", "path": "/student/practice/art", "icon": "palette"},
        ],
    },
    {
        "group": "正式测评",
        "items": [
            {"key": "music-official", "title": "音乐正式测评", "path": "/student/official/music", "icon": "music-note"},
            {"key": "art-official", "title": "美术正式测评", "path": "/student/official/art", "icon": "brush"},
        ],
    },
    {
        "group": "测评结果",
        "items": [
            {"key": "results", "title": "测评记录", "path": "/student/results", "icon": "list"},
            {"key": "curve", "title": "成绩曲线", "path": "/student/curve", "icon": "trend"},
            {"key": "class-report", "title": "班级测评信息", "path": "/student/class-report", "icon": "users-chart"},
        ],
    },
    {
        "group": "证书",
        "items": [
            {"key": "certificate", "title": "我的证书", "path": "/student/certificate", "icon": "award"},
        ],
    },
    {
        "group": "个人",
        "items": [
            {"key": "profile", "title": "个人信息", "path": "/student/profile", "icon": "user"},
            {"key": "autonomy", "title": "课外自主学习", "path": "/student/autonomy", "icon": "book"},
        ],
    },
]

TEACHER_SIDEBAR = [
    {
        "group": "班级管理",
        "items": [
            {"key": "class", "title": "班级列表", "path": "/teacher/class", "icon": "users"},
            {"key": "class-create", "title": "创建班级", "path": "/teacher/class/create", "icon": "plus-circle"},
        ],
    },
    {
        "group": "学生管理",
        "items": [
            {"key": "students", "title": "学生列表", "path": "/teacher/students", "icon": "user"},
            {"key": "student-import", "title": "批量导入", "path": "/teacher/students/import", "icon": "upload"},
        ],
    },
    {
        "group": "试题",
        "items": [
            {"key": "questions", "title": "试题库", "path": "/teacher/questions", "icon": "file-text"},
        ],
    },
    {
        "group": "组卷",
        "items": [
            {"key": "papers", "title": "试卷列表", "path": "/teacher/papers", "icon": "layers"},
            {"key": "paper-create", "title": "手动组卷", "path": "/teacher/papers/create", "icon": "edit"},
            {"key": "paper-auto", "title": "自动组卷", "path": "/teacher/papers/auto", "icon": "shuffle"},
        ],
    },
    {
        "group": "测评发布",
        "items": [
            {"key": "music-publish", "title": "发布音乐测评", "path": "/teacher/publish/music", "icon": "music"},
            {"key": "art-publish", "title": "发布美术测评", "path": "/teacher/publish/art", "icon": "palette"},
        ],
    },
    {
        "group": "评分与证书",
        "items": [
            {"key": "score", "title": "学生评分", "path": "/teacher/score", "icon": "star"},
            {"key": "certificate", "title": "学生证书", "path": "/teacher/certificate", "icon": "award"},
        ],
    },
    {
        "group": "个人",
        "items": [
            {"key": "profile", "title": "个人信息", "path": "/teacher/profile", "icon": "user-circle"},
        ],
    },
]


# ======================== 学生端工作台 ========================

STUDENT_WORKSPACE = {
    "student": {"name": "李小明", "studentNo": "2024052101", "grade": "五年级", "className": "五(2)班"},
    "stats": [
        {"label": "已完成测评", "value": 8, "color": "#4f9cf9", "trend": "+2"},
        {"label": "练习次数", "value": 36, "color": "#a06ee8", "trend": "+8"},
        {"label": "平均得分", "value": 87.5, "color": "#2fbfa5", "trend": "+3.2"},
        {"label": "获得证书", "value": 2, "color": "#f2b23e", "trend": "+1"},
    ],
    "upcoming": [
        {"id": 1, "title": "音乐正式测评 · 第五单元", "subject": "music", "date": "2026-10-25 09:00", "duration": 40},
        {"id": 2, "title": "美术正式测评 · 色彩运用", "subject": "art", "date": "2026-10-28 14:30", "duration": 45},
    ],
    "recent": [
        {"id": 101, "title": "音乐测评练习 · 节奏训练", "subject": "music", "score": 92, "date": "2026-10-21"},
        {"id": 102, "title": "美术测评练习 · 水彩风景", "subject": "art", "score": 85, "date": "2026-10-20"},
        {"id": 103, "title": "音乐正式测评 · 第四单元", "subject": "music", "score": 88, "date": "2026-10-16"},
    ],
    "curve": [
        {"month": "03", "music": 78, "art": 75},
        {"month": "04", "music": 80, "art": 79},
        {"month": "05", "music": 82, "art": 83},
        {"month": "06", "music": 85, "art": 84},
        {"month": "07", "music": 86, "art": 86},
        {"month": "09", "music": 88, "art": 87},
        {"month": "10", "music": 90, "art": 89},
    ],
}


# ======================== 教师端工作台 ========================

TEACHER_WORKSPACE = {
    "teacher": {"name": "王美丽", "teacherNo": "T20230088", "subject": "美术 / 音乐", "school": "阳光小学"},
    "stats": [
        {"label": "管理班级", "value": 3, "color": "#4f9cf9"},
        {"label": "学生人数", "value": 142, "color": "#a06ee8"},
        {"label": "已发布测评", "value": 12, "color": "#2fbfa5"},
        {"label": "待批改材料", "value": 7, "color": "#f2709c"},
    ],
    "myClasses": [
        {"id": "C001", "name": "五(1)班", "studentCount": 45, "headteacher": "张丽"},
        {"id": "C002", "name": "五(2)班", "studentCount": 47, "headteacher": "王美丽"},
        {"id": "C003", "name": "六(1)班", "studentCount": 50, "headteacher": "刘芳"},
    ],
    "recentPapers": [
        {"id": 1001, "title": "音乐·节奏与旋律 测评卷", "subject": "music", "class": "五(2)班", "publishDate": "2026-10-18", "respondents": 45},
        {"id": 1002, "title": "美术·色彩表达 测评卷", "subject": "art", "class": "五(1)班", "publishDate": "2026-10-15", "respondents": 42},
        {"id": 1003, "title": "音乐·中国民族乐器 测评卷", "subject": "music", "class": "六(1)班", "publishDate": "2026-10-10", "respondents": 48},
    ],
    "auditQueue": [
        {"id": 201, "student": "张小华", "className": "五(2)班", "reason": "申请更换班级", "date": "2026-10-21"},
        {"id": 202, "student": "陈美丽", "className": "五(2)班", "reason": "科任教师加入申请", "date": "2026-10-20"},
    ],
}


# ======================== 登录接口 ========================

# 纯 mock：按角色返回不同 token + 用户信息
USERS = {
    "student": {
        "name": "李小明", "role": "student", "token": "mock-student-token",
        "avatar": "Li",
    },
    "teacher": {
        "name": "王美丽", "role": "teacher", "token": "mock-teacher-token",
        "avatar": "Wa",
    },
    "provincial": {
        "name": "赵省管", "role": "provincial", "token": "mock-provincial-token",
        "avatar": "Zh",
    },
    "questionbank": {
        "name": "钱题库", "role": "questionbank", "token": "mock-questionbank-token",
        "avatar": "Qi",
    },
    "school": {
        "name": "王海燕", "role": "school", "token": "mock-school-token",
        "avatar": "Wa",
    },
    "district": {
        "name": "李建国", "role": "district", "token": "mock-district-token",
        "avatar": "Li",
    },
    "city": {
        "name": "何文博", "role": "city", "token": "mock-city-token",
        "avatar": "He",
    },
}


# ======================== 班级详情（学生） ========================

STUDENT_CLASS_DETAIL = {
    "classNo": "2024052",
    "className": "五(2)班",
    "grade": "五年级",
    "headteacher": {"name": "王美丽", "phone": "138****1234"},
    "studentCount": 47,
    "mySeat": 12,
    "tip": "加入班级后请及时完成班主任发布的正式测评，测评记录将计入学期艺术素质档案。",
}


# ======================== 练习 / 试卷 Mock ========================

def _make_paper(subject, kind):
    title_map = {
        ("music", "practice"): "音乐测评练习 · 节奏训练",
        ("music", "official"): "音乐正式测评 · 第五单元",
        ("art", "practice"): "美术测评练习 · 色彩基础",
        ("art", "official"): "美术正式测评 · 色彩运用",
    }
    return {
        "id": f"{subject}-{kind}-01",
        "title": title_map.get((subject, kind), "试卷"),
        "duration": 40 if subject == "music" else 45,
        "totalScore": 100,
        "questionCount": 12 if subject == "music" else 8,
        "questions": [
            {"id": 1, "type": "single", "text": "以下哪种属于五声音阶？", "options": ["宫商角徵羽", "do re mi fa", "1 2 3 4", "以上都对"], "answer": 0},
            {"id": 2, "type": "single", "text": "在 C 大调中，sol 对应的唱名是？", "options": ["3", "4", "5", "6"], "answer": 2},
        ],
    }


# ======================== 省级管理员端 ========================

PROVINCIAL_STATS = {
    "cities": 14,
    "districts": 125,
    "students": 312480,
    "exams": 48,
    "cityRate": [
        {"name": "成都市", "rate": 96, "color": "#4f9cf9"},
        {"name": "绵阳市", "rate": 88, "color": "#a06ee8"},
        {"name": "德阳市", "rate": 82, "color": "#2fbfa5"},
        {"name": "乐山市", "rate": 78, "color": "#f2709c"},
        {"name": "宜宾市", "rate": 74, "color": "#f2b23e"},
        {"name": "自贡市", "rate": 69, "color": "#8b7cf6"},
        {"name": "广元市", "rate": 62, "color": "#2fbfa5"},
        {"name": "其他市州", "rate": 58, "color": "#4f9cf9"},
    ],
    "subjectDist": [
        {"name": "音乐", "value": 22, "color": "#a06ee8"},
        {"name": "美术", "value": 20, "color": "#2fbfa5"},
        {"name": "综合艺术", "value": 6, "color": "#f2709c"},
    ],
}

PROVINCIAL_PAPERS = [
    {"id": "P2026001", "title": "2026秋季省级音乐统一测评（七年级）", "subject": "音乐", "scope": "全省", "questionCount": 40, "totalScore": 100, "status": "已发布", "creator": "省教研室", "createdAt": "2026-10-12"},
    {"id": "P2026002", "title": "2026秋季省级美术统一测评（八年级）", "subject": "美术", "scope": "全省", "questionCount": 35, "totalScore": 100, "status": "已发布", "creator": "省教研室", "createdAt": "2026-10-08"},
    {"id": "P2026003", "title": "2027春季省级音乐测评（九年级）", "subject": "音乐", "scope": "全省", "questionCount": 45, "totalScore": 100, "status": "草稿", "creator": "省教研室", "createdAt": "2026-10-20"},
]

PROVINCIAL_EXAM_STATS = {
    "summary": {"published": 48, "finished": 41, "averageScore": 82.6, "passRate": 91.3},
    "byGrade": [
        {"grade": "七年级", "count": 18, "avg": 84.2, "passRate": 93.1},
        {"grade": "八年级", "count": 16, "avg": 81.7, "passRate": 90.5},
        {"grade": "九年级", "count": 14, "avg": 80.9, "passRate": 89.8},
    ],
}

PROVINCIAL_ACCOUNTS = {
    "student": [
        {"id": "S20260001", "name": "李小明", "studentNo": "2024052101", "school": "阳光小学", "grade": "五年级", "status": "正常"},
        {"id": "S20260002", "name": "张小华", "studentNo": "2024052102", "school": "阳光小学", "grade": "五年级", "status": "正常"},
    ],
    "school": [
        {"id": "SCH001", "name": "阳光小学", "district": "朝阳区", "city": "成都市", "students": 1280, "status": "正常"},
        {"id": "SCH002", "name": "育才中学", "district": "武侯区", "city": "成都市", "students": 2140, "status": "正常"},
    ],
    "district": [
        {"id": "D001", "name": "朝阳区", "city": "成都市", "schools": 32, "status": "正常"},
        {"id": "D002", "name": "武侯区", "city": "成都市", "schools": 28, "status": "正常"},
    ],
    "city": [
        {"id": "C001", "name": "成都市", "districts": 20, "schools": 486, "status": "正常"},
        {"id": "C002", "name": "绵阳市", "districts": 9, "schools": 214, "status": "正常"},
    ],
}

PROVINCIAL_EXPORT_RATE = [
    {"city": "成都市", "students": 98600, "joined": 94656, "rate": 96.0},
    {"city": "绵阳市", "students": 42300, "joined": 37224, "rate": 88.0},
    {"city": "德阳市", "students": 28100, "joined": 23042, "rate": 82.0},
    {"city": "乐山市", "students": 25400, "joined": 19812, "rate": 78.0},
]

PROVINCIAL_LOGS = [
    {"id": 1, "time": "2026-10-21 14:32", "user": "省管理员", "action": "发布测评", "target": "2026秋季省级音乐统一测评（七年级）", "ip": "10.12.3.45"},
    {"id": 2, "time": "2026-10-20 09:18", "user": "省管理员", "action": "新建试卷", "target": "2027春季省级音乐测评（九年级）", "ip": "10.12.3.45"},
    {"id": 3, "time": "2026-10-19 16:04", "user": "题库管理员", "action": "审核通过", "target": "Q5862 打击乐器选择题", "ip": "10.12.7.18"},
]


# ======================== 题库管理端 ========================

QB_STATS = {
    "total": 5862,
    "approved": 5418,
    "pending": 148,
    "rejected": 36,
    "bySubject": [
        {"name": "音乐", "value": 3120, "color": "#a06ee8"},
        {"name": "美术", "value": 2380, "color": "#2fbfa5"},
        {"name": "综合艺术", "value": 362, "color": "#f2709c"},
    ],
    "byType": [
        {"name": "选择题", "value": 2450},
        {"name": "判断题", "value": 1680},
        {"name": "填空题", "value": 940},
        {"name": "简答题", "value": 612},
        {"name": "创作题", "value": 180},
    ],
}

QB_QUESTIONS = [
    {"id": "Q5862", "subject": "音乐", "type": "选择题", "question": "以下哪件乐器属于打击乐器？A.小提琴 B.钢琴 C.架子鼓 D.长笛", "difficulty": "易", "grade": "七年级", "score": 2, "chapter": "第一单元·乐器家族", "creator": "张老师", "useCount": 36, "auditStatus": "通过"},
    {"id": "Q5861", "subject": "美术", "type": "判断题", "question": "中国画中的“四君子”指的是梅、兰、竹、菊。", "difficulty": "易", "grade": "八年级", "score": 2, "chapter": "第二单元·中国画欣赏", "creator": "李老师", "useCount": 28, "auditStatus": "通过"},
    {"id": "Q5860", "subject": "音乐", "type": "选择题", "question": "贝多芬的《命运交响曲》是第几交响曲？A.第三 B.第五 C.第六 D.第九", "difficulty": "中", "grade": "九年级", "score": 3, "chapter": "第三单元·交响音乐", "creator": "王老师", "useCount": 42, "auditStatus": "通过"},
    {"id": "Q5859", "subject": "美术", "type": "填空题", "question": "文艺复兴时期最著名的艺术家之一______创作了《蒙娜丽莎》。", "difficulty": "易", "grade": "七年级", "score": 3, "chapter": "第一单元·西方绘画", "creator": "陈老师", "useCount": 20, "auditStatus": "通过"},
    {"id": "Q5858", "subject": "音乐", "type": "简答题", "question": "请简述中国传统音乐与西方古典音乐在节奏上的主要差异。", "difficulty": "难", "grade": "九年级", "score": 10, "chapter": "第五单元·中外音乐比较", "creator": "赵老师", "useCount": 8, "auditStatus": "通过"},
    {"id": "Q5857", "subject": "美术", "type": "创作题", "question": "请以“春天”为主题，创作一幅水彩画，要求构图均衡、色彩和谐。", "difficulty": "难", "grade": "八年级", "score": 15, "chapter": "第四单元·水彩画创作", "creator": "孙老师", "useCount": 12, "auditStatus": "通过"},
    {"id": "Q5856", "subject": "音乐", "type": "判断题", "question": "五线谱中，高音谱号也叫 G 谱号。", "difficulty": "易", "grade": "七年级", "score": 2, "chapter": "第一单元·记谱法", "creator": "张老师", "useCount": 32, "auditStatus": "待审核"},
    {"id": "Q5855", "subject": "美术", "type": "选择题", "question": "以下哪种色彩搭配属于互补色？A.红与橙 B.蓝与橙 C.黄与绿 D.蓝与紫", "difficulty": "中", "grade": "七年级", "score": 2, "chapter": "第二单元·色彩知识", "creator": "李老师", "useCount": 18, "auditStatus": "待审核"},
]

QB_AUDIT = [
    {"id": "Q5863", "subject": "音乐", "type": "选择题", "question": "《二泉映月》的演奏乐器是？A.二胡 B.琵琶 C.古筝 D.笛子", "creator": "张老师", "submittedAt": "2026-10-21 10:22", "status": "待审核"},
    {"id": "Q5864", "subject": "美术", "type": "创作题", "question": "以“校园一角”为题创作一幅速写，要求线条流畅、透视准确。", "creator": "孙老师", "submittedAt": "2026-10-20 15:40", "status": "待审核"},
    {"id": "Q5865", "subject": "音乐", "type": "判断题", "question": "京剧中的“生”行当指男性角色。", "creator": "王老师", "submittedAt": "2026-10-20 09:12", "status": "已驳回"},
]

QB_RESOURCES = [
    {"id": "R001", "name": "架子鼓示例音频.mp3", "type": "音频", "size": "1.8 MB", "questions": 12, "uploader": "张老师", "uploadedAt": "2026-10-12"},
    {"id": "R002", "name": "中国画四君子.jpg", "type": "图片", "size": "860 KB", "questions": 8, "uploader": "李老师", "uploadedAt": "2026-10-10"},
    {"id": "R003", "name": "命运交响曲选段.mp3", "type": "音频", "size": "4.2 MB", "questions": 16, "uploader": "王老师", "uploadedAt": "2026-10-08"},
]

QB_COURSES = [
    {"id": "CO01", "name": "初中音乐（人教版）", "subject": "音乐", "grade": "七-九年级", "chapters": 8, "questions": 1280, "status": "启用"},
    {"id": "CO02", "name": "初中美术（人教版）", "subject": "美术", "grade": "七-九年级", "chapters": 7, "questions": 960, "status": "启用"},
    {"id": "CO03", "name": "小学艺术（综合）", "subject": "综合艺术", "grade": "三-六年级", "chapters": 6, "questions": 362, "status": "停用"},
]

QB_CHAPTERS = [
    {"id": "CH01", "course": "初中音乐（人教版）", "name": "第一单元 音乐的魅力", "questions": 168, "order": 1},
    {"id": "CH02", "course": "初中音乐（人教版）", "name": "第二单元 民族音乐", "questions": 142, "order": 2},
    {"id": "CH03", "course": "初中美术（人教版）", "name": "第一单元 西方绘画", "questions": 156, "order": 1},
]

QB_LOGS = [
    {"id": 1, "time": "2026-10-21 10:22", "user": "张老师", "action": "新建试题", "target": "Q5863 二胡选择题", "ip": "10.12.8.66"},
    {"id": 2, "time": "2026-10-20 16:10", "user": "题库管理员", "action": "审核通过", "target": "Q5862 打击乐器选择题", "ip": "10.12.7.18"},
    {"id": 3, "time": "2026-10-20 09:12", "user": "题库管理员", "action": "驳回试题", "target": "Q5865 京剧行当判断题", "ip": "10.12.7.18"},
]
