# Django College Management System (Mini ERP)

A comprehensive Django-based ERP system for managing college operations with role-based access for HOD, STAFF, and STUDENTS.

## Features

### 🎯 Core Modules

#### 1. **Authentication & Authorization**
- Role-based login (HOD, STAFF, STUDENT)
- Custom user model with user types
- Protected views with role-based decorators
- Automatic role-based dashboard redirect

#### 2. **Attendance Management**
- **Staff**: Mark attendance by subject, date, and session
- **Student**: View attendance reports and percentage
- **HOD**: View departmental attendance reports

#### 3. **Leave Management**
- **Staff & Students**: Apply for leave with date and reason
- **HOD**: Review and approve/reject leave requests
- Leave status tracking (Pending, Approved, Rejected)

#### 4. **Feedback System**
- **Staff & Students**: Submit feedback to HOD
- **HOD**: View feedback and send replies

#### 5. **Staff Management**
- **HOD**: Add, edit, list, and delete staff members
- Staff profile with contact information

#### 6. **Admin Panel**
- Full Django admin with searchable, filterable models
- List displays for all entities
- Proper permissions and access control

### 🎨 User Interface

- **Modern, responsive design** with sidebar navigation
- **Real-time updates** with AJAX for attendance marking
- **Flash messages** for user feedback
- **Professional styling** with color-coded badges
- **Mobile-responsive** layout
- **Smooth animations** and hover effects

## System Requirements

- Python 3.10+
- Django 6.0.2
- SQLite3 (included with Python)

## Installation & Setup

### 1. **Clone/Navigate to Project**
```bash
cd C:\Users\saini\Desktop\college_Management_System\student_management_project
```

### 2. **Create & Activate Virtual Environment** (if not already done)
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac
```

### 3. **Install Dependencies**
```bash
pip install django==6.0.2
```

### 4. **Run Migrations**
```bash
python manage.py migrate
```

### 5. **Populate Test Data**
```bash
python manage.py populate_test_data
```

This creates:
- **HOD Account**: username `hod123`, password `password123`
- **Staff Accounts**: `staff1`, `staff2` (password: `password123`)
- **Student Accounts**: `student1`, `student2` (password: `password123`)
- **Test Data**: Courses, Sessions, Subjects

### 6. **Start Development Server**
```bash
python manage.py runserver
```

Server runs on `http://localhost:8000`

---

## Testing Guide

### 🔐 **1. Login & Authentication**

1. Navigate to `http://localhost:8000/`
2. Login with any test credentials:
   - HOD: `hod123` / `password123`
   - Staff: `staff1` / `password123`
   - Student: `student1` / `password123`
3. Verify you're redirected to the correct dashboard

### 👨‍💼 **2. HOD Dashboard**

**URL**: `http://localhost:8000/hod/dashboard/`

**What to Test:**
- [ ] Dashboard displays statistics (total staff, students, courses, attendance)
- [ ] Sidebar shows all HOD links
- [ ] Top bar shows logged-in user name
- [ ] "Quick Actions" buttons work

**Features to Access:**
- [ ] **Staff Management**: `/hod/staff/` - Add, edit, list staff
- [ ] **Attendance Reports**: `/hod/attendance/view/` - View attendance by subject/date
- [ ] **Leave Requests**: `/hod/student/leave/` and `/hod/staff/leave/` - Approve/reject leaves
- [ ] **Feedback**: `/hod/student/feedback/` and `/hod/staff/feedback/` - View and reply to feedback

### 👨‍🏫 **3. Staff Workflow**

**URL**: `http://localhost:8000/staff/dashboard/`

**Test Attendance Workflow:**
1. Go to Dashboard → "Take Attendance"
2. Select Subject: "Data Structures"
3. Select Session: "2024-06-01 To 2025-05-31"
4. Select Date: Any date
5. Click "Fetch Students"
6. Check/uncheck students as Present/Absent
7. Click "Save Attendance"
8. ✅ Should see success message

**Test Update Attendance:**
1. Go to Dashboard → "Update Attendance"
2. Repeat steps 2-5 above
3. Click "Get Attendance" to view previous entries
4. Modify attendance and click "Update"
5. ✅ Should see success message

**Test Leave Application:**
1. Go to Dashboard → "Apply Leave"
2. Select a date and enter reason
3. Click "Submit Request"
4. View in "Leave Status" to see approval status

**Test Feedback:**
1. Go to Dashboard → "Feedback"
2. Submit a message to HOD
3. View in the list to see HOD's reply (when HOD replies)

### 👨‍🎓 **4. Student Workflow**

**URL**: `http://localhost:8000/student/dashboard/`

**Test Attendance View:**
1. Go to Dashboard → "My Attendance"
2. Select Subject: "Data Structures"
3. Select Date Range: Any range
4. Click "View Report"
5. ✅ Should see attendance record if staff marked it

**Test Leave & Feedback:**
Same as Staff (see above)

**Test Profile:**
1. Go to Dashboard → "My Profile"
2. ✅ Should see course, session, gender, address information

### 👨‍💻 **5. Admin Panel** 

**URL**: `http://localhost:8000/admin/`

**Login with HOD credentials**: `hod123` / `password123`

**Test All Models:**
- [ ] CustomUser - Search by username, filter by user_type
- [ ] Courses - View all courses
- [ ] Sessions - View all sessions/batches
- [ ] Subjects - Search and filter by course/staff
- [ ] Students - Filter by course/session, search by name
- [ ] Staff - View staff profiles
- [ ] Attendance - View attendance records
- [ ] Leave Reports - View leave requests with status
- [ ] Feedback - View feedback and reply status

---

## Project Structure

```
student_management_project/
├── db.sqlite3                          # Database
├── manage.py                           # Django management script
├── static/
│   └── css/style.css                  # Main styling
├── templates/
│   ├── base.html                      # Base layout with navbar/sidebar
│   └── home.html                      # Home template
├── student_management_app/
│   ├── migrations/                    # Database migrations
│   ├── management/
│   │   └── commands/
│   │       └── populate_test_data.py  # Test data command
│   ├── templates/
│   │   ├── hod_template/              # HOD view templates
│   │   ├── hod_templates/             # HOD management templates
│   │   ├── staff_template/            # Staff view templates
│   │   ├── staff_templates/           # Staff management templates
│   │   ├── student_template/          # Student view templates
│   │   ├── student_templates/         # Student management templates
│   │   └── student_management_app/    # Common templates
│   ├── admin.py                       # Admin configuration
│   ├── apps.py                        # App config
│   ├── forms.py                       # Form definitions
│   ├── models.py                      # Database models
│   ├── role_helpers.py                # Role-based decorators
│   ├── urls.py                        # URL routing
│   ├── views.py                       # Common views
│   ├── HodViews.py                    # HOD-specific views
│   ├── StaffViews.py                  # Staff-specific views
│   └── StudentViews.py                # Student-specific views
└── student_management_project/
    ├── settings.py                    # Django settings
    ├── urls.py                        # URL configuration
    ├── asgi.py                        # ASGI config
    └── wsgi.py                        # WSGI config
```

## Database Models

### Core User Model
- **CustomUser** (extends Django User)
  - Roles: HOD, STAFF, STUDENT
  - Fields: username, email, first_name, last_name, user_type

### Academic Models
- **Courses** - Course/Program information
- **SessionYearModel** - Academic session/batch
- **Subjects** - Courses taught by staff
- **Staff** - Staff member profiles (modern)
- **Staffs** - Staff member profiles (legacy)
- **Students** - Student profiles

### Management Models
- **Attendance** - Attendance records by subject/date
- **AttendanceReport** - Individual student attendance
- **LeaveReportStudent** - Student leave requests
- **LeaveReportStaff** - Staff leave requests
- **FeedBackStudent** - Student feedback to HOD
- **FeedBackStaffs** - Staff feedback to HOD

## Key Features Implementation

### Role-Based Access Control
```python
@hod_required          # Only HOD can access
@staff_required        # Only STAFF can access
@student_required      # Only STUDENT can access
```

### AJAX Attendance Marking
- Fetch students by subject/session
- Mark presence/absence with checkboxes
- Save attendance data via JSON POST
- Update existing attendance records

### Messages Framework
- Success messages on form submission
- Error handling with user-friendly messages
- Flash messages displayed in UI

### Form Handling
- Staff creation with validation
- Profile updates with email uniqueness check
- Leave and feedback submission

---

## Common Issues & Solutions

### **Issue**: "TemplateDoesNotExist" error
**Solution**: Verify all template files exist in the correct directories

### **Issue**: CSRF token errors
**Solution**: Ensure `{% csrf_token %}` is in all POST forms

### **Issue**: Static files not loading
**Solution**: Run `python manage.py collectstatic`

### **Issue**: 403 Forbidden or redirected to login
**Solution**: Ensure you have the correct role and are logged in with the right user type

---

## Production Considerations

⚠️ **Before deploying to production:**

1. Set `DEBUG = False` in settings.py
2. Generate a strong `SECRET_KEY`
3. Configure `ALLOWED_HOSTS`
4. Use a production database (PostgreSQL/MySQL)
5. Set up proper static/media file handling (S3, etc.)
6. Enable HTTPS
7. Configure email backend for notifications
8. Set up proper logging

---

## Support & Documentation

For Django documentation: https://docs.djangoproject.com/

---

## License

This project is provided as-is for educational purposes.

---

**Last Updated**: February 23, 2026
**Django Version**: 6.0.2
**Python Version**: 3.10+
