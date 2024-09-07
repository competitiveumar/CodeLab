# Import necessary modules from Django and other libraries
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import UserRegisterForm
from .forms import CourseCreationForm, TeacherProfileForm, FeedbackForm, CourseMaterialForm, StatusUpdateForm
from .models import Profile, Course, Enrollment, Feedback, CourseMaterial, StatusUpdate, Student
from .serializers import ProfileSerializer, CourseSerializer, EnrollmentSerializer, FeedbackSerializer, CourseMaterialSerializer, StatusUpdateSerializer, StudentSerializer
from rest_framework import viewsets
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
import json
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    """
    Render the home page with the latest status updates and user status.
    """
    latest_status_updates = StatusUpdate.objects.order_by('-created_at')[:5]
    other_user_status = None
    if request.user.is_authenticated:
        other_user_status = 'Teacher' if request.user.profile.teacher else 'Student' if request.user.profile.student else 'None'
    return render(request, 'CodeLabWebsite/home.html', {
        'latest_status_updates': latest_status_updates,
        'other_user_status': other_user_status
    })

@login_required
def update_status(request):
    """
    Update the status of a profile based on the action specified in the request.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        profile_id = data.get('profile_id')
        profile = get_object_or_404(Profile, id=profile_id)

        if action == 'like':
            profile.like_count += 1
            profile.save()
            return JsonResponse({'success': True, 'like_count': profile.like_count})
        elif action == 'dislike':
            profile.dislike_count += 1
            profile.save()
            return JsonResponse({'success': True, 'dislike_count': profile.dislike_count})
        elif action == 'reset':
            profile.like_count = 0
            profile.dislike_count = 0
            profile.save()
            return JsonResponse({'success': True, 'like_count': profile.like_count, 'dislike_count': profile.dislike_count})
        elif action == 'update_status':
            new_status = data.get('new_status')
            profile.status = new_status
            profile.save()
            return JsonResponse({'success': True, 'new_status': profile.status})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid action.'})
    return JsonResponse({'success': False, 'error': 'Invalid request method.'})

@login_required
def manage_students(request, course_id):
    """
    Render the page for managing students in a course.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user.profile)
    enrollments = Enrollment.objects.filter(course=course)
    return render(request, 'CodeLabWebsite/manage_students.html', {'course': course, 'enrollments': enrollments})

@login_required
def block_student(request, course_id, student_id):
    """
    Block a student from a course.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user.profile)
    enrollment = get_object_or_404(Enrollment, course=course, student_id=student_id)
    enrollment.blocked = True
    enrollment.save()
    messages.success(request, f'Student {enrollment.student.user.username} has been blocked.')
    return redirect('manage_students', course_id=course_id)
    
@login_required
def unblock_student(request, course_id, student_id):
    """
    Unblock a student from a course.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user.profile)
    enrollment = get_object_or_404(Enrollment, course=course, student_id=student_id)
    enrollment.blocked = False
    enrollment.save()
    messages.success(request, f'Student {enrollment.student.user.username} has been unblocked.')
    return redirect('manage_students', course_id=course_id)

@login_required
def remove_student(request, course_id, student_id):
    """
    Remove a student from a course.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user.profile)
    enrollment = get_object_or_404(Enrollment, course=course, student_id=student_id)
    enrollment.delete()
    messages.success(request, f'Student {enrollment.student.user.username} has been removed from the course.')
    return redirect('manage_students', course_id=course_id)

@login_required
def submit_feedback(request, course_id):
    """
    Submit feedback for a course.
    """
    course = get_object_or_404(Course, id=course_id)
    student = request.user.profile

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.student = student
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('course_content', course_id=course.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FeedbackForm()

    return render(request, 'CodeLabWebsite/submit_feedback.html', {'form': form, 'course': course})

@login_required
def view_feedback(request, course_id):
    """
    View feedback for a course.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user.profile)
    feedbacks = Feedback.objects.filter(course=course)
    return render(request, 'CodeLabWebsite/view_feedback.html', {'course': course, 'feedbacks': feedbacks})

@login_required
def add_material(request, course_id):
    """
    Add new material to a course.
    """
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            course.new_material = True  # Set new_material to True
            course.save()
            messages.success(request, 'Material added successfully!')
            return redirect('course_content', course_id=course.id)
    else:
        form = CourseMaterialForm()
    return render(request, 'CodeLabWebsite/add_material.html', {'form': form, 'course': course})

@login_required
def course_content(request, course_id):
    """
    Render the course content page.
    """
    course = get_object_or_404(Course, id=course_id)
    enrollment = get_object_or_404(Enrollment, course=course, student=request.user.profile)

    if enrollment.blocked:
        messages.error(request, 'You are blocked from viewing the content. Please contact the teacher.')
        return redirect('student_dashboard')

    if course.new_material:
        # Handle new material logic here
        pass

    return render(request, 'CodeLabWebsite/course_content.html', {'course': course})

class CustomLoginView(LoginView):
    """
    Custom login view with additional checks.
    """
    template_name = 'CodeLabWebsite/login.html'
    form_class = AuthenticationForm

    def form_valid(self, form):
        """
        Handle valid form submission.
        """
        user = form.get_user()
        if not hasattr(user, 'profile'):
            messages.error(self.request, 'User does not exist.')
            return self.form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Handle invalid form submission.
        """
        username = form.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            messages.error(self.request, 'User does not exist.')
        return super().form_invalid(form)

def home(request):
    """
    Render the home page (redundant function, should be removed or merged).
    """
    latest_status_updates = StatusUpdate.objects.order_by('-created_at')[:5]
    return render(request, 'CodeLabWebsite/home.html', {'latest_status_updates': latest_status_updates})

def register(request):
    """
    Handle user registration.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            name = form.cleaned_data.get('name')
            teacher = form.cleaned_data.get('teacher')
            student = form.cleaned_data.get('student')
            Profile.objects.update_or_create(user=user, defaults={'name': name, 'teacher': teacher, 'student': student})
            messages.success(request, f'Account created for {user.username}! You can now log in.')
            return redirect('login')
        else:
            print(form.errors)  # Log form errors to the console
    else:
        form = UserRegisterForm()
    return render(request, 'CodeLabWebsite/register.html', {'form': form})

@login_required
def dashboard_redirect(request):
    """
    Redirect to the appropriate dashboard based on user type.
    """
    if hasattr(request.user, 'profile'):
        if request.user.profile.teacher:  
            return redirect('teacher_dashboard')
        else:
            return redirect('student_dashboard')
    return redirect('home')

@login_required
def teacher_dashboard(request):
    """
    Render the teacher dashboard with course information and new enrollment notifications.
    """
    if not hasattr(request.user, 'profile') or not request.user.profile.teacher:  
        return redirect('home')
    
    courses = Course.objects.filter(teacher=request.user.profile).annotate(
        enrolled_students_count=Count('enrolled_students')
    )
    
    new_enrollment_found = any(course.new_enrollment for course in courses)
    
    # Set session variable to show notification each time a new student enrolls
    if new_enrollment_found:
        request.session['show_notification'] = True
        for course in courses:
            if course.new_enrollment:
                course.new_enrollment = False
                course.save()
    else:
        request.session['show_notification'] = False
    
    return render(request, 'CodeLabWebsite/teacher_dashboard.html', {
        'courses': courses,
        'new_enrollment_found': new_enrollment_found,
        'show_notification': request.session.pop('show_notification', False),
    })

@login_required
def student_dashboard(request):
    """
    Render the student dashboard with enrolled courses and new material alerts.
    """
    enrolled_courses = Enrollment.objects.filter(student=request.user.profile)
    
    # Check if there is new material in any of the enrolled courses
    new_material_found = any(item.course.new_material for item in enrolled_courses)
    
    # Set session variable if new material is found
    if new_material_found:
        request.session['new_material_alert'] = True
        for item in enrolled_courses:
            if item.course.new_material:
                item.course.new_material = False
                item.course.save()
    else:
        request.session['new_material_alert'] = False
    
    return render(request, 'CodeLabWebsite/student_dashboard.html', {
        'enrolled_courses': enrolled_courses,
        'new_material_alert': request.session.pop('new_material_alert', False),
    })

@login_required
def search_users(request):
    """
    Search for users based on type and query.
    """
    user_type = request.GET.get('type')
    search_query = request.GET.get('q', '')
    profiles = Profile.objects.all()

    if user_type == 'student':
        profiles = profiles.filter(teacher=False)
    elif user_type == 'teacher':
        profiles = profiles.filter(teacher=True)

    if search_query:
        profiles = profiles.filter(user__username__icontains=search_query)

    return render(request, 'CodeLabWebsite/teacher_user-search.html', {'profiles': profiles, 'search_query': search_query})

@login_required
def user_profile(request, user_id):
    """
    Display the profile of a specific user, showing courses they are associated with.
    """
    profile = get_object_or_404(Profile, user__id=user_id)
    courses = []
    if profile.teacher:  
        courses = Course.objects.filter(teacher=profile)
    else:
        enrollments = Enrollment.objects.filter(student=profile)
        courses = [enrollment.course for enrollment in enrollments]

    return render(request, 'CodeLabWebsite/teacher_user-search_user-profile.html', {'profile': profile, 'courses': courses})

