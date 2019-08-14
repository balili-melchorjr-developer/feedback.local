from django.contrib import admin
from .models import Department, QuestionSet, Question, Response, AnswerBase, AnswerText, AnswerRadio, AnswerSelect, AnswerSelectMultiple, AnswerInteger


# Register your models here.


class QuestionInline(admin.TabularInline):
    model = Question
    # ordering = ("question_set")
    extra = 0


class QuestionSetInline(admin.TabularInline):
    model = QuestionSet
    extra = 0


class DepartmentAdmin(admin.ModelAdmin):
    inlines = [QuestionInline, QuestionSetInline]


class AnswerBaseInline(admin.StackedInline):
    fields = ("question", "body")
    # readonly_fields = ("question")
    extra = 0


class AnswerTextInline(AnswerBaseInline):
    model = AnswerText


class AnswerRadioInline(AnswerBaseInline):
    model = AnswerRadio


class AnswerSelectInline(AnswerBaseInline):
    model = AnswerSelect


class AnswerSelectMultipleInline(AnswerBaseInline):
    model = AnswerSelectMultiple


class AnswerIntegerInline(AnswerBaseInline):
    model = AnswerInteger


class ResponseAdmin(admin.ModelAdmin):
    list_display = ("customer_uuid", "customer", "date_created")
    inlines = [AnswerTextInline, AnswerRadioInline, AnswerSelectInline, AnswerSelectMultipleInline, AnswerIntegerInline]
    # specifies the order as well  as which fields to act on
    # readonly_fields = ("department", "date_created", "date_modified", "customer_uuid")


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Response, ResponseAdmin)
