from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name','username', 'email', 'password','age' )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']

class TeacherNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name']

class NetworkTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkTeacher
        fields = ['network_name', 'network_url']

class TeacherInfoSerializer(serializers.ModelSerializer):
    networks_teacher = NetworkTeacherSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'first_name', 'last_name', 'bio', 'networks_teacher']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentNameSerializer(serializers.ModelSerializer):
    user = UserProfileNameSerializer()
    class Meta:
        model = Student
        fields = ['user']


class NetworkStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkStudent
        fields = '__all__'

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class CategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']

class SubCategorySerializer(serializers.ModelSerializer):
    category = CategoryNameSerializer()
    class Meta:
        model = SubCategory
        fields = ['category', 'subcategory_name']

class SubCategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = [ 'id', 'subcategory_name']

class CategoryDetailSerializer(serializers.ModelSerializer):
    category_sub = SubCategoryListSerializer(read_only=True, many=True)
    class Meta:
        model = Category
        fields = ['category_name', 'category_sub']

class TeacherListSerializer(serializers.ModelSerializer):
    sub_teacher = SubCategoryListSerializer(read_only=True, many=True)
    class Meta:
        model = Teacher
        fields = ['id','first_name', 'last_name',  'avatar', 'sub_teacher',]


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ['language_name']

class CourseListSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(many=True)
    created_by = TeacherNameSerializer()
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    students_count = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ['id', 'course_name', 'description', 'level', 'language', 'price', 'avg_rating', 'review_count', 'students_count', 'created_by', 'course_image',
                  'is_certificate',  ]

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_review_count(self, obj):
        return obj.get_review_count()

    def get_students_count(self, obj):
        return obj.get_students_count()

class TeacherDetailSerializer(serializers.ModelSerializer):
    networks_teacher = NetworkTeacherSerializer(many=True, read_only=True)
    course_teacher = CourseListSerializer(read_only=True, many=True)
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'avatar', 'role', 'bio', 'networks_teacher', 'course_teacher' ]

class SubCategoryDetailSerializer(serializers.ModelSerializer):
    subcategory_course = CourseListSerializer(many=True, read_only=True)
    class Meta:
        model = SubCategory
        fields = ['subcategory_name', 'subcategory_course']

class CourseCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'course_name']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    due_date = serializers.DateTimeField(format='%d-%m-%Y %H:%M')
    class Meta:
        model = Assignment
        fields = ['id', 'assignment_name', 'description', 'due_date']

class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'lesson_file', 'video_url', 'has_assignment']

class LessonDetailSerializer(serializers.ModelSerializer):
    assignment_lesson = AssignmentSerializer(read_only=True, many=True)
    class Meta:
        model = Lesson
        fields = ['title', 'lesson_file', 'video_url', 'assignment_lesson']

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ['id', 'exam_name', 'duration']

class ExamListSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()
    total_score = serializers.SerializerMethodField()
    class Meta:
        model = Exam
        fields = ['id', 'exam_name', 'duration', 'question_count', 'total_score']

    def get_question_count(self,obj):
        return obj.get_question_count()

    def get_total_score(self, obj):
        return obj.get_total_score()

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'option_name']

class QuestionSerializer(serializers.ModelSerializer):
    question_option = OptionSerializer(read_only=True, many=True)
    class Meta:
        model = Question
        fields = ['id', 'question_name', 'score', 'question_option']

class ExamDetailSerializer(serializers.ModelSerializer):
    question_exam = QuestionSerializer(read_only=True, many=True)
    class Meta:
        model = Exam
        fields = [ 'exam_name', 'duration', 'question_exam']

class CertificateSerializer(serializers.ModelSerializer):
    course = CourseCertificateSerializer()
    class Meta:
        model = Certificate
        fields = ['course', 'created_date', 'certificate_file']

class ReviewSerializer(serializers.ModelSerializer):
    student = StudentNameSerializer()
    likes = serializers.SerializerMethodField()
    dislikes = serializers.SerializerMethodField()
    created_date = serializers.DateTimeField(format='%Y-%m-%d')
    class Meta:
        model = Review
        fields = ['id', 'student', 'rating', 'text', 'likes', 'dislikes', 'created_date']

    def get_likes(self, obj):
        obj.get_likes()

    def get_dislikes(self, obj):
        obj.get_dislikes()

class ReviewLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewLike
        fields = '__all__'

class ChapterSerializer(serializers.ModelSerializer):
    count_lesson = serializers.SerializerMethodField()
    lesson_chapter = LessonListSerializer(read_only=True, many=True)
    exams = ExamListSerializer(read_only=True, many=True)
    class Meta:
        model = Chapter
        fields = ['id', 'chapter_name', 'count_lesson', 'lesson_chapter', 'exams']

    def count_lesson(self, obj):
        return obj.count_lesson()


class CourseDetailSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(many=True)
    created_by = TeacherInfoSerializer()
    subcategory = SubCategorySerializer(many=True)
    chapters = ChapterSerializer(read_only=True, many=True)
    course_review = ReviewSerializer(read_only=True, many=True)
    created_date = serializers.DateField(format='%Y-%m-%d')

    class Meta:
        model = Course
        fields = ['course_name', 'description', 'level', 'language', 'price', 'is_certificate', 'created_by',
                  'subcategory', 'chapters', 'course_review','created_date' ]