@login_required
def edit_teacher_profile(request):
    """
    Allow teachers to edit their profile.
    """
    profile = request.user.profile
    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
                profile.photo.name = request.FILES['photo'].name
            if request.POST.get('remove_image') == 'True':
                profile.photo.delete()
                profile.photo = None
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('teacher_dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherProfileForm(instance=profile)
    return render(request, 'CodeLabWebsite/teacher_private-profile.html', {'form': form})

def home(request):
    """
    Render the home page (redundant function, should be removed or merged).
    """
    latest_status_updates = StatusUpdate.objects.order_by('-created_at')[:5]
    return render(request, 'CodeLabWebsite/home.html', {'latest_status_updates': latest_status_updates})

@login_required
def all_courses(request):
    """
    Display all courses and highlight those the student is enrolled in.
    """
    courses = Course.objects.select_related('teacher').all()
    enrolled_courses = Enrollment.objects.filter(student=request.user.profile).values_list('course_id', flat=True)
    context = {
        'courses': courses,
        'enrolled_course_ids': list(enrolled_courses),
    }
    return render(request, 'CodeLabWebsite/student_courses.html', context)

@login_required
def enroll_course(request, course_id):
    """
    Enroll a student in a course.
    """
    if request.method == 'POST':
        course = Course.objects.get(id=course_id)
        Enrollment.objects.get_or_create(student=request.user.profile, course=course)
        course.new_enrollment = True  
        course.save()
        messages.success(request, 'Successfully enrolled in the course!')
    return redirect('all_courses')

@login_required
def leave_course(request, course_id):
    """
    Allow a student to leave a course.
    """
    if request.method == 'POST':
        course = Course.objects.get(id=course_id)
        enrollment = Enrollment.objects.filter(student=request.user.profile, course=course)
        if enrollment.exists():
            enrollment.delete()
            messages.success(request, 'You have left the course.')
    return redirect('all_courses')

@login_required
def create_course(request):
    """
    Create a new course.
    """
    if request.method == 'POST':
        form = CourseCreationForm(request.POST, request.FILES)  # Include request.FILES
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = request.user.profile
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('teacher_dashboard')
    else:
        form = CourseCreationForm()
    return render(request, 'CodeLabWebsite/teacher_create-course.html', {'form': form})

@login_required
def edit_course(request, course_id):
    """
    Edit an existing course.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user.profile)
    if request.method == 'POST':
        form = CourseCreationForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            if 'materials' in request.FILES:
                course.new_material = True 
            form.save()
            messages.success(request, 'Course updated successfully.')
            return redirect('teacher_dashboard')
    else:
        form = CourseCreationForm(instance=course)
    return render(request, 'CodeLabWebsite/teacher_edit-course.html', {'form': form, 'course': course})

@login_required
def delete_course(request, course_id):
    """
    Delete a course.
    """
    course = get_object_or_404(Course, id=course_id, teacher=request.user.profile)
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('teacher_dashboard')
    return redirect('teacher_dashboard')

@login_required
def course_content(request, course_id):
    """
    Render the course content page (duplicated function, should be removed or merged).
    """
    course = get_object_or_404(Course, id=course_id)
    enrollment = get_object_or_404(Enrollment, course=course, student=request.user.profile)

    if enrollment.blocked:
        messages.error(request, 'You are blocked from viewing the content. Please contact the teacher.')
        return redirect('student_dashboard')

    return render(request, 'CodeLabWebsite/course_content.html', {'course': course})

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    API viewset for handling user profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class CourseViewSet(viewsets.ModelViewSet):
    """
    API viewset for handling courses.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    """
    API viewset for handling enrollments.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class FeedbackViewSet(viewsets.ModelViewSet):
    """
    API viewset for handling feedback.
    """
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

class CourseMaterialViewSet(viewsets.ModelViewSet):
    """
    API viewset for handling course materials.
    """
    queryset = CourseMaterial.objects.all()
    serializer_class = CourseMaterialSerializer

class StatusUpdateViewSet(viewsets.ModelViewSet):
    """
    API viewset for handling status updates.
    """
    queryset = StatusUpdate.objects.all()
    serializer_class = StatusUpdateSerializer

class StudentViewSet(viewsets.ModelViewSet):
    """
    API viewset for handling students.
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_serializer_context(self):
        """
        Provide additional context for the student serializer.
        """
        context = super().get_serializer_context()
        context['title'] = 'Students and Teachers'
        return context
