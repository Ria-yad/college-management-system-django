import json

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .models import (
    Attendance,
    AttendanceReport,
    FeedBackStaffs,
    LeaveReportStaff,
    SessionYearModel,
    Staff,
    Staffs,
    Students,
    Subjects,
)
from .role_helpers import staff_required


def _get_staffs_profile_for_user(user):
    staff_obj = Staffs.objects.filter(admin=user).first()
    if staff_obj:
        return staff_obj

    modern_profile = Staff.objects.filter(user=user).first()
    defaults = {
        "address": getattr(modern_profile, "address", ""),
        "gender": getattr(modern_profile, "gender", ""),
    }
    staff_obj, _ = Staffs.objects.get_or_create(admin=user, defaults=defaults)
    return staff_obj


@staff_required
def staff_take_attendance(request):
    staff_obj = _get_staffs_profile_for_user(request.user)
    subjects = Subjects.objects.filter(staff_id=staff_obj).select_related("course_id")
    session_years = SessionYearModel.objects.all().order_by("-id")
    return render(
        request,
        "staff_template/take_attendance_template.html",
        {"subjects": subjects, "session_years": session_years},
    )


@staff_required
@require_POST
def get_students_ajax(request):
    subject_id = request.POST.get("subject")
    session_year_id = request.POST.get("session_year")

    if not subject_id or not session_year_id:
        return JsonResponse({"status": "error", "message": "Missing required fields."}, status=400)

    staff_obj = _get_staffs_profile_for_user(request.user)
    try:
        subject = Subjects.objects.get(id=subject_id, staff_id=staff_obj)
    except Subjects.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Invalid subject."}, status=403)

    students = Students.objects.filter(
        course_id=subject.course_id,
        session_year_id_id=session_year_id,
    ).select_related("admin")

    student_data = [
        {
            "id": student.id,
            "name": student.admin.get_full_name() or student.admin.username,
            "username": student.admin.username,
        }
        for student in students
    ]

    return JsonResponse({"status": "success", "students": student_data})


