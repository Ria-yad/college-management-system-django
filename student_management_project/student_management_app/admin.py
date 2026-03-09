from django.contrib import admin

from .models import (
    Attendance,
    AttendanceReport,
    Courses,
    CustomUser,
    FeedBackStaffs,
    FeedBackStudent,
    LeaveReportStaff,
    LeaveReportStudent,
    SessionYearModel,
    Staff,
    Staffs,
    Students,
    Subjects,
)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "user_type", "is_active")
    list_filter = ("user_type", "is_active", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("get_full_name", "user", "gender", "created_at")
    list_filter = ("gender", "created_at")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name")
    readonly_fields = ("created_at", "updated_at")

    def get_full_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = "Name"


@admin.register(Staffs)
class StaffsAdmin(admin.ModelAdmin):
    list_display = ("admin", "gender", "created_at")
    list_filter = ("gender", "created_at")
    search_fields = ("admin__username", "admin__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ("admin", "course_id", "session_year_id", "gender", "created_at")
    list_filter = ("gender", "course_id", "session_year_id", "created_at")
    search_fields = ("admin__username", "admin__email", "admin__first_name", "admin__last_name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Courses)
class CoursesAdmin(admin.ModelAdmin):
    list_display = ("course_name", "created_at")
    search_fields = ("course_name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(SessionYearModel)
class SessionYearModelAdmin(admin.ModelAdmin):
    list_display = ("session_start_year", "session_end_year")
    ordering = ("-session_start_year",)


@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ("subject_name", "course_id", "staff_id", "created_at")
    list_filter = ("course_id", "staff_id", "created_at")
    search_fields = ("subject_name", "course_id__course_name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("subject_id", "attendance_date", "session_year_id", "created_at")
    list_filter = ("subject_id", "attendance_date", "session_year_id")
    search_fields = ("subject_id__subject_name",)
    readonly_fields = ("created_at", "updated_at")
    actions = None


@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ("student_id", "attendance_id", "status", "created_at")
    list_filter = ("status", "created_at", "attendance_id__attendance_date")
    search_fields = ("student_id__admin__username",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(LeaveReportStudent)
class LeaveReportStudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "leave_date", "leave_status", "created_at")
    list_filter = ("leave_status", "leave_date", "created_at")
    search_fields = ("student_id__admin__username", "student_id__admin__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(LeaveReportStaff)
class LeaveReportStaffAdmin(admin.ModelAdmin):
    list_display = ("staff_id", "leave_date", "leave_status", "created_at")
    list_filter = ("leave_status", "leave_date", "created_at")
    search_fields = ("staff_id__admin__username", "staff_id__admin__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(FeedBackStudent)
class FeedBackStudentAdmin(admin.ModelAdmin):
    list_display = ("student_id", "created_at", "has_reply")
    list_filter = ("created_at",)
    search_fields = ("student_id__admin__username", "feedback")
    readonly_fields = ("created_at", "updated_at")

    def has_reply(self, obj):
        return bool(obj.feedback_reply.strip())
    has_reply.boolean = True
    has_reply.short_description = "Replied"


@admin.register(FeedBackStaffs)
class FeedBackStaffsAdmin(admin.ModelAdmin):
    list_display = ("staff_id", "created_at", "has_reply")
    list_filter = ("created_at",)
    search_fields = ("staff_id__admin__username", "feedback")
    readonly_fields = ("created_at", "updated_at")

    def has_reply(self, obj):
        return bool(obj.feedback_reply.strip())
    has_reply.boolean = True
    has_reply.short_description = "Replied"
