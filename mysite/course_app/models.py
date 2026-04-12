from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    RoleChoices = (
    ('student', 'student'),
    ('teacher', 'teacher')
    )
    role = models.CharField(max_length=20, choices=RoleChoices, default='student')
    bio = models.TextField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(17), MaxValueValidator(100)], null=True, blank=True)
    avatar = models.ImageField(upload_to='image_user', null=True, blank=True)
    date_registered = models.DateField(auto_now_add=True)


class Teacher(UserProfile):
    phone_number = PhoneNumberField(blank=True)

    class Meta:
        verbose_name = 'Teacher'

class NetworkTeacher(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='networks_teacher')
    network_name = models.CharField(max_length=32)
    network_url = models.URLField()

class Category(models.Model):
    category_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.category_name

class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=62, unique=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True, related_name='sub_teacher')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_sub')

    def __str__(self):
        return self.subcategory_name

class Language(models.Model):
    language_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.language_name

class Course(models.Model):
    course_name = models.CharField(max_length=100)
    description = models.TextField()
    subcategory = models.ManyToManyField(SubCategory, related_name='subcategory_course')
    Level_Choices = (
    ('начальный', 'начальный'),
    ('средний', 'средний'),
    ('продвинутый', 'продвинутый'),
    )
    level = models.CharField(max_length=32, choices=Level_Choices)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(Teacher,on_delete=models.CASCADE, related_name='course_teacher')
    created_date = models.DateField(auto_now_add=True)
    update_at = models.DateField()
    language = models.ManyToManyField(Language)
    course_image = models.ImageField(upload_to='image_course/')
    is_certificate = models.BooleanField(default=True)

    def __str__(self):
        return self.course_name

    def get_avg_rating(self):
        ratting = self.course_review.all()
        if ratting.exists():
            return round(sum([i.rating for i in ratting]) / ratting.count(), 1)
        return 0

    def get_review_count(self):
        return self.course_review.count()

    def get_students_count(self):
        return self.student_course.count()

class Student(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    course = models.ManyToManyField(Course, related_name='student_course')



class NetworkStudent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    network_name = models.CharField(max_length=32)
    network_url = models.URLField()


class Chapter(models.Model):
    chapter_name = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')

    def __str__(self):
        return self.chapter_name

    def count_lesson(self):
        return self.lesson_chapter.count()

class Lesson(models.Model):
    title = models.CharField(max_length=64)
    lesson_file = models.FileField(upload_to='lesson_files/', null=True, blank=True)
    content = models.TextField()
    video_url = models.URLField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lesson_chapter')
    has_assignment = models.BooleanField(default=True)

class Assignment(models.Model):
    assignment_name = models.CharField(max_length=64)
    description = models.TextField()
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assignment_lesson')
    due_date = models.DateTimeField(verbose_name='дедлайн')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class Exam(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='exams')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=32)
    duration = models.DurationField()

    def get_question_count(self):
        return self.question_exam.count()

    def get_total_score(self):
        total = self.question_exam.all()
        if total.exists():
            return sum([i.score for i in total])
        return 0

    def __str__(self):
        return f'{self.chapter} {self.exam_name}'

class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='question_exam')
    question_name = models.CharField(max_length=150)
    score = models.PositiveSmallIntegerField(choices=[(i, str(i))for i in range(1,6)])

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_option')
    option_name = models.CharField(max_length=64)
    option_type = models.BooleanField()

class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    certificate_file = models.FileField(upload_to='certificate_file/')
    created_date = models.DateField(auto_now_add=True)

class Review(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_review')
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i))for i in range(1,6)], null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_likes(self):
        has_like = self.review_like.all()
        if has_like.exists():
            return has_like.filter(like=True).count()
        return 0

    def get_dislikes(self):
        has_dislike = self.review_like.all()
        if has_dislike.exists():
            return has_dislike.filter(dislike=True).count()
        return 0

class ReviewLike(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_like')
    like = models.BooleanField(default=False)
    dislike = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
