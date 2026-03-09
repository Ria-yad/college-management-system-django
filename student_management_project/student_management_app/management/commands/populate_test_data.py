from django.core.management.base import BaseCommand
from student_management_app.models import (
    CustomUser,
    Staff,
    Staffs,
    Students,
    Courses,
    SessionYearModel,
    Subjects,
)
from datetime import date


class Command(BaseCommand):
    help = "Populate database with test data for testing all roles and workflows"

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting to populate test data..."))

        # Create session
        session, created = SessionYearModel.objects.get_or_create(
            session_start_year=date(2024, 6, 1),
            session_end_year=date(2025, 5, 31),
        )
        self.stdout.write(f"Session: {session}")

        # Create courses
        course1, _ = Courses.objects.get_or_create(course_name="Bachelor of Science in Computer Science")
        course2, _ = Courses.objects.get_or_create(course_name="Bachelor of Arts in English")
        self.stdout.write(f"Courses created: {course1}, {course2}")

        # Create HOD user
        hod_user, created = CustomUser.objects.get_or_create(
            username="hod123",
            defaults={
                "email": "hod@college.edu",
                "first_name": "Admin",
                "last_name": "User",
                "user_type": "HOD",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            hod_user.set_password("password123")
            hod_user.save()
        self.stdout.write(f"HOD User created: {hod_user.username}")

        # Create Staff users
        staff_user1, created = CustomUser.objects.get_or_create(
            username="staff1",
            defaults={
                "email": "staff1@college.edu",
                "first_name": "John",
                "last_name": "Smith",
                "user_type": "STAFF",
            },
        )
        if created:
            staff_user1.set_password("password123")
            staff_user1.save()

        staff_profile1, _ = Staff.objects.get_or_create(
            user=staff_user1,
            defaults={
                "address": "123 Main Street, City",
                "gender": "Male",
            },
        )
        staffs1, _ = Staffs.objects.get_or_create(
            admin=staff_user1,
            defaults={
                "address": "123 Main Street, City",
                "gender": "Male",
            },
        )
        self.stdout.write(f"Staff user created: {staff_user1.username}")

        # Create another Staff user
        staff_user2, created = CustomUser.objects.get_or_create(
            username="staff2",
            defaults={
                "email": "staff2@college.edu",
                "first_name": "Jane",
                "last_name": "Doe",
                "user_type": "STAFF",
            },
        )
        if created:
            staff_user2.set_password("password123")
            staff_user2.save()

        staff_profile2, _ = Staff.objects.get_or_create(
            user=staff_user2,
            defaults={
                "address": "456 Oak Avenue, City",
                "gender": "Female",
            },
        )
        staffs2, _ = Staffs.objects.get_or_create(
            admin=staff_user2,
            defaults={
                "address": "456 Oak Avenue, City",
                "gender": "Female",
            },
        )
        self.stdout.write(f"Staff user created: {staff_user2.username}")

        # Create Student users
        student_user1, created = CustomUser.objects.get_or_create(
            username="student1",
            defaults={
                "email": "student1@college.edu",
                "first_name": "Alice",
                "last_name": "Brown",
                "user_type": "STUDENT",
            },
        )
        if created:
            student_user1.set_password("password123")
            student_user1.save()

        student1, _ = Students.objects.get_or_create(
            admin=student_user1,
            defaults={
                "course_id": course1,
                "session_year_id": session,
                "address": "789 Pine Road, City",
                "gender": "Female",
            },
        )
        self.stdout.write(f"Student user created: {student_user1.username}")

        # Create another Student user
        student_user2, created = CustomUser.objects.get_or_create(
            username="student2",
            defaults={
                "email": "student2@college.edu",
                "first_name": "Bob",
                "last_name": "Wilson",
                "user_type": "STUDENT",
            },
        )
        if created:
            student_user2.set_password("password123")
            student_user2.save()

        student2, _ = Students.objects.get_or_create(
            admin=student_user2,
            defaults={
                "course_id": course1,
                "session_year_id": session,
                "address": "101 Elm Street, City",
                "gender": "Male",
            },
        )
        self.stdout.write(f"Student user created: {student_user2.username}")

        # Create Subjects
        subject1, _ = Subjects.objects.get_or_create(
            subject_name="Data Structures",
            course_id=course1,
            staff_id=staffs1,
        )
        subject2, _ = Subjects.objects.get_or_create(
            subject_name="Web Development",
            course_id=course1,
            staff_id=staffs2,
        )
        self.stdout.write(f"Subjects created: {subject1}, {subject2}")

        self.stdout.write(self.style.SUCCESS("✓ Test data populated successfully!"))
        self.stdout.write(self.style.WARNING("\nTest Credentials:"))
        self.stdout.write("=" * 50)
        self.stdout.write(f"HOD:     username: hod123, password: password123")
        self.stdout.write(f"Staff 1: username: staff1, password: password123")
        self.stdout.write(f"Staff 2: username: staff2, password: password123")
        self.stdout.write(f"Student 1: username: student1, password: password123")
        self.stdout.write(f"Student 2: username: student2, password: password123")
        self.stdout.write("=" * 50)
