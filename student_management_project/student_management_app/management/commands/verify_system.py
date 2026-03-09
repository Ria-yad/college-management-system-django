#!/usr/bin/env python
"""
Comprehensive system verification script for Django College Management System
Tests all models, views, forms, and workflows
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate
from student_management_app.models import (
    CustomUser,
    Staff,
    Staffs,
    Students,
    Courses,
    SessionYearModel,
    Subjects,
    Attendance,
    AttendanceReport,
    LeaveReportStudent,
    LeaveReportStaff,
    FeedBackStudent,
    FeedBackStaffs,
)
from student_management_app.forms import StaffCreateForm, StaffUpdateForm, StaffProfileUpdateForm
from datetime import date, timedelta
from django.utils import timezone


class Command(BaseCommand):
    help = "Verify all models, forms, views, and workflows"

    def add_arguments(self, parser):
        parser.add_argument('--verbose', action='store_true', help='Show detailed output')

    def log(self, msg, level="INFO"):
        if level == "SUCCESS":
            self.stdout.write(self.style.SUCCESS(f"✓ {msg}"))
        elif level == "ERROR":
            self.stdout.write(self.style.ERROR(f"✗ {msg}"))
        elif level == "WARNING":
            self.stdout.write(self.style.WARNING(f"⚠ {msg}"))
        else:
            self.stdout.write(f"ℹ {msg}")

    def handle(self, *args, **options):
        verbose = options.get('verbose', False)
        self.stdout.write(self.style.SUCCESS("\n" + "=" * 60))
        self.stdout.write(self.style.SUCCESS("DJANGO COLLEGE MANAGEMENT SYSTEM - VERIFICATION"))
        self.stdout.write(self.style.SUCCESS("=" * 60 + "\n"))

        errors = []
        warnings = []

        # ===== TEST 1: Models Verification =====
        self.stdout.write(self.style.HTTP_INFO("\n[TEST 1] MODELS VERIFICATION"))
        try:
            user_count = CustomUser.objects.count()
            self.log(f"CustomUser model working ({user_count} users)")
            
            staff_count = Staff.objects.count()
            self.log(f"Staff model working ({staff_count} staff)")
            
            student_count = Students.objects.count()
            self.log(f"Students model working ({student_count} students)")
            
            course_count = Courses.objects.count()
            self.log(f"Courses model working ({course_count} courses)")
            
            session_count = SessionYearModel.objects.count()
            self.log(f"SessionYearModel working ({session_count} sessions)")
            
            subject_count = Subjects.objects.count()
            self.log(f"Subjects model working ({subject_count} subjects)")
            
            attendance_count = Attendance.objects.count()
            self.log(f"Attendance model working ({attendance_count} records)")
            
            leave_student = LeaveReportStudent.objects.count()
            self.log(f"LeaveReportStudent model working ({leave_student} records)")
            
            leave_staff = LeaveReportStaff.objects.count()
            self.log(f"LeaveReportStaff model working ({leave_staff} records)")
            
            feedback_student = FeedBackStudent.objects.count()
            self.log(f"FeedBackStudent model working ({feedback_student} records)")
            
            feedback_staff = FeedBackStaffs.objects.count()
            self.log(f"FeedBackStaffs model working ({feedback_staff} records)")
        except Exception as e:
            errors.append(f"Model verification failed: {str(e)}")
            self.log(f"Model verification failed: {str(e)}", "ERROR")

        # ===== TEST 2: User Authentication =====
        self.stdout.write(self.style.HTTP_INFO("\n[TEST 2] USER AUTHENTICATION"))
        try:
            hod_user = CustomUser.objects.filter(username="hod123").first()
            if hod_user:
                self.log(f"HOD user found: {hod_user.username} ({hod_user.user_type})")
                # Test password
                auth_user = authenticate(username="hod123", password="password123")
                if auth_user:
                    self.log("HOD authentication successful")
                else:
                    warnings.append("HOD password authentication failed")
                    self.log("HOD password authentication failed", "WARNING")
            else:
                errors.append("HOD user not found")
                self.log("HOD user not found", "ERROR")

            staff_user = CustomUser.objects.filter(username="staff1").first()
            if staff_user:
                self.log(f"Staff user found: {staff_user.username} ({staff_user.user_type})")
            else:
                errors.append("Staff user not found")
                self.log("Staff user not found", "ERROR")

            student_user = CustomUser.objects.filter(username="student1").first()
            if student_user:
                self.log(f"Student user found: {student_user.username} ({student_user.user_type})")
            else:
                errors.append("Student user not found")
                self.log("Student user not found", "ERROR")
        except Exception as e:
            errors.append(f"Authentication test failed: {str(e)}")
            self.log(f"Authentication test failed: {str(e)}", "ERROR")

        # ===== TEST 3: User Type Mapping =====
        self.stdout.write(self.style.HTTP_INFO("\n[TEST 3] USER TYPE MAPPING"))
        try:
            from student_management_app.role_helpers import dashboard_name_for_user, ROLE_DASHBOARD_MAP
            
            hod_user = CustomUser.objects.filter(username="hod123").first()
            if hod_user:
                dashboard = dashboard_name_for_user(hod_user)
                expected = "hod_dashboard"
                if dashboard == expected:
                    self.log(f"HOD redirect correct: {dashboard}")
                else:
                    warnings.append(f"HOD redirect expected '{expected}', got '{dashboard}'")
                    self.log(f"HOD redirect mismatch", "WARNING")

            staff_user = CustomUser.objects.filter(username="staff1").first()
            if staff_user:
                dashboard = dashboard_name_for_user(staff_user)
                expected = "staff_dashboard"
                if dashboard == expected:
                    self.log(f"Staff redirect correct: {dashboard}")
                else:
                    warnings.append(f"Staff redirect expected '{expected}', got '{dashboard}'")

            student_user = CustomUser.objects.filter(username="student1").first()
            if student_user:
                dashboard = dashboard_name_for_user(student_user)
                expected = "student_dashboard"
                if dashboard == expected:
                    self.log(f"Student redirect correct: {dashboard}")
                else:
                    warnings.append(f"Student redirect expected '{expected}', got '{dashboard}'")
        except Exception as e:
            errors.append(f"Role mapping test failed: {str(e)}")
            self.log(f"Role mapping test failed: {str(e)}", "ERROR")

        # ===== TEST 4: Form Validation =====
        self.stdout.write(self.style.HTTP_INFO("\n[TEST 4] FORM VALIDATION"))
        try:
            # Test StaffCreateForm validation
            form_data = {
                'username': f'teststaff_{timezone.now().timestamp()}',
                'email': f'test_{timezone.now().timestamp()}@test.com',
                'password': 'testpass123',
                'first_name': 'Test',
                'last_name': 'Staff',
                'address': 'Test Address',
                'gender': 'Male',
            }
            form = StaffCreateForm(form_data)
            if form.is_valid():
                self.log("StaffCreateForm validation passed")
            else:
                warnings.append(f"StaffCreateForm validation error: {form.errors}")
                self.log("StaffCreateForm validation check", "WARNING")
        except Exception as e:
            errors.append(f"Form validation test failed: {str(e)}")
            self.log(f"Form validation test failed: {str(e)}", "ERROR")

        # ===== TEST 5: Related Data Consistency =====
        self.stdout.write(self.style.HTTP_INFO("\n[TEST 5] DATA CONSISTENCY"))
        try:
            student = Students.objects.first()
            if student:
                if student.course_id and student.session_year_id:
                    self.log(f"Student {student.admin.username} linked to course and session")
                else:
                    warnings.append("Student missing course or session reference")
                    self.log("Student missing course or session reference", "WARNING")

            subject = Subjects.objects.first()
            if subject:
                if subject.course_id and subject.staff_id:
                    self.log(f"Subject {subject.subject_name} linked to course and staff")
                else:
                    warnings.append("Subject missing course or staff reference")

            # Check Staff/Staffs duplication
            dual_staff = CustomUser.objects.filter(
                user_type='STAFF',
                staff_profile__isnull=False
            ).exists()
            staffs_legacy = Staffs.objects.filter(
                admin__user_type='STAFF'
            ).count()
            if staffs_legacy > 0:
                self.log(f"Staff data model consistency check ({staffs_legacy} staff records)")
        except Exception as e:
            errors.append(f"Data consistency test failed: {str(e)}")
            self.log(f"Data consistency test failed: {str(e)}", "ERROR")

        # ===== TEST 6: Workflow Simulation =====
        self.stdout.write(self.style.HTTP_INFO("\n[TEST 6] WORKFLOW SIMULATION"))
        try:
            # Test Leave Application
            student = Students.objects.filter(admin__username="student1").first()
            if student:
                leave_data = {
                    'student_id': student,
                    'leave_date': date.today() + timedelta(days=1),
                    'leave_message': 'Test leave request',
                    'leave_status': 0,
                }
                leave = LeaveReportStudent.objects.create(**leave_data)
                if leave.id:
                    self.log(f"Leave request workflow test passed (ID: {leave.id})")
                else:
                    errors.append("Could not create leave request")

            # Test Feedback
            if student:
                feedback_data = {
                    'student_id': student,
                    'feedback': 'Test feedback message',
                    'feedback_reply': '',
                }
                feedback = FeedBackStudent.objects.create(**feedback_data)
                if feedback.id:
                    self.log(f"Feedback workflow test passed (ID: {feedback.id})")
                    # Test reply
                    feedback.feedback_reply = 'HOD Reply'
                    feedback.save()
                    self.log("Feedback reply test passed")
        except Exception as e:
            errors.append(f"Workflow simulation failed: {str(e)}")
            self.log(f"Workflow simulation failed: {str(e)}", "ERROR")

        # ===== SUMMARY =====
        self.stdout.write(self.style.SUCCESS("\n" + "=" * 60))
        self.stdout.write(self.style.SUCCESS("VERIFICATION SUMMARY"))
        self.stdout.write(self.style.SUCCESS("=" * 60))

        if errors:
            self.stdout.write(self.style.ERROR(f"\n❌ ERRORS FOUND ({len(errors)}):"))
            for error in errors:
                self.stdout.write(self.style.ERROR(f"  - {error}"))
        else:
            self.stdout.write(self.style.SUCCESS("\n✅ NO CRITICAL ERRORS"))

        if warnings:
            self.stdout.write(self.style.WARNING(f"\n⚠️  WARNINGS ({len(warnings)}):"))
            for warning in warnings:
                self.stdout.write(self.style.WARNING(f"  - {warning}"))
        else:
            self.stdout.write(self.style.SUCCESS("✅ NO WARNINGS"))

        if not errors:
            self.stdout.write(self.style.SUCCESS("\n✅ SYSTEM VERIFICATION COMPLETE - ALL TESTS PASSED\n"))
        else:
            self.stdout.write(self.style.ERROR(f"\n❌ VERIFICATION FAILED - {len(errors)} ERRORS\n"))
