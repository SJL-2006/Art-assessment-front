"""向数据库注入演示数据（学生/教师/班级/试题/试卷/成绩/证书）。

运行：python manage.py shell < api/seed.py
或：python manage.py loaddata （如果后续换成 fixtures JSON）
"""
from datetime import date, timedelta

from django.contrib.auth.models import User
from django.utils import timezone

from .models import (
    Certificate, ClassInfo, ClassMembership, Exam, Paper, PaperQuestion,
    Question, Score, UserProfile,
)


def run():
    print("== 注入演示数据 ==")

    # 1. 用户
    _make_users()
    # 2. 班级 + 成员
    _make_classes()
    # 3. 题库
    _make_questions()
    # 4. 试卷
    _make_papers()
    # 5. 测评发布
    _make_exams()
    # 6. 成绩
    _make_scores()
    # 7. 证书
    _make_certificates()

    print("== 完成 ==")


def _make_users():
    users = [
        # (username, password, is_staff, role, extra)
        ("admin",     "admin123", True,  "province_admin", {"name": "系统管理员", "phone": "13900000001"}),
        ("teacher",   "teacher",  False, "teacher",        {"name": "王美丽", "teacher_no": "T20230088", "subject": "美术/音乐", "school": "阳光小学", "district": "朝阳区", "phone": "13800000002"}),
        ("teacher2",  "teacher2", False, "teacher",        {"name": "张丽", "teacher_no": "T20230090", "subject": "音乐", "school": "阳光小学", "district": "朝阳区", "phone": "13800000003"}),
        ("student",   "student",  False, "student",        {"name": "李小明", "student_no": "2024052101", "grade": "五年级", "school": "阳光小学", "district": "朝阳区", "phone": "13700000004"}),
        ("student2",  "student2", False, "student",        {"name": "张小华", "student_no": "2024052102", "grade": "五年级", "school": "阳光小学", "district": "朝阳区", "phone": "13700000005"}),
        ("student3",  "student3", False, "student",        {"name": "陈美丽", "student_no": "2024052103", "grade": "五年级", "school": "阳光小学", "district": "朝阳区", "phone": "13700000006"}),
        ("student4",  "student4", False, "student",        {"name": "刘洋洋", "student_no": "2024052104", "grade": "五年级", "school": "阳光小学", "district": "朝阳区", "phone": "13700000007"}),
    ]
    for username, pwd, staff, role, extra in users:
        u, created = User.objects.get_or_create(username=username)
        if created:
            u.set_password(pwd)
            u.is_staff = staff
            u.first_name = extra.get("name", "")
            u.save()
            UserProfile.objects.create(
                user=u, role=role,
                student_no=extra.get("student_no", ""),
                teacher_no=extra.get("teacher_no", ""),
                grade=extra.get("grade", ""),
                subject=extra.get("subject", ""),
                school=extra.get("school", ""),
                district=extra.get("district", ""),
                phone=extra.get("phone", ""),
            )
    print(f"  用户注入：{User.objects.count()} 个")


def _make_classes():
    teacher = User.objects.get(username="teacher")
    cls, _ = ClassInfo.objects.get_or_create(
        classno="2024052", defaults={
            "name": "五(2)班", "grade": "五年级", "school": "阳光小学", "headteacher": teacher,
        },
    )
    cls2, _ = ClassInfo.objects.get_or_create(
        classno="2024051", defaults={
            "name": "五(1)班", "grade": "五年级", "school": "阳光小学", "headteacher": User.objects.get(username="teacher2"),
        },
    )

    # 学生加入
    for s in User.objects.filter(profile__role="student"):
        ClassMembership.objects.get_or_create(class_info=cls, user=s, role="student")
    # 科任教师
    ClassMembership.objects.get_or_create(class_info=cls2, user=teacher, role="subject_teacher")
    print(f"  班级注入：{ClassInfo.objects.count()} 个，成员 {ClassMembership.objects.count()} 条")


