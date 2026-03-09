from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    StaffCreateForm, StaffProfileUpdateForm, StaffUpdateForm,
    StudentCreateForm, StudentUpdateForm, CourseForm, SessionForm, SubjectForm
)
from .models import (
    Attendance, Courses, Staff, Staffs, Students, SessionYearModel, Subjects
)
from .role_helpers import dashboard_name_for_user, hod_required, staff_required, student_required


def login_page(request):
    context = {}

    if request.user.is_authenticated:
        dashboard_name = dashboard_name_for_user(request.user)
        if dashboard_name:
            return redirect(dashboard_name)

        logout(request)
        context["error"] = "Your account role is not configured. Please contact admin."
        return render(request, "student_management_app/login.html", context)

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            dashboard_name = dashboard_name_for_user(user)
            if dashboard_name:
                return redirect(dashboard_name)

            logout(request)
            context["error"] = "Your account role is not configured. Please contact admin."
        else:
            context["error"] = "Invalid username or password."

    return render(request, "student_management_app/login.html", context)


@hod_required
def hod_dashboard(request):
    context = {
        "total_students": Students.objects.count(),
        "total_staff": Staffs.objects.count(),
        "total_courses": Courses.objects.count(),
        "total_attendance": Attendance.objects.count(),
    }
    return render(request, "student_management_app/hod_dashboard.html", context)


@staff_required
def staff_dashboard(request):
    staff_profile = Staff.objects.filter(user=request.user).first()
    context = {
        "staff_profile": staff_profile,
        "total_students": Students.objects.count(),
        "total_staff": Staffs.objects.count(),
        "total_courses": Courses.objects.count(),
        "total_attendance_marked": Attendance.objects.count(),
    }
    return render(request, "staff_templates/dashboard.html", context)


@staff_required
def staff_profile(request):
    staff_profile_obj = Staff.objects.filter(user=request.user).first()
    context = {
        "staff": staff_profile_obj,
    }
    return render(request, "staff_templates/profile.html", context)


@staff_required
def staff_profile_update(request):
    staff_profile_obj = Staff.objects.filter(user=request.user).first()
    form = StaffProfileUpdateForm(
        request.POST or None,
        user=request.user,
        staff=staff_profile_obj,
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("staff_profile")

    return render(request, "staff_templates/profile_update.html", {"form": form})


@student_required
def student_dashboard(request):
    context = {
        "total_students": Students.objects.count(),
        "total_staff": Staffs.objects.count(),
        "total_courses": Courses.objects.count(),
        "total_attendance": Attendance.objects.count(),
    }
    return render(request, "student_templates/dashboard.html", context)


@student_required
def student_profile(request):
    student = Students.objects.filter(admin=request.user).first()
    context = {
        "student": student,
    }
    return render(request, "student_templates/profile.html", context)


@hod_required
def add_staff(request):
    form = StaffCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("list_staff")
    return render(request, "hod_templates/add_staff.html", {"form": form})


@hod_required
def list_staff(request):
    staff_list = Staff.objects.select_related("user").all().order_by("-created_at")
    return render(request, "hod_templates/list_staff.html", {"staff_list": staff_list})


@hod_required
def edit_staff(request, staff_id):
    staff = get_object_or_404(Staff.objects.select_related("user"), pk=staff_id)
    form = StaffUpdateForm(request.POST or None, staff=staff)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("list_staff")
    return render(request, "hod_templates/edit_staff.html", {"form": form, "staff": staff})


@hod_required
def delete_staff(request, staff_id):
    staff = get_object_or_404(Staff.objects.select_related("user"), pk=staff_id)
    staff.user.delete()
    return redirect("list_staff")


# ===== HOD STUDENT MANAGEMENT =====

@hod_required
def hod_list_students(request):
    students = Students.objects.select_related("admin", "course_id", "session_year_id").all().order_by("-created_at")
    return render(request, "hod_templates/list_students.html", {"students": students})


@hod_required
def hod_add_student(request):
    form = StudentCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student created successfully.")
        return redirect("hod_list_students")
    return render(request, "hod_templates/add_student.html", {"form": form})


@hod_required
def hod_edit_student(request, student_id):
    student = get_object_or_404(Students.objects.select_related("admin"), pk=student_id)
    form = StudentUpdateForm(request.POST or None, student=student)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Student updated successfully.")
        return redirect("hod_list_students")
    return render(request, "hod_templates/edit_student.html", {"form": form, "student": student})


@hod_required
def hod_delete_student(request, student_id):
    student = get_object_or_404(Students.objects.select_related("admin"), pk=student_id)
    student.admin.delete()
    messages.success(request, "Student deleted successfully.")
    return redirect("hod_list_students")


# ===== HOD COURSE MANAGEMENT =====

@hod_required
def hod_list_courses(request):
    courses = Courses.objects.all().order_by("-created_at")
    return render(request, "hod_templates/list_courses.html", {"courses": courses})


@hod_required
def hod_add_course(request):
    form = CourseForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Course created successfully.")
        return redirect("hod_list_courses")
    return render(request, "hod_templates/add_course.html", {"form": form})


@hod_required
def hod_edit_course(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    form = CourseForm(request.POST or None, instance=course)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Course updated successfully.")
        return redirect("hod_list_courses")
    return render(request, "hod_templates/edit_course.html", {"form": form, "course": course})


@hod_required
def hod_delete_course(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    course.delete()
    messages.success(request, "Course deleted successfully.")
    return redirect("hod_list_courses")


# ===== HOD SESSION MANAGEMENT =====

@hod_required
def hod_list_sessions(request):
    sessions = SessionYearModel.objects.all().order_by("-session_start_year")
    return render(request, "hod_templates/list_sessions.html", {"sessions": sessions})


@hod_required
def hod_add_session(request):
    form = SessionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Session created successfully.")
        return redirect("hod_list_sessions")
    return render(request, "hod_templates/add_session.html", {"form": form})


@hod_required
def hod_edit_session(request, session_id):
    session = get_object_or_404(SessionYearModel, pk=session_id)
    form = SessionForm(request.POST or None, instance=session)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Session updated successfully.")
        return redirect("hod_list_sessions")
    return render(request, "hod_templates/edit_session.html", {"form": form, "session": session})


@hod_required
def hod_delete_session(request, session_id):
    session = get_object_or_404(SessionYearModel, pk=session_id)
    session.delete()
    messages.success(request, "Session deleted successfully.")
    return redirect("hod_list_sessions")


# ===== HOD SUBJECT MANAGEMENT =====

@hod_required
def hod_list_subjects(request):
    subjects = Subjects.objects.select_related("course_id", "staff_id").all().order_by("-created_at")
    return render(request, "hod_templates/list_subjects.html", {"subjects": subjects})


@hod_required
def hod_add_subject(request):
    form = SubjectForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Subject created successfully.")
        return redirect("hod_list_subjects")
    return render(request, "hod_templates/add_subject.html", {"form": form})


@hod_required
def hod_edit_subject(request, subject_id):
    subject = get_object_or_404(Subjects, pk=subject_id)
    form = SubjectForm(request.POST or None, instance=subject)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Subject updated successfully.")
        return redirect("hod_list_subjects")
    return render(request, "hod_templates/edit_subject.html", {"form": form, "subject": subject})


@hod_required
def hod_delete_subject(request, subject_id):
    subject = get_object_or_404(Subjects, pk=subject_id)
    subject.delete()
    messages.success(request, "Subject deleted successfully.")
    return redirect("hod_list_subjects")


def logout_user(request):
    logout(request)
    return redirect("login_page")
