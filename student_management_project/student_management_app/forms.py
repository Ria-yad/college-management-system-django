from django import forms
from django.db import transaction

from .models import CustomUser, Staff, Staffs, Students, Courses, SessionYearModel, Subjects


class StaffCreateForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    address = forms.CharField(widget=forms.Textarea, required=False)
    gender = forms.ChoiceField(choices=Staff.GENDER_CHOICES, required=False)

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    @transaction.atomic
    def save(self):
        user = CustomUser(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            user_type="STAFF",
        )
        user.set_password(self.cleaned_data["password"])
        user.save()

        Staff.objects.create(
            user=user,
            address=self.cleaned_data.get("address", ""),
            gender=self.cleaned_data.get("gender", ""),
        )
        Staffs.objects.create(
            admin=user,
            address=self.cleaned_data.get("address", ""),
            gender=self.cleaned_data.get("gender", ""),
        )

        return user


class StaffUpdateForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    address = forms.CharField(widget=forms.Textarea, required=False)
    gender = forms.ChoiceField(choices=Staff.GENDER_CHOICES, required=False)

    def __init__(self, *args, staff=None, **kwargs):
        self.staff = staff
        super().__init__(*args, **kwargs)

        if self.staff and not self.is_bound:
            self.fields["username"].initial = self.staff.user.username
            self.fields["email"].initial = self.staff.user.email
            self.fields["first_name"].initial = self.staff.user.first_name
            self.fields["last_name"].initial = self.staff.user.last_name
            self.fields["address"].initial = self.staff.address
            self.fields["gender"].initial = self.staff.gender

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        qs = CustomUser.objects.filter(username=username)
        if self.staff:
            qs = qs.exclude(pk=self.staff.user.pk)
        if qs.exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        qs = CustomUser.objects.filter(email=email)
        if self.staff:
            qs = qs.exclude(pk=self.staff.user.pk)
        if qs.exists():
            raise forms.ValidationError("Email already exists.")
        return email

    @transaction.atomic
    def save(self):
        user = self.staff.user
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.user_type = "STAFF"
        user.save()

        self.staff.address = self.cleaned_data.get("address", "")
        self.staff.gender = self.cleaned_data.get("gender", "")
        self.staff.save()

        legacy_staff, _ = Staffs.objects.get_or_create(admin=user)
        legacy_staff.address = self.staff.address
        legacy_staff.gender = self.staff.gender
        legacy_staff.save()

        return self.staff


class StaffProfileUpdateForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea, required=False)
    gender = forms.ChoiceField(choices=Staff.GENDER_CHOICES, required=False)

    def __init__(self, *args, user=None, staff=None, **kwargs):
        self.user = user
        self.staff = staff
        super().__init__(*args, **kwargs)

        if self.user and not self.is_bound:
            self.fields["first_name"].initial = self.user.first_name
            self.fields["last_name"].initial = self.user.last_name
            self.fields["email"].initial = self.user.email
            if self.staff:
                self.fields["address"].initial = self.staff.address
                self.fields["gender"].initial = self.staff.gender

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        qs = CustomUser.objects.filter(email=email)
        if self.user:
            qs = qs.exclude(pk=self.user.pk)
        if qs.exists():
            raise forms.ValidationError("Email already exists.")
        return email

    @transaction.atomic
    def save(self):
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.email = self.cleaned_data["email"]
        self.user.user_type = "STAFF"
        self.user.save()

        staff_profile, _ = Staff.objects.get_or_create(user=self.user)
        staff_profile.address = self.cleaned_data.get("address", "")
        staff_profile.gender = self.cleaned_data.get("gender", "")
        staff_profile.save()

        legacy_staff, _ = Staffs.objects.get_or_create(admin=self.user)
        legacy_staff.address = staff_profile.address
        legacy_staff.gender = staff_profile.gender
        legacy_staff.save()

        return staff_profile


class StudentLeaveApplyForm(forms.Form):
    leave_reason = forms.CharField(widget=forms.Textarea, label="Leave Reason")

class StudentCreateForm(forms.Form):
    """Form to create a new student user and profile"""
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    address = forms.CharField(widget=forms.Textarea, required=False)
    gender = forms.ChoiceField(choices=Students.GENDER_CHOICES, required=False)
    course_id = forms.ModelChoiceField(queryset=Courses.objects.all())
    session_year_id = forms.ModelChoiceField(queryset=SessionYearModel.objects.all())

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email

    @transaction.atomic
    def save(self):
        user = CustomUser(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            user_type="STUDENT",
        )
        user.set_password(self.cleaned_data["password"])
        user.save()

        student = Students.objects.create(
            admin=user,
            address=self.cleaned_data.get("address", ""),
            gender=self.cleaned_data.get("gender", ""),
            course_id=self.cleaned_data["course_id"],
            session_year_id=self.cleaned_data["session_year_id"],
        )
        return user


class StudentUpdateForm(forms.Form):
    """Form to update existing student data"""
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    address = forms.CharField(widget=forms.Textarea, required=False)
    gender = forms.ChoiceField(choices=Students.GENDER_CHOICES, required=False)
    course_id = forms.ModelChoiceField(queryset=Courses.objects.all())
    session_year_id = forms.ModelChoiceField(queryset=SessionYearModel.objects.all())

    def __init__(self, *args, student=None, **kwargs):
        self.student = student
        super().__init__(*args, **kwargs)
        if self.student and not self.is_bound:
            self.fields["username"].initial = self.student.admin.username
            self.fields["email"].initial = self.student.admin.email
            self.fields["first_name"].initial = self.student.admin.first_name
            self.fields["last_name"].initial = self.student.admin.last_name
            self.fields["address"].initial = self.student.address
            self.fields["gender"].initial = self.student.gender
            self.fields["course_id"].initial = self.student.course_id
            self.fields["session_year_id"].initial = self.student.session_year_id

    def clean_username(self):
        username = self.cleaned_data["username"].strip()
        qs = CustomUser.objects.filter(username=username)
        if self.student:
            qs = qs.exclude(pk=self.student.admin.pk)
        if qs.exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        qs = CustomUser.objects.filter(email=email)
        if self.student:
            qs = qs.exclude(pk=self.student.admin.pk)
        if qs.exists():
            raise forms.ValidationError("Email already exists.")
        return email

    @transaction.atomic
    def save(self):
        user = self.student.admin
        user.username = self.cleaned_data["username"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()

        self.student.address = self.cleaned_data.get("address", "")
        self.student.gender = self.cleaned_data.get("gender", "")
        self.student.course_id = self.cleaned_data["course_id"]
        self.student.session_year_id = self.cleaned_data["session_year_id"]
        self.student.save()
        return self.student


class CourseForm(forms.ModelForm):
    """Form for Course CRUD"""
    class Meta:
        model = Courses
        fields = ["course_name"]
        widgets = {
            "course_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter course name"}),
        }


class SessionForm(forms.ModelForm):
    """Form for Session/Batch CRUD"""
    class Meta:
        model = SessionYearModel
        fields = ["session_start_year", "session_end_year"]
        widgets = {
            "session_start_year": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "session_end_year": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }


class SubjectForm(forms.ModelForm):
    """Form for Subject CRUD"""
    class Meta:
        model = Subjects
        fields = ["subject_name", "course_id", "staff_id"]
        widgets = {
            "subject_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter subject name"}),
            "course_id": forms.Select(attrs={"class": "form-control"}),
            "staff_id": forms.Select(attrs={"class": "form-control"}),
        }