@staff_required
@require_POST
def save_attendance_data_ajax(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON payload."}, status=400)

    subject_id = payload.get("subject_id")
    session_year_id = payload.get("session_year_id")
    attendance_date = payload.get("attendance_date")
    students = payload.get("students", [])

    if not subject_id or not session_year_id or not attendance_date:
        return JsonResponse({"status": "error", "message": "Missing required fields."}, status=400)

    staff_obj = _get_staffs_profile_for_user(request.user)
    try:
        subject = Subjects.objects.get(id=subject_id, staff_id=staff_obj)
        session_year = SessionYearModel.objects.get(id=session_year_id)
    except (Subjects.DoesNotExist, SessionYearModel.DoesNotExist):
        return JsonResponse({"status": "error", "message": "Invalid subject or session."}, status=400)

    attendance, created = Attendance.objects.get_or_create(
        subject_id=subject,
        attendance_date=attendance_date,
        session_year_id=session_year,
    )
    if not created:
        return JsonResponse(
            {
                "status": "error",
                "message": "Attendance already exists for this subject, session and date. Use update attendance.",
            },
            status=400,
        )

    for item in students:
        student_id = item.get("id")
        status = bool(item.get("status", True))
        try:
            student = Students.objects.get(id=student_id)
        except Students.DoesNotExist:
            continue

        AttendanceReport.objects.create(
            student_id=student,
            attendance_id=attendance,
            status=status,
        )

    return JsonResponse({"status": "success", "message": "Attendance saved successfully."})


@staff_required
def staff_update_attendance(request):
    staff_obj = _get_staffs_profile_for_user(request.user)
    subjects = Subjects.objects.filter(staff_id=staff_obj).select_related("course_id")
    session_years = SessionYearModel.objects.all().order_by("-id")
    return render(
        request,
        "staff_template/update_attendance_template.html",
        {"subjects": subjects, "session_years": session_years},
    )


@staff_required
@require_POST
def get_attendance_dates_ajax(request):
    subject_id = request.POST.get("subject")
    session_year_id = request.POST.get("session_year")

    if not subject_id or not session_year_id:
        return JsonResponse({"status": "error", "message": "Missing required fields."}, status=400)

    staff_obj = _get_staffs_profile_for_user(request.user)
    try:
        subject = Subjects.objects.get(id=subject_id, staff_id=staff_obj)
    except Subjects.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Invalid subject."}, status=403)

    dates = Attendance.objects.filter(
        subject_id=subject,
        session_year_id_id=session_year_id,
    ).order_by("-attendance_date")

    data = [{"id": row.id, "attendance_date": str(row.attendance_date)} for row in dates]
    return JsonResponse({"status": "success", "dates": data})


@staff_required
@require_POST
def get_attendance_student_ajax(request):
    attendance_id = request.POST.get("attendance_id")
    if not attendance_id:
        return JsonResponse({"status": "error", "message": "Missing attendance id."}, status=400)

    staff_obj = _get_staffs_profile_for_user(request.user)
    try:
        attendance = Attendance.objects.select_related("subject_id").get(
            id=attendance_id,
            subject_id__staff_id=staff_obj,
        )
    except Attendance.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Attendance not found."}, status=404)

    reports = AttendanceReport.objects.filter(attendance_id=attendance).select_related("student_id__admin")
    students = [
        {
            "id": report.student_id.id,
            "name": report.student_id.admin.get_full_name() or report.student_id.admin.username,
            "status": report.status,
        }
        for report in reports
    ]
    return JsonResponse({"status": "success", "students": students})


@staff_required
@require_POST
def update_attendance_data_ajax(request):
    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON payload."}, status=400)

    attendance_id = payload.get("attendance_id")
    students = payload.get("students", [])
    if not attendance_id:
        return JsonResponse({"status": "error", "message": "Missing attendance id."}, status=400)

    staff_obj = _get_staffs_profile_for_user(request.user)
    try:
        attendance = Attendance.objects.select_related("subject_id").get(
            id=attendance_id,
            subject_id__staff_id=staff_obj,
        )
    except Attendance.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Attendance not found."}, status=404)

    for item in students:
        student_id = item.get("id")
        status = bool(item.get("status", False))
        AttendanceReport.objects.filter(
            attendance_id=attendance,
            student_id_id=student_id,
        ).update(status=status)

    return JsonResponse({"status": "success", "message": "Attendance updated successfully."})


@staff_required
def staff_apply_leave(request):
    staff = _get_staffs_profile_for_user(request.user)

    if request.method == "POST":
        leave_date = request.POST.get("leave_date")
        leave_message = request.POST.get("leave_message", "").strip()

        if leave_date and leave_message:
            LeaveReportStaff.objects.create(
                staff_id=staff,
                leave_date=leave_date,
                leave_message=leave_message,
                leave_status=0,
            )
            messages.success(request, "Leave request submitted successfully.")
            return redirect("staff_leave_view")

        messages.error(request, "Both leave date and message are required.")

    return render(request, "staff_templates/apply_leave.html")


@staff_required
def staff_leave_view(request):
    staff = _get_staffs_profile_for_user(request.user)
    leave_data = LeaveReportStaff.objects.filter(staff_id=staff).order_by("-created_at")
    return render(request, "staff_templates/view_leave.html", {"leave_data": leave_data})


@staff_required
def staff_feedback(request):
    staff = _get_staffs_profile_for_user(request.user)
    feedback_data = FeedBackStaffs.objects.filter(staff_id=staff).order_by("-created_at")
    return render(request, "staff_template/staff_feedback.html", {"feedback_data": feedback_data})


@staff_required
def staff_feedback_save(request):
    if request.method != "POST":
        return redirect("staff_feedback")

    staff = _get_staffs_profile_for_user(request.user)
    feedback_message = request.POST.get("feedback_message", "").strip()

    if not feedback_message:
        messages.error(request, "Feedback message is required.")
        return redirect("staff_feedback")

    FeedBackStaffs.objects.create(
        staff_id=staff,
        feedback=feedback_message,
        feedback_reply="",
    )
    messages.success(request, "Feedback sent successfully.")
    return redirect("staff_feedback")
