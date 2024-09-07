from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, UserProfileViewSet, FeedbackViewSet, CustomLoginView, StudentViewSet

# Initialize the default router
router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'feedbacks', FeedbackViewSet)
router.register(r'students-and-teachers', StudentViewSet)

# Define URL patterns
urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),  # User registration
    path('login/', CustomLoginView.as_view(), name='login'),  # Custom login view
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Logout view
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),  # Dashboard redirect
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),  # Teacher dashboard
    path('create_course/', views.create_course, name='create_course'),  # Create course
    path('edit_course/<int:course_id>/', views.edit_course, name='edit_course'),  # Edit course
    path('delete_course/<int:course_id>/', views.delete_course, name='delete_course'),  # Delete course
    path('edit_teacher_profile/', views.edit_teacher_profile, name='edit_teacher_profile'),  # Edit teacher profile
    path('search/', views.search_users, name='search_users'),  # Search users
    path('user_profile/<int:user_id>/', views.user_profile, name='user_profile'),  # User profile
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),  # Student dashboard
    path('all_courses/', views.all_courses, name='all_courses'),  # All courses
    path('enroll_course/<int:course_id>/', views.enroll_course, name='enroll_course'),  # Enroll in course
    path('leave_course/<int:course_id>/', views.leave_course, name='leave_course'),  # Leave course
    path('course_content/<int:course_id>/', views.course_content, name='course_content'),  # Course content
    path('course/<int:course_id>/feedback/', views.submit_feedback, name='submit_feedback'),  # Submit feedback
    path('course/<int:course_id>/feedback/view/', views.view_feedback, name='view_feedback'),  # View feedback
    path('course/<int:course_id>/add_material/', views.add_material, name='add_material'),  # Add course material
    path('course/<int:course_id>/manage_students/', views.manage_students, name='manage_students'),  # Manage students
    path('course/<int:course_id>/block_student/<int:student_id>/', views.block_student, name='block_student'),  # Block student
    path('course/<int:course_id>/unblock_student/<int:student_id>/', views.unblock_student, name='unblock_student'),  # Unblock student
    path('course/<int:course_id>/remove_student/<int:student_id>/', views.remove_student, name='remove_student'),  # Remove student
    path('update_status/', views.update_status, name='update_status'),  # Update status
    path('api/', include(router.urls)),  # Include the router URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Serve media files during development