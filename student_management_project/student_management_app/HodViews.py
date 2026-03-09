from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import (
    Attendance,
    AttendanceReport,
    FeedBackStaffs,
    FeedBackStudent,
    LeaveReportStaff,
    LeaveReportStudent,
    SessionYearModel,
    Subjects,
)
from .role_helpers import hod_required


@hod_required
def admin_view_attendance(request):
    subjects = Subjects.objects.select_related("course_id", "staff_id__admin").all().order_by("subject_name")
    session_years = SessionYearModel.objects.all().order_by("-id")
    return render(
        request,
        "hod_template/admin_view_attendance.html",
        {"subjects": subjects, "session_years": session_years},
    )


@hod_required
@require_POST
def admin_get_attendance_dates_ajax(request):
    subject_id = request.POST.get("subject")
    session_year_id = request.POST.get("session_year")

    if not subject_id or not session_year_id:
        return JsonResponse({"status": "error", "message": "Missing required fields."}, status=400)

    dates = Attendance.objects.filter(
        subject_id_id=subject_id,
        session_year_id_id=session_year_id,
    ).order_by("-attendance_date")

    data = [{"id": row.id, "attendance_date": str(row.attendance_date)} for row in dates]
    return JsonResponse({"status": "success", "dates": data})


@hod_required
@require_POST
def admin_get_attendance_student_ajax(request):
    attendance_id = request.POST.get("attendance_id")
    if not attendance_id:
        return JsonResponse({"status": "error", "message": "Missing attendance id."}, status=400)

    try:
        attendance = Attendance.objects.get(id=attendance_id)
    except Attendance.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Attendance not found."}, status=404)

    reports = AttendanceReport.objects.filter(attendance_id=attendance).select_related("student_id__admin")
    students = [
        {
            "name": report.student_id.admin.get_full_name() or report.student_id.admin.username,
            "username": report.student_id.admin.username,
            "status": report.status,
        }
        for report in reports
    ]

    return JsonResponse({"status": "success", "students": students})


@hod_required
def admin_student_leave_view(request):
    leave_data = LeaveReportStudent.objects.select_related("student_id__admin").order_by("-created_at")
    return render(request, "hod_templates/student_leave_list.html", {"leave_data": leave_data})


@hod_required
def approve_student_leave(request, leave_id):
    leave = get_object_or_404(LeaveReportStudent, id=leave_id)
    leave.leave_status = 1
    leave.save(update_fields=["leave_status", "updated_at"])
    return redirect("admin_student_leave_view")


@hod_required
def reject_student_leave(request, leave_id):
    leave = get_object_or_404(LeaveReportStudent, id=leave_id)
    leave.leave_status = 2
    leave.save(update_fields=["leave_status", "updated_at"])
    return redirect("admin_student_leave_view")


@hod_required
def admin_staff_leave_view(request):
    leave_data = LeaveReportStaff.objects.select_related("staff_id__admin").order_by("-created_at")
    return render(request, "hod_templates/staff_leave_list.html", {"leave_data": leave_data})


@hod_required
def approve_staff_leave(request, leave_id):
    leave = get_object_or_404(LeaveReportStaff, id=leave_id)
    leave.leave_status = 1
    leave.save(update_fields=["leave_status", "updated_at"])
    return redirect("admin_staff_leave_view")


@hod_required
def reject_staff_leave(request, leave_id):
    leave = get_object_or_404(LeaveReportStaff, id=leave_id)
    leave.leave_status = 2
    leave.save(update_fields=["leave_status", "updated_at"])
    return redirect("admin_staff_leave_view")


@hod_required
def hod_student_feedback_list(request):
    feedback_data = FeedBackStudent.objects.select_related("student_id__admin").order_by("-created_at")
    return render(request, "hod_template/student_feedback_template.html", {"feedback_data": feedback_data})


@hod_required
def hod_student_feedback_reply(request):
    if request.method != "POST":
        return redirect("hod_student_feedback_list")

    feedback_id = request.POST.get("feedback_id")
    reply_text = request.POST.get("reply_text", "").strip()

    feedback = get_object_or_404(FeedBackStudent, id=feedback_id)
    feedback.feedback_reply = reply_text
    feedback.save(update_fields=["feedback_reply", "updated_at"])

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse("True", safe=False)

    return redirect("hod_student_feedback_list")


@hod_required
def hod_staff_feedback_list(request):
    feedback_data = FeedBackStaffs.objects.select_related("staff_id__admin").order_by("-created_at")
    return render(request, "hod_template/staff_feedback_template.html", {"feedback_data": feedback_data})


@hod_required
def hod_staff_feedback_reply(request):
    if request.method != "POST":
        return redirect("hod_staff_feedback_list")

    feedback_id = request.POST.get("feedback_id")
    reply_text = request.POST.get("reply_text", "").strip()

    feedback = get_object_or_404(FeedBackStaffs, id=feedback_id)
    feedback.feedback_reply = reply_text
    feedback.save(update_fields=["feedback_reply", "updated_at"])

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse("True", safe=False)

    return redirect("hod_staff_feedback_list")
