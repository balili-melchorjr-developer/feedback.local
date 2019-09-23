from django.contrib import admin
from .models import Department, QuestionSet, Question, Response, AnswerBase, AnswerText, AnswerRadio, AnswerSelect, AnswerSelectMultiple, AnswerInteger


# Register your models here.

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


admin.site.register(Department)
admin.site.register(Response, ResponseAdmin)
admin.site.register(Question)
admin.site.register(QuestionSet)