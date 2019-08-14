# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from django.core.exceptions import ValidationError


class Department(models.Model):
    name = models.CharField(max_length=120)
    status = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def question(self):
        if self.pk:
            return Question.objects.filter(department=self.pk)
        else:
            return None


class QuestionSet(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    status = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


def validate_list(value):
    ''' takes a text value and verifies that there is at least one comma '''
    values = value.split(',')
    if len(values) < 2:
        raise ValidationError("The selected field requires an associated list of choices. Choices must contain more than one item.")


class Question(models.Model):
    TEXT = 'text'
    RADIO = 'radio'
    SELECT = 'select'
    SELECT_MULTIPLE = 'select-multiple'
    INTEGER = 'integer'

    QUESTION_TYPES = (
        (TEXT, 'Text'),
        (RADIO, 'Radio'),
        (SELECT, 'Select'),
        (SELECT_MULTIPLE, 'Select Multiple'),
        (INTEGER, 'Integer'),
    )

    text = models.TextField()
    required = models.BooleanField()
    question_set = models.ForeignKey(QuestionSet, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    question_type = models.CharField(max_length=200, choices=QUESTION_TYPES, default=TEXT)
    choices = models.TextField(blank=True, null=True,
            help_text='if the question type is "radio," "select," or "select multiple" provide a comma-separated list of options for this question.')
    status = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if (self.question_type == Question.RADIO or self.question_type == Question.SELECT
                or self.question_type == Question.SELECT_MULTIPLE):
            validate_list(self.choices)
        super(Question, self).save(*args, **kwargs)

    def get_choices(self):
        ''' parse the choices field and return a tuple formatted appropriately for the 'choices' argument of a form widget '''
        choices = self.choices.split(',')
        choices_list = []
        for c in choices:
            c = c.strip()
            choices_list.append((c, c))
        choices_tuple = tuple(choices_list)
        return choices_tuple

    def __str__(self):
        return self.text


class Response(models.Model):
    # a response object is just a collection of question and answer with a
    # a unique interview uuid
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    customer = models.CharField(max_length=200)
    customer_uuid = models.CharField("Interview unique identifier", max_length=36)

    def __unicode__(self):
        return "response %s" % self.customer_uuid


class AnswerBase(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

# these type-specific answer models user a text field to allow for flexible
# field sizes depending on the actual question this answer corresponds to. any
# "required" attribute will be enforced by the form.


class AnswerText(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerRadio(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerSelect(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerSelectMultiple(AnswerBase):
    body = models.TextField(blank=True, null=True)


class AnswerInteger(AnswerBase):
    body = models.IntegerField(blank=True, null=True)