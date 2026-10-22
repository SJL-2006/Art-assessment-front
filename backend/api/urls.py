from django.urls import path

from . import views

urlpatterns = [
    # 首页
    path("home/", views.home_data, name="home-data"),
    # 登录
    path("login/", views.login, name="login"),
    # 学生端
    path("student/sidebar/", views.student_sidebar, name="student-sidebar"),
    path("student/workspace/", views.student_workspace, name="student-workspace"),
    path("student/class/", views.student_class_detail, name="student-class"),
    path("student/practice/<str:subject>/", views.student_practice_paper, name="student-practice"),
    path("student/official/<str:subject>/", views.student_official_paper, name="student-official"),
    # 教师端
    path("teacher/sidebar/", views.teacher_sidebar, name="teacher-sidebar"),
    path("teacher/workspace/", views.teacher_workspace, name="teacher-workspace"),
    path("teacher/classes/", views.teacher_my_classes, name="teacher-classes"),
    path("teacher/papers/recent/", views.teacher_recent_papers, name="teacher-papers-recent"),
    # 省级管理员端
    path("provincial/stats/", views.provincial_stats, name="provincial-stats"),
    path("provincial/exam-stats/", views.provincial_exam_stats, name="provincial-exam-stats"),
    path("provincial/papers/", views.provincial_papers, name="provincial-papers"),
    path("provincial/publish/", views.provincial_publish, name="provincial-publish"),
    path("provincial/accounts/<str:kind>/", views.provincial_accounts, name="provincial-accounts"),
    path("provincial/export-rate/", views.provincial_export_rate, name="provincial-export-rate"),
    path("provincial/logs/", views.provincial_logs, name="provincial-logs"),
    # 题库管理端
    path("qb/stats/", views.qb_stats, name="qb-stats"),
    path("qb/questions/", views.qb_questions, name="qb-questions"),
    path("qb/audit/", views.qb_audit, name="qb-audit"),
    path("qb/resources/", views.qb_resources, name="qb-resources"),
    path("qb/courses/", views.qb_courses, name="qb-courses"),
    path("qb/chapters/", views.qb_chapters, name="qb-chapters"),
    path("qb/logs/", views.qb_logs, name="qb-logs"),
]
