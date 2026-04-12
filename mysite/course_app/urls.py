from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import *

router = SimpleRouter()
router.register(r'user', UserProfileViewSet)
router.register(r'student', StudentViewSet)
router.register(r'language', LanguageViewSet)
router.register(r'my_certificate', CertificateViewSet)
router.register(r'review', ReviewViewSet)
router.register(r'review_like', ReviewLikeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('course/', CourseListAPIView.as_view(), name='course_list'),
    path('course/<int:pk>', CourseDetailAPIView.as_view(), name='course_detail'),
    path('course/create', CourseCreateAPIView.as_view(), name='course_create'),
    path('course/<int:pk>edit', CourseEditAPIView.as_view(), name='course_edit'),
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/<int:pk>', LessonDetailAPIView.as_view(), name='lesson_detail'),
    path('exam/', ExamListAPIView.as_view(), name='exam_list'),
    path('exam/<int:pk>', ExamDetailAPIView.as_view(), name='exam_detail'),
    path('category/', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>', CategoryDetailAPIView.as_view(), name='category_detail'),
    path('subcategory/', SubCategoryListAPIView.as_view(), name='subcategory_list'),
    path('subcategory/<int:pk>', SubCategoryDetailAPIView.as_view(), name='subcategory_detail'),
    path('teacher/', TeacherListAPIView.as_view(), name='teacher_list'),
    path('teacher/<int:pk>', TeacherDetailAPIView.as_view(), name='teacher_detail'),
]