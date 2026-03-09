from django.contrib import messages
from django.shortcuts import redirect, render

from .models import AttendanceReport, FeedBackStudent, LeaveReportStudent, Students, Subjects
from .role_helpers import student_required


@student_required
def student_view_attendance(request):
    student = Students.objects.select_related("course_id").filter(admin=request.user).first()
    subjects = Subjects.objects.none()
    if student:
        subjects = Subjects.objects.filter(course_id=student.course_id).order_by("subject_name")

    context = {
        "student": student,
        "subjects": subjects,
    }
    return render(request, "student_template/student_view_attendance.html", context)


@student_required
def student_view_attendance_post(request):
    if request.method != "POST":
        return redirect("student_view_attendance")

    student = Students.objects.select_related("course_id").filter(admin=request.user).first()
    if not student:
        messages.error(request, "Student profile is not configured.")
        return redirect("student_view_attendance")

    subject_id = request.POST.get("subject")
    start_date = request.POST.get("start_date")
    end_date = request.POST.get("end_date")

    if not subject_id or not start_date or not end_date:
        messages.error(request, "Please select subject, start date and end date.")
        return redirect("student_view_attendance")

    try:
        subject = Subjects.objects.get(id=subject_id, course_id=student.course_id)
    except Subjects.DoesNotExist:
        messages.error(request, "Invalid subject selected.")
        return redirect("student_view_attendance")

    reports = AttendanceReport.objects.filter(
        student_id=student,
        attendance_id__subject_id=subject,
        attendance_id__attendance_date__range=[start_date, end_date],
    ).select_related("attendance_id").order_by("attendance_id__attendance_date")

    total_present = reports.filter(status=True).count()
    total_absent = reports.filter(status=False).count()
    total_classes = reports.count()

    context = {
        "subject": subject,
        "start_date": start_date,
        "end_date": end_date,
        "reports": reports,
        "total_present": total_present,
        "total_absent": total_absent,
        "total_classes": total_classes,
    }
    return render(request, "student_template/student_attendance_data.html", context)


@student_required
def student_apply_leave(request):
    student = Students.objects.filter(admin=request.user).first()
    if not student:
        messages.error(request, "Student profile is not configured.")
        return redirect("student_dashboard")

    if request.method == "POST":
        leave_date = request.POST.get("leave_date")
        leave_message = request.POST.get("leave_message", "").strip()

        if leave_date and leave_message:
            LeaveReportStudent.objects.create(
                student_id=student,
                leave_date=leave_date,
                leave_message=leave_message,
                leave_status=0,
            )
            messages.success(request, "Leave request submitted successfully.")
            return redirect("student_leave_view")

        messages.error(request, "Both leave date and message are required.")

    return render(request, "student_templates/apply_leave.html")


@student_required
def student_leave_view(request):
    student = Students.objects.filter(admin=request.user).first()
    leave_data = LeaveReportStudent.objects.none()
    if student:
        leave_data = LeaveReportStudent.objects.filter(student_id=student).order_by("-created_at")

    return render(request, "student_templates/view_leave.html", {"leave_data": leave_data})


@student_required
def student_feedback(request):
    student = Students.objects.filter(admin=request.user).first()
    feedback_data = FeedBackStudent.objects.none()
    if student:
        feedback_data = FeedBackStudent.objects.filter(student_id=student).order_by("-created_at")

    return render(request, "student_template/student_feedback.html", {"feedback_data": feedback_data})


@student_required
def student_feedback_save(request):
    if request.method != "POST":
        return redirect("student_feedback")

    student = Students.objects.filter(admin=request.user).first()
    if not student:
        messages.error(request, "Student profile is not configured.")
        return redirect("student_feedback")

    feedback_message = request.POST.get("feedback_message", "").strip()
    if not feedback_message:
        messages.error(request, "Feedback message is required.")
        return redirect("student_feedback")

    FeedBackStudent.objects.create(
        student_id=student,
        feedback=feedback_message,
        feedback_reply="",
    )
    messages.success(request, "Feedback sent successfully.")
    return redirect("student_feedback")
