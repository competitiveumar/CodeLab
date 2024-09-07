from rest_framework import serializers
from .models import Profile, Course, Enrollment, Feedback, CourseMaterial, StatusUpdate, Student

class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for the Profile model."""
    class Meta:
        model = Profile
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    """Serializer for the Course model."""
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for the Enrollment model."""
    class Meta:
        model = Enrollment
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    """Serializer for the Feedback model."""
    class Meta:
        model = Feedback
        fields = '__all__'

class CourseMaterialSerializer(serializers.ModelSerializer):
    """Serializer for the CourseMaterial model."""
    class Meta:
        model = CourseMaterial
        fields = '__all__'

class StatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for the StatusUpdate model."""
    class Meta:
        model = StatusUpdate
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    """Serializer for the Student model."""
    class Meta:
        model = Student
        fields = '__all__'