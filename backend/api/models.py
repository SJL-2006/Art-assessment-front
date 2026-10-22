"""艺术测评系统核心模型

覆盖 Excel 功能设计中的学生端、教师端、学校端、题库管理端的核心实体：
用户 / 班级 / 题库 / 组卷 / 测评 / 成绩 / 证书。
"""
from django.conf import settings
from django.db import models


# ======================== 用户扩展 ========================
class UserProfile(models.Model):
    """扩展 Django auth.User，存角色、学籍、学校等业务字段。"""

    class Role(models.TextChoices):
        STUDENT = "student", "学生"
        TEACHER = "teacher", "教师"
        HEADTEACHER = "headteacher", "班主任"
        SCHOOL_ADMIN = "school_admin", "学校管理员"
        DISTRICT_ADMIN = "district_admin", "区县管理员"
        CITY_ADMIN = "city_admin", "市州管理员"
        PROVINCE_ADMIN = "province_admin", "省级管理员"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT)

    # 学生字段
    student_no = models.CharField("学籍号", max_length=32, blank=True, default="")
    grade = models.CharField("年级", max_length=16, blank=True, default="")
    avatar = models.CharField("头像标识", max_length=32, blank=True, default="")

    # 教师/管理员字段
    teacher_no = models.CharField("教师工号", max_length=32, blank=True, default="")
    subject = models.CharField("任教学科", max_length=32, blank=True, default="")

    # 归属
    school = models.CharField("学校名称", max_length=64, blank=True, default="")
    district = models.CharField("区县", max_length=32, blank=True, default="")

    phone = models.CharField("手机号", max_length=16, blank=True, default="")

    class Meta:
        verbose_name = "用户资料"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()})"


# ======================== 班级 ========================
class ClassInfo(models.Model):
    """班级（学生端"我的班级"、教师端"班级管理"）。"""
    classno = models.CharField("班级编号", max_length=32, unique=True)
    name = models.CharField("班级名称", max_length=32)      # 例如 "五(2)班"
    grade = models.CharField("年级", max_length=16)
    school = models.CharField("所属学校", max_length=64)
    headteacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="head_classes", verbose_name="班主任",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "班级"

    def __str__(self):
        return f"{self.school} {self.name}"


class ClassMembership(models.Model):
    """学生-班级、科任教师-班级 的关系表。"""

    class Role(models.TextChoices):
        STUDENT = "student", "学生"
        SUBJECT_TEACHER = "subject_teacher", "科任教师"

    class_info = models.ForeignKey(ClassInfo, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="class_memberships")
    role = models.CharField(max_length=20, choices=Role.choices)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "班级成员"
        unique_together = ("class_info", "user", "role")

    def __str__(self):
        return f"{self.user} · {self.role} · {self.class_info}"


# ======================== 题库 ========================
class Subject(models.TextChoices):
    MUSIC = "music", "音乐"
    ART = "art", "美术"
    DANCE = "dance", "舞蹈"
    GENERAL = "general", "综合"


