from django import forms  # Import Django forms module
from django.contrib.auth.forms import UserCreationForm  # Import UserCreationForm from Django auth forms
from django.contrib.auth.models import User  # Import User model from Django auth models
from .models import Course, Profile, StatusUpdate, Feedback, CourseMaterial  # Import models from the local app
from django.core.exceptions import ValidationError  # Import ValidationError for custom validation
from django.template.defaultfilters import filesizeformat  # Import filesizeformat for file size formatting

class FeedbackForm(forms.ModelForm):
    """Form for submitting feedback with a rating."""
    
    # Define rating choices as a list of tuples
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    # Define rating field with choices and a select widget
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select)

    class Meta:
        model = Feedback  # Specify the model to use
        fields = ['text', 'rating']  # Specify the fields to include in the form

    def clean_rating(self):
        """Ensure the rating is between 1 and 5."""
        rating = int(self.cleaned_data.get('rating'))
        if rating < 1 or rating > 5:
            raise ValidationError('Rating must be between 1 and 5.')
        return rating

class UserRegisterForm(UserCreationForm):
    """Form for registering a new user with additional fields."""
    
    email = forms.EmailField(required=True, help_text='Enter a valid email address.')
    name = forms.CharField(required=True, max_length=100, help_text='Enter your full name.')
    teacher = forms.BooleanField(required=False, help_text='Check if you are registering as a teacher.')
    student = forms.BooleanField(required=False, help_text='Check if you are registering as a student.')

    class Meta:
        model = User  # Specify the model to use
        fields = ['username', 'email', 'password1', 'password2', 'name', 'teacher', 'student']  # Specify the fields to include in the form

    def __init__(self, *args, **kwargs):
        """Initialize the form with custom help texts and labels."""
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Enter a unique username.'
        self.fields['password1'].help_text = 'Enter a strong password.'
        self.fields['password2'].help_text = 'Re-enter the password for confirmation.'
        self.fields['name'].label = 'Name'
        self.fields['teacher'].label = 'Teacher'
        self.fields['student'].label = 'Student'

    def clean(self):
        """Ensure that either teacher or student is selected, but not both."""
        cleaned_data = super().clean()
        teacher = cleaned_data.get('teacher')
        student = cleaned_data.get('student')
        if not teacher and not student:
            raise forms.ValidationError('You must select either Teacher or Student.')
        if teacher and student:
            raise forms.ValidationError('You cannot select both Teacher and Student.')
        return cleaned_data
    
class CourseCreationForm(forms.ModelForm):
    """Form for creating a new course."""
    
    class Meta:
        model = Course  # Specify the model to use
        fields = ['title', 'description', 'course_image', 'materials']  # Specify the fields to include in the form
        
    course_image = forms.ImageField(required=False, label='Course Image')  # Define an optional image field

class TeacherProfileForm(forms.ModelForm):
    """Form for updating a teacher's profile."""
    
    username = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    photo = forms.ImageField(widget=forms.FileInput, required=False)
    delete_photo = forms.BooleanField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = Profile  # Specify the model to use
        fields = ['username', 'email', 'name', 'photo', 'delete_photo']  # Specify the fields to include in the form

    def __init__(self, *args, **kwargs):
        """Initialize the form with initial values and custom widget attributes."""
        super(TeacherProfileForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username
            self.fields['email'].initial = self.instance.user.email
        if self.instance and self.instance.photo:
            try:
                self.fields['photo'].widget.attrs.update({
                    'data-initial-file': self.instance.photo.url,
                    'data-initial-file-name': self.instance.photo.name,
                    'data-initial-file-size': filesizeformat(self.instance.photo.size)
                })
            except FileNotFoundError:
                self.instance.photo = None

    def clean_username(self):
        """Ensure the username is unique."""
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exclude(pk=self.instance.user.pk).exists():
            raise ValidationError('This username is already taken.')
        return username

    def save(self, commit=True):
        """Save the profile and update the related user model."""
        profile = super(TeacherProfileForm, self).save(commit=False)
        if self.cleaned_data.get('delete_photo'):
            profile.photo.delete()
            profile.photo = None
        if commit:
            user = profile.user
            user.username = self.cleaned_data.get('username', user.username)
            user.email = self.cleaned_data.get('email', user.email)
            user.save()
            profile.save()
        return profile
    
class CourseMaterialForm(forms.ModelForm):
    """Form for uploading course materials."""
    
    class Meta:
        model = CourseMaterial  # Specify the model to use
        fields = ['file', 'description']  # Specify the fields to include in the form

class StatusUpdateForm(forms.ModelForm):
    """Form for submitting a status update."""
    
    class Meta:
        model = StatusUpdate  # Specify the model to use
        fields = ['content']  # Specify the fields to include in the form