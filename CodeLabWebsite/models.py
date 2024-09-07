from django.db import models  # Import Django's models module
from django.contrib.auth.models import User  # Import User model from Django auth models
from django.core.validators import MaxValueValidator, MinValueValidator  # Import validators for field validation
from django.db.models.signals import post_save  # Import post_save signal
from django.dispatch import receiver  # Import receiver decorator for signal handling

class Profile(models.Model):
    """Model representing a user profile."""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to the User model
    name = models.CharField(max_length=100, null=True, blank=True)  # Optional name field
    teacher = models.BooleanField(default=False)  # Boolean field to indicate if the user is a teacher
    student = models.BooleanField(default=False)  # Boolean field to indicate if the user is a student
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)  # Optional photo field
    status = models.CharField(max_length=255, null=True, blank=True)  # Optional status field
    like_count = models.PositiveIntegerField(default=0)  # Count of likes
    dislike_count = models.PositiveIntegerField(default=0)  # Count of dislikes
    
    def __str__(self):
        """Return the username of the associated user."""
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile instance when a new User is created."""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the Profile instance when the User is saved."""
    instance.profile.save()

class Course(models.Model):
    """Model representing a course."""
    
    title = models.CharField(max_length=200)  # Title of the course
    description = models.TextField()  # Description of the course
    teacher = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='courses_taught')  # Teacher of the course
    materials = models.FileField(upload_to='coursematerials/', null=True, blank=True)  # Optional course materials
    course_image = models.ImageField(upload_to='course_images/', null=True, blank=True)  # Optional course image
    new_material = models.BooleanField(default=False)  # Boolean field to indicate new material
    new_enrollment = models.BooleanField(default=False)  # Boolean field to indicate new enrollment

    def __str__(self):
        """Return the title of the course."""
        return self.title

class CourseMaterial(models.Model):
    """Model representing course materials."""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_materials')  # Associated course
    file = models.FileField(upload_to='course_materials/')  # File field for the material
    description = models.TextField(blank=True, null=True)  # Optional description of the material
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the material was uploaded

    def __str__(self):
        """Return a string representation of the course material."""
        return f"{self.course.title} - {self.file.name}"

class Enrollment(models.Model):
    """Model representing a student's enrollment in a course."""
    
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='enrollments')  # Enrolled student
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolled_students')  # Enrolled course
    date_enrolled = models.DateTimeField(auto_now_add=True)  # Timestamp of when the enrollment occurred
    blocked = models.BooleanField(default=False)  # Boolean field to indicate if the student is blocked

    def __str__(self):
        """Return a string representation of the enrollment."""
        return f"{self.student.user.username} enrolled in {self.course.title}"

class Feedback(models.Model):
    """Model representing feedback for a course."""
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')  # Associated course
    student = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='given_feedbacks')  # Student giving the feedback
    text = models.TextField()  # Feedback text
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # Rating with validation

    def __str__(self):
        """Return a string representation of the feedback."""
        return f"Feedback by {self.student.user.username} for {self.course.title}"

class StatusUpdate(models.Model):
    """Model representing a status update."""
    
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_updates')  # User posting the status update
    content = models.TextField()  # Content of the status update
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of when the status update was created

    def __str__(self):
        """Return a string representation of the status update."""
        return f"{self.user.username}'s status update"

class Student(models.Model):
    """Model representing a student profile."""
    
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='student_profile')  # Associated profile
    enrollment_date = models.DateTimeField(auto_now_add=True)  # Timestamp of when the student enrolled

    def __str__(self):
        """Return the username of the associated user."""
        return self.profile.user.username