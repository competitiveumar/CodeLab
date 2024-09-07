from rest_framework.routers import DefaultRouter  # Import DefaultRouter from Django REST framework
from .views import CourseViewSet  # Import CourseViewSet from the local views module

# Create a router object
router = DefaultRouter()

# Register the CourseViewSet with the router
router.register(r'courses', CourseViewSet)

# Define the URL patterns using the router's URLs
urlpatterns = router.urls