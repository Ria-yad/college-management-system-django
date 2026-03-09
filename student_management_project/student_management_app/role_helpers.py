from functools import wraps

from django.shortcuts import redirect


ROLE_DASHBOARD_MAP = {
    "HOD": "hod_dashboard",
    "STAFF": "staff_dashboard",
    "STUDENT": "student_dashboard",
    "1": "hod_dashboard",
    "2": "staff_dashboard",
    "3": "student_dashboard",
}


def dashboard_name_for_user(user):
    role = (getattr(user, "user_type", "") or "").strip().upper()
    dashboard_name = ROLE_DASHBOARD_MAP.get(role)
    if dashboard_name:
        return dashboard_name

    if getattr(user, "is_superuser", False):
        return "hod_dashboard"

    return None


def role_required(expected_dashboard_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login_page")
            if dashboard_name_for_user(request.user) != expected_dashboard_name:
                return redirect("login_page")
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator


hod_required = role_required("hod_dashboard")
staff_required = role_required("staff_dashboard")
student_required = role_required("student_dashboard")