def _make_questions():
    teacher = User.objects.get(username="teacher")
    qs = [
        dict(subject="music", qtype="single", difficulty=2, grade="五年级", chapter="音阶",
             content="以下哪种属于五声音阶？",
             options=["宫商角徵羽", "do re mi fa", "1 2 3 4", "以上都对"], answer=0,
             analysis="五声音阶由宫(1)商(2)角(3)徵(5)羽(6)五个音构成。", created_by=teacher),
        dict(subject="music", qtype="single", difficulty=1, grade="五年级", chapter="唱名",
             content="在 C 大调中，sol 对应的唱名序号是？",
             options=["3", "4", "5", "6"], answer=2,
             analysis="C 大调中 do=1, re=2, mi=3, fa=4, sol=5。", created_by=teacher),
        dict(subject="music", qtype="judge", difficulty=1, grade="五年级", chapter="节奏",
             content="4/4 拍每小节有 4 拍。",
             answer=True,
             analysis="4/4 拍中，分子表示每小节拍数，分母表示每拍的音符类型。", created_by=teacher),

        dict(subject="art", qtype="single", difficulty=1, grade="五年级", chapter="色彩",
             content="红、黄、蓝是？",
             options=["二次色", "三次色", "三原色", "互补色"], answer=2,
             analysis="红、黄、蓝为色彩三原色，其它颜色可由它们混合而来。", created_by=teacher),
        dict(subject="art", qtype="single", difficulty=2, grade="五年级", chapter="构图",
             content="画面主体应放在哪个位置最舒适？",
             options=["中心", "左上角", "黄金分割点", "边缘"], answer=2,
             analysis="黄金分割点 (约 0.618) 是经典构图法则。", created_by=teacher),
        dict(subject="art", qtype="fill", difficulty=2, grade="五年级", chapter="技法",
             content="水彩画的三种基本技法分别是干画法、____ 和 ____。",
             answer=["湿画法", "渲染法"],
             analysis="干画法、湿画法、渲染法是水彩的经典技法。", created_by=teacher),
    ]
    for q in qs:
        Question.objects.get_or_create(content=q["content"], defaults=q)
    print(f"  试题注入：{Question.objects.count()} 道")


def _make_papers():
    teacher = User.objects.get(username="teacher")
    paper, _ = Paper.objects.get_or_create(
        title="音乐·节奏与旋律 测评卷",
        defaults={
            "subject": "music", "mode": "auto", "scope": "class", "status": "published",
            "duration": 40, "total_score": 100, "creator": teacher,
            "published_at": timezone.now(),
        },
    )
    art_paper, _ = Paper.objects.get_or_create(
        title="美术·色彩表达 测评卷",
        defaults={
            "subject": "art", "mode": "manual", "scope": "class", "status": "draft",
            "duration": 45, "total_score": 100, "creator": teacher,
        },
    )
    # 把题目挂上去
    music_qs = Question.objects.filter(subject="music")
    for i, q in enumerate(music_qs, 1):
        PaperQuestion.objects.get_or_create(paper=paper, question=q, defaults={"order": i, "score": 30})
    art_qs = Question.objects.filter(subject="art")
    for i, q in enumerate(art_qs, 1):
        PaperQuestion.objects.get_or_create(paper=art_paper, question=q, defaults={"order": i, "score": 30})
    print(f"  试卷注入：{Paper.objects.count()} 份")


def _make_exams():
    paper = Paper.objects.get(title="音乐·节奏与旋律 测评卷")
    exam, _ = Exam.objects.get_or_create(
        paper=paper, title="音乐正式测评 · 第五单元",
        defaults={
            "publish_to": [{"classno": "2024052"}],
            "start_at": timezone.now() - timedelta(days=7),
            "end_at": timezone.now() + timedelta(days=2),
            "creator": paper.creator,
        },
    )
    print(f"  测评注入：{Exam.objects.count()} 次")


def _make_scores():
    exam = Exam.objects.first()
    paper = Paper.objects.get(title="音乐·节奏与旋律 测评卷")
    art_paper = Paper.objects.get(title="美术·色彩表达 测评卷")
    for i, stu in enumerate(User.objects.filter(profile__role="student")):
        base = [92, 88, 85, 76, 83, 90, 78][i % 7]
        Score.objects.get_or_create(
            student=stu, subject="music", recorded_at=date.today() - timedelta(days=5 - i),
            defaults={"source": "official", "exam": exam, "paper": paper, "score": base, "total_score": 100},
        )
        Score.objects.get_or_create(
            student=stu, subject="art", recorded_at=date.today() - timedelta(days=6 - i),
            defaults={"source": "practice", "paper": art_paper, "score": base - 3, "total_score": 100},
        )
    print(f"  成绩注入：{Score.objects.count()} 条")


def _make_certificates():
    for stu in User.objects.filter(profile__role="student"):
        Certificate.objects.get_or_create(
            student=stu, subject="music", cert_no=f"M-{stu.username}-2026",
            defaults={"level": "excellent", "issued_at": date(2026, 10, 15), "score": 92},
        )
        Certificate.objects.get_or_create(
            student=stu, subject="art", cert_no=f"A-{stu.username}-2026",
            defaults={"level": "good", "issued_at": date(2026, 10, 15), "score": 85},
        )
    print(f"  证书注入：{Certificate.objects.count()} 张")