class Question(models.Model):
    """试题（题库管理端）。"""

    class Type(models.TextChoices):
        SINGLE = "single", "单选题"
        MULTIPLE = "multiple", "多选题"
        JUDGE = "judge", "判断题"
        FILL = "fill", "填空题"
        WRITE = "write", "简答题"
        PERFORM = "perform", "实操题"

    class Difficulty(models.IntegerChoices):
        EASY = 1, "简单"
        MEDIUM = 2, "中等"
        HARD = 3, "困难"

    subject = models.CharField("学科", max_length=16, choices=Subject.choices)
    qtype = models.CharField("题型", max_length=16, choices=Type.choices)
    difficulty = models.IntegerField("难度", choices=Difficulty.choices, default=Difficulty.MEDIUM)
    grade = models.CharField("适用年级", max_length=16, blank=True, default="")
    chapter = models.CharField("章节/知识点", max_length=64, blank=True, default="")
    content = models.TextField("题干")
    options = models.JSONField("选项列表", blank=True, null=True, help_text='["A", "B", "C", "D"]')
    answer = models.JSONField("标准答案", help_text="单选存下标 int；多选存下标数组；填空/简答存文本")
    analysis = models.TextField("答案解析", blank=True, default="")
    audio = models.URLField("音频资源", blank=True, default="")
    image = models.URLField("图片资源", blank=True, default="")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="questions"
    )
    is_approved = models.BooleanField("已审核", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "试题"
        ordering = ["-created_at"]

    def __str__(self):
        return f"[{self.get_subject_display()}] {self.content[:20]}"


# ======================== 组卷 ========================
class Paper(models.Model):
    """试卷（手动 / 自动组卷，校级以上也共用）。"""

    class Mode(models.TextChoices):
        MANUAL = "manual", "手动组卷"
        AUTO = "auto", "自动组卷"

    class Scope(models.TextChoices):
        CLASS = "class", "班级级"
        SCHOOL = "school", "校级"
        DISTRICT = "district", "区县级"
        CITY = "city", "市州级"
        PROVINCE = "province", "省级"

    class Status(models.TextChoices):
        DRAFT = "draft", "草稿"
        PUBLISHED = "published", "已发布"
        RECALLED = "recalled", "已撤回"

    title = models.CharField("试卷标题", max_length=120)
    subject = models.CharField("学科", max_length=16, choices=Subject.choices)
    mode = models.CharField("组卷方式", max_length=16, choices=Mode.choices, default=Mode.MANUAL)
    scope = models.CharField("发布范围", max_length=16, choices=Scope.choices, default=Scope.CLASS)
    status = models.CharField("状态", max_length=16, choices=Status.choices, default=Status.DRAFT)
    duration = models.PositiveIntegerField("限时(分钟)", default=40)
    total_score = models.PositiveIntegerField("总分", default=100)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="papers"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "试卷"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class PaperQuestion(models.Model):
    """试卷-试题 多对多中间表（记录顺序和分值）。"""
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="items")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="paper_items")
    order = models.PositiveIntegerField("题号")
    score = models.PositiveIntegerField("本题分值", default=5)

    class Meta:
        verbose_name = "试卷试题"
        ordering = ["order"]
        unique_together = ("paper", "question")


# ======================== 测评发布 ========================
class Exam(models.Model):
    """一次正式测评发布。一份试卷可以多次发布（给不同班级/年级）。"""
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE, related_name="exams")
    title = models.CharField("测评名称", max_length=120)
    publish_to = models.JSONField("发布范围", help_text='[{"classno":"C001"},{"grade":"五年级"}]')
    start_at = models.DateTimeField("开始时间")
    end_at = models.DateTimeField("结束时间")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="exams"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "正式测评"
        ordering = ["-start_at"]

    def __str__(self):
        return self.title


# ======================== 成绩 ========================
class Score(models.Model):
    """成绩记录（正式测评 / 练习 / 平时表现 统一入库）。"""

    class Source(models.TextChoices):
        OFFICIAL = "official", "正式测评"
        PRACTICE = "practice", "练习"
        USUAL = "usual", "平时表现"
        IMPORT = "import", "线下导入"

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="scores", verbose_name="学生"
    )
    exam = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True, related_name="scores")
    paper = models.ForeignKey(Paper, on_delete=models.SET_NULL, null=True, blank=True, related_name="scores")
    source = models.CharField("来源", max_length=16, choices=Source.choices, default=Source.OFFICIAL)
    subject = models.CharField("学科", max_length=16, choices=Subject.choices)
    score = models.DecimalField("得分", max_digits=5, decimal_places=1)
    total_score = models.PositiveIntegerField("满分", default=100)
    recorded_at = models.DateField("测评日期")
    remark = models.CharField("备注", max_length=255, blank=True, default="")

    class Meta:
        verbose_name = "成绩"
        ordering = ["-recorded_at"]
        indexes = [models.Index(fields=["student", "subject", "recorded_at"])]

    def __str__(self):
        return f"{self.student} · {self.get_subject_display()} · {self.score}"


# ======================== 证书 ========================
class Certificate(models.Model):
    """测评证书（学生端"我的证书"）。"""

    class Level(models.TextChoices):
        EXCELLENT = "excellent", "优秀"
        GOOD = "good", "良好"
        PASS = "pass", "合格"

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="certificates", verbose_name="学生"
    )
    subject = models.CharField("学科", max_length=16, choices=Subject.choices)
    level = models.CharField("等级", max_length=16, choices=Level.choices)
    cert_no = models.CharField("证书编号", max_length=32, unique=True)
    issued_at = models.DateField("颁发日期")
    score = models.DecimalField("对应成绩", max_digits=5, decimal_places=1, null=True, blank=True)

    class Meta:
        verbose_name = "证书"
        ordering = ["-issued_at"]

    def __str__(self):
        return f"{self.student} · {self.get_subject_display()} · {self.get_level_display()}"
