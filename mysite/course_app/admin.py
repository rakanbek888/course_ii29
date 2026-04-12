from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TranslationInlineModelAdmin

@admin.register(Language,Exam,Question,Option,Assignment,Lesson)
class ProductAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class ChapterInline(admin.TabularInline,TranslationInlineModelAdmin):
    model = Chapter
    extra = 1

@admin.register(Course)
class ProductAdmin(TranslationAdmin):
    inlines = [ChapterInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

class SubCategoryInline(admin.TabularInline,TranslationInlineModelAdmin):
    model = SubCategory
    extra = 1

@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    inlines = [SubCategoryInline]
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


class NetworkTeacherInline(admin.TabularInline):
    model = NetworkTeacher
    extra = 1

class TeacherAdmin(admin.ModelAdmin):
    inlines = [NetworkTeacherInline]

class NetworkStudentInline(admin.TabularInline):
    model = NetworkStudent
    extra = 1

class StudentAdmin(admin.ModelAdmin):
    inlines = [NetworkStudentInline]


admin.site.register(UserProfile)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Certificate)
admin.site.register(Review)
admin.site.register(ReviewLike)

