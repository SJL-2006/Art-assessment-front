"""Django admin 后台注册 —— 把所有业务模型挂到 /admin/ 方便查看。"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (
    Certificate, ClassInfo, ClassMembership, Exam, Paper, PaperQuestion,
    Question, Score, UserProfile,
)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name = "扩展资料"


# 先取消 auth 默认的 UserAdmin 注册，再挂上扩展版
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [UserProfileInline]
    list_display = ("username", "first_name", "email", "is_staff", "is_active")
    list_filter = ("is_staff", "profile__role")


@admin.register(ClassInfo)
class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ("classno", "name", "grade", "school", "headteacher")


@admin.register(ClassMembership)
class ClassMembershipAdmin(admin.ModelAdmin):
    list_display = ("class_info", "user", "role")
    list_filter = ("role",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "subject", "qtype", "difficulty", "chapter", "content_summary")
    list_filter = ("subject", "qtype", "difficulty")
    search_fields = ("content", "chapter")

    def content_summary(self, obj):
        return obj.content[:30] + "..." if len(obj.content) > 30 else obj.content


@admin.register(Paper)
class PaperAdmin(admin.ModelAdmin):
    list_display = ("title", "subject", "mode", "scope", "status", "duration", "total_score", "creator")
    list_filter = ("subject", "mode", "status")


@admin.register(PaperQuestion)
class PaperQuestionAdmin(admin.ModelAdmin):
    list_display = ("paper", "question", "order", "score")


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("title", "paper", "start_at", "end_at", "creator")


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display = ("student", "subject", "source", "score", "total_score", "recorded_at")
    list_filter = ("subject", "source")


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("cert_no", "student", "subject", "level", "issued_at")
