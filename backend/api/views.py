from django.http import JsonResponse

from . import mock_data as md


def _json(payload, status=200):
    return JsonResponse(payload, json_dumps_params={"ensure_ascii": False}, status=status)


# ======================== 首页（保持不变） ========================
def home_data(request):
    data = {
        "siteName": "艺术测评系统",
        "slogan": "艺术，让生活更有色彩",
        "nav": [
            {"name": "首页", "path": "/", "active": True},
            {"name": "测评练习", "path": "/practice"},
            {"name": "成绩分析", "path": "/analysis"},
            {"name": "个人中心", "path": "/profile"},
            {"name": "系统帮助", "path": "/help"},
        ],
        "hero": {
            "tagline": "发现艺术之美 · 让成长更有色彩",
            "title": "艺术测评系统",
            "subtitle": "以艺术为桥 · 发现更好的你",
            "description": "通过专业的艺术测评，帮助你全面了解自己的艺术潜能，"
                           "激发创造力，提升艺术素养，成就更好的未来。",
            "buttonText": "开启艺术之旅",
        },
        "features": [
            {"key": "art", "title": "美术测评", "lines": ["发现你的绘画潜能", "感受色彩的魅力"], "color": "#2fbfa5", "icon": "palette"},
            {"key": "music", "title": "音乐测评", "lines": ["聆听你的音乐天赋", "感受旋律的力量"], "color": "#a06ee8", "icon": "music"},
            {"key": "dance", "title": "舞蹈测评", "lines": ["展现你的肢体语言", "释放无限可能"], "color": "#f2b23e", "icon": "dance"},
            {"key": "general", "title": "综合测评", "lines": ["多维度评估", "全面了解艺术素养"], "color": "#4f9cf9", "icon": "book"},
            {"key": "analysis", "title": "成绩分析", "lines": ["数据化分析", "助力成长与提升"], "color": "#8b7cf6", "icon": "chart"},
            {"key": "report", "title": "个人报告", "lines": ["专属艺术成长报告", "记录你的每一步进步"], "color": "#f2709c", "icon": "report"},
        ],
    }
    return _json(data)


# ======================== 登录 ========================
def login(request):
    """POST /api/login/  body: {role: 'student' | 'teacher'} (mock 不校验密码)"""
    role = request.GET.get("role")
    if not role:
        if request.content_type and "json" in request.content_type:
            import json
            body = json.loads(request.body or b"{}")
            role = body.get("role")
    user = md.USERS.get(role)
    if not user:
        return _json({"message": "角色不支持"}, status=400)
    return _json({"code": 0, "data": user})


# ======================== 学生端 ========================
def student_sidebar(request):
    return _json({"code": 0, "data": md.STUDENT_SIDEBAR})


def student_workspace(request):
    return _json({"code": 0, "data": md.STUDENT_WORKSPACE})


def student_class_detail(request):
    return _json({"code": 0, "data": md.STUDENT_CLASS_DETAIL})


def student_practice_paper(request, subject):
    return _json({"code": 0, "data": md._make_paper(subject, "practice")})


def student_official_paper(request, subject):
    return _json({"code": 0, "data": md._make_paper(subject, "official")})


# ======================== 教师端 ========================
def teacher_sidebar(request):
    return _json({"code": 0, "data": md.TEACHER_SIDEBAR})


def teacher_workspace(request):
    return _json({"code": 0, "data": md.TEACHER_WORKSPACE})


def teacher_my_classes(request):
    return _json({"code": 0, "data": md.TEACHER_WORKSPACE["myClasses"]})


def teacher_recent_papers(request):
    return _json({"code": 0, "data": md.TEACHER_WORKSPACE["recentPapers"]})


# ======================== 省级管理员端 ========================
def provincial_stats(request):
    return _json({"code": 0, "data": md.PROVINCIAL_STATS})


def provincial_exam_stats(request):
    return _json({"code": 0, "data": md.PROVINCIAL_EXAM_STATS})


def provincial_papers(request):
    return _json({"code": 0, "data": md.PROVINCIAL_PAPERS})


def provincial_publish(request):
    """省级测评发布记录（复用试卷列表中的已发布项）。"""
    published = [p for p in md.PROVINCIAL_PAPERS if p["status"] == "已发布"]
    return _json({"code": 0, "data": published})


def provincial_accounts(request, kind):
    return _json({"code": 0, "data": md.PROVINCIAL_ACCOUNTS.get(kind, [])})


def provincial_export_rate(request):
    return _json({"code": 0, "data": md.PROVINCIAL_EXPORT_RATE})


def provincial_logs(request):
    return _json({"code": 0, "data": md.PROVINCIAL_LOGS})


# ======================== 题库管理端 ========================
def qb_stats(request):
    return _json({"code": 0, "data": md.QB_STATS})


def qb_questions(request):
    return _json({"code": 0, "data": md.QB_QUESTIONS})


def qb_audit(request):
    return _json({"code": 0, "data": md.QB_AUDIT})


def qb_resources(request):
    return _json({"code": 0, "data": md.QB_RESOURCES})


def qb_courses(request):
    return _json({"code": 0, "data": md.QB_COURSES})


def qb_chapters(request):
    return _json({"code": 0, "data": md.QB_CHAPTERS})


def qb_logs(request):
    return _json({"code": 0, "data": md.QB_LOGS})
