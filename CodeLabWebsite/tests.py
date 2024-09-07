from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile, Course, Feedback
from .forms import UserRegisterForm, CourseCreationForm, FeedbackForm

class UserRegistrationTests(TestCase):
    """Test cases for user registration."""

    def test_user_registration(self):
        """Test valid user registration."""
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
            'name': 'Test User',
            'teacher': False,
            'student': True
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)
        self.assertEqual(user.username, 'testuser')

    def test_invalid_registration(self):
        """Test invalid user registration with mismatched passwords."""
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'DifferentPassword123',
            'name': 'Test User',
            'teacher': False,
            'student': True
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_duplicate_username(self):
        """Test user registration with a duplicate username."""
        User.objects.create_user(username='testuser', password='password')
        form_data = {
            'username': 'testuser',
            'email': 'testuser2@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
            'name': 'Test User',
            'teacher': False,
            'student': True
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())

class CourseCreationTests(TestCase):
    """Test cases for course creation."""

    def setUp(self):
        """Set up a teacher user and profile for course creation tests."""
        self.user = User.objects.create_user(username='teacher', password='password')
        self.profile = Profile.objects.create(user=self.user, teacher=True)

    def test_course_creation(self):
        """Test invalid course creation (intentionally set to fail)."""
        self.client.login(username='teacher', password='password')
        form_data = {
            'title': 'Test Course',
            'description': 'A test course description',
            'teacher': self.profile.id
        }
        form = CourseCreationForm(data=form_data)
        self.assertFalse(form.is_valid())  # Intentionally set to False to fail the test
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = self.profile
            course.save()
            self.assertEqual(Course.objects.count(), 1)
            self.assertEqual(course.title, 'Test Course')

    def test_valid_course_creation(self):
        """Test valid course creation."""
        self.client.login(username='teacher', password='password')
        form_data = {
            'title': 'Valid Course',
            'description': 'A valid course description',
            'teacher': self.profile.id
        }
        form = CourseCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        course = form.save(commit=False)
        course.teacher = self.profile
        course.save()
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(course.title, 'Valid Course')

    def test_course_creation_by_non_teacher(self):
        """Test course creation by a non-teacher user."""
        non_teacher_user = User.objects.create_user(username='student', password='password')
        Profile.objects.create(user=non_teacher_user, student=True)
        self.client.login(username='student', password='password')
        form_data = {
            'title': 'Invalid Course',
            'description': 'A course description',
            'teacher': self.profile.id
        }
        form = CourseCreationForm(data=form_data)
        self.assertFalse(form.is_valid())

class FeedbackSubmissionTests(TestCase):
    """Test cases for feedback submission."""

    def setUp(self):
        """Set up users, profiles, and a course for feedback submission tests."""
        self.teacher_user = User.objects.create_user(username='teacher', password='password')
        self.student_user = User.objects.create_user(username='student', password='password')
        self.teacher_profile = Profile.objects.create(user=self.teacher_user, teacher=True)
        self.student_profile = Profile.objects.create(user=self.student_user, student=True)
        self.course = Course.objects.create(title='Test Course', description='A test course', teacher=self.teacher_profile)

    def test_feedback_submission(self):
        """Test invalid feedback submission (intentionally set to fail)."""
        self.client.login(username='student', password='password')
        form_data = {
            'text': 'Great course!',
            'rating': 5
        }
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())  # Intentionally set to False to fail the test
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = self.course
            feedback.student = self.student_profile
            feedback.save()
            self.assertEqual(Feedback.objects.count(), 1)
            self.assertEqual(feedback.text, 'Great course!')
            self.assertEqual(feedback.rating, 5)

    def test_valid_feedback_submission(self):
        """Test valid feedback submission."""
        self.client.login(username='student', password='password')
        form_data = {
            'text': 'Excellent course!',
            'rating': 5
        }
        form = FeedbackForm(data=form_data)
        self.assertTrue(form.is_valid())
        feedback = form.save(commit=False)
        feedback.course = self.course
        feedback.student = self.student_profile
        feedback.save()
        self.assertEqual(Feedback.objects.count(), 1)
        self.assertEqual(feedback.text, 'Excellent course!')
        self.assertEqual(feedback.rating, 5)

    def test_feedback_submission_by_non_student(self):
        """Test feedback submission by a non-student user."""
        self.client.login(username='teacher', password='password')
        form_data = {
            'text': 'Not a student feedback',
            'rating': 3
        }
        form = FeedbackForm(data=form_data)
        self.assertFalse(form.is_valid())