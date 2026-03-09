from django.urls import path

from . import HodViews, StaffViews, StudentViews, views

urlpatterns = [
    path("", views.login_page, name="login_page"),
    path("logout/", views.logout_user, name="logout_user"),

    path("hod/dashboard/", views.hod_dashboard, name="hod_dashboard"),
    path("staff/dashboard/", views.staff_dashboard, name="staff_dashboard"),
    path("student/dashboard/", views.student_dashboard, name="student_dashboard"),

    path("staff/profile/", views.staff_profile, name="staff_profile"),
    path("staff/profile/update/", views.staff_profile_update, name="staff_profile_update"),
    path("student/profile/", views.student_profile, name="student_profile"),

    path("hod/staff/add/", views.add_staff, name="add_staff"),
    path("hod/staff/list/", views.list_staff, name="list_staff"),
    path("hod/staff/edit/<int:staff_id>/", views.edit_staff, name="edit_staff"),
    path("hod/staff/delete/<int:staff_id>/", views.delete_staff, name="delete_staff"),

    # HOD Student Management
    path("hod/student/list/", views.hod_list_students, name="hod_list_students"),
    path("hod/student/add/", views.hod_add_student, name="hod_add_student"),
    path("hod/student/edit/<int:student_id>/", views.hod_edit_student, name="hod_edit_student"),
    path("hod/student/delete/<int:student_id>/", views.hod_delete_student, name="hod_delete_student"),

    # HOD Course Management
    path("hod/course/list/", views.hod_list_courses, name="hod_list_courses"),
    path("hod/course/add/", views.hod_add_course, name="hod_add_course"),
    path("hod/course/edit/<int:course_id>/", views.hod_edit_course, name="hod_edit_course"),
    path("hod/course/delete/<int:course_id>/", views.hod_delete_course, name="hod_delete_course"),

    # HOD Session Management
    path("hod/session/list/", views.hod_list_sessions, name="hod_list_sessions"),
    path("hod/session/add/", views.hod_add_session, name="hod_add_session"),
    path("hod/session/edit/<int:session_id>/", views.hod_edit_session, name="hod_edit_session"),
    path("hod/session/delete/<int:session_id>/", views.hod_delete_session, name="hod_delete_session"),

    # HOD Subject Management
    path("hod/subject/list/", views.hod_list_subjects, name="hod_list_subjects"),
    path("hod/subject/add/", views.hod_add_subject, name="hod_add_subject"),
    path("hod/subject/edit/<int:subject_id>/", views.hod_edit_subject, name="hod_edit_subject"),
    path("hod/subject/delete/<int:subject_id>/", views.hod_delete_subject, name="hod_delete_subject"),

    path("staff/attendance/take/", StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path("staff/attendance/get-students/", StaffViews.get_students_ajax, name="get_students_ajax"),
    path("staff/attendance/save/", StaffViews.save_attendance_data_ajax, name="save_attendance_data_ajax"),
    path("staff/attendance/update/", StaffViews.staff_update_attendance, name="staff_update_attendance"),
    path("staff/attendance/get-dates/", StaffViews.get_attendance_dates_ajax, name="get_attendance_dates_ajax"),
    path("staff/attendance/get-attendance/", StaffViews.get_attendance_student_ajax, name="get_attendance_student_ajax"),
    path("staff/attendance/update-save/", StaffViews.update_attendance_data_ajax, name="update_attendance_data_ajax"),

    path("student/attendance/", StudentViews.student_view_attendance, name="student_view_attendance"),
    path("student/attendance/post/", StudentViews.student_view_attendance_post, name="student_view_attendance_post"),

    path("student/leave/apply/", StudentViews.student_apply_leave, name="student_apply_leave"),
    path("student/leave/view/", StudentViews.student_leave_view, name="student_leave_view"),
    path("staff/leave/apply/", StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path("staff/leave/view/", StaffViews.staff_leave_view, name="staff_leave_view"),

    path("student/feedback/", StudentViews.student_feedback, name="student_feedback"),
    path("student/feedback/save/", StudentViews.student_feedback_save, name="student_feedback_save"),
    path("staff/feedback/", StaffViews.staff_feedback, name="staff_feedback"),
    path("staff/feedback/save/", StaffViews.staff_feedback_save, name="staff_feedback_save"),

    path("hod/student/feedback/", HodViews.hod_student_feedback_list, name="hod_student_feedback_list"),
    path("hod/student/feedback/reply/", HodViews.hod_student_feedback_reply, name="hod_student_feedback_reply"),
    path("hod/staff/feedback/", HodViews.hod_staff_feedback_list, name="hod_staff_feedback_list"),
    path("hod/staff/feedback/reply/", HodViews.hod_staff_feedback_reply, name="hod_staff_feedback_reply"),

    path("hod/student/leave/", HodViews.admin_student_leave_view, name="admin_student_leave_view"),
    path("hod/student/leave/approve/<int:leave_id>/", HodViews.approve_student_leave, name="approve_student_leave"),
    path("hod/student/leave/reject/<int:leave_id>/", HodViews.reject_student_leave, name="reject_student_leave"),
    path("hod/staff/leave/", HodViews.admin_staff_leave_view, name="admin_staff_leave_view"),
    path("hod/staff/leave/approve/<int:leave_id>/", HodViews.approve_staff_leave, name="approve_staff_leave"),
    path("hod/staff/leave/reject/<int:leave_id>/", HodViews.reject_staff_leave, name="reject_staff_leave"),

    path("hod/attendance/view/", HodViews.admin_view_attendance, name="admin_view_attendance"),
    path("hod/attendance/get-dates/", HodViews.admin_get_attendance_dates_ajax, name="admin_get_attendance_dates_ajax"),
    path("hod/attendance/get-attendance/", HodViews.admin_get_attendance_student_ajax, name="admin_get_attendance_student_ajax"),
]
