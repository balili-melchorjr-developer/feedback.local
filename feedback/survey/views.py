from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import URLResolver
from django.contrib import messages
from django.db.models import Q, Count
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()

# Create your views here.

from .models import Question, Questionnaire, QuestionSet, Department, AnswerRadio, AnswerBase
from .forms import ResponseForm

def home(request):
    department = Department.objects.all()
    context = {'department_list': department}
    return render(request, 'home.html', context)

def questionnaire(request, id):    
    questionnaire = Questionnaire.objects.filter(department=id)
    context = {'questionnaire_list': questionnaire}
    return render(request, 'questionnaire.html', context)

# def question_set(request, id):
#     department = Department.objects.get(id=id)
#     questionset_list = QuestionSet.objects.filter(department=department)
#     context = {'questionset_list': questionset_list}
#     return render(request, 'question_set.html', context)
    
def survey(request, id):
    try:
        department = Department.objects.all()
    except Department.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
    
    questionnaire = Questionnaire.objects.get(id=id)
    question_set_items = QuestionSet.objects.filter(questionnaire=questionnaire)
    question_set = (c.name for c in question_set_items)
    print("Question for this department")
    print(question_set_items)
    if request.method == 'POST':
        form = ResponseForm(request.POST, questionnaire=questionnaire)
        if form.is_valid():
            response = form.save()
            form = ResponseForm(questionnaire=questionnaire)
            # return HttpResponseRedirect("/survey/%s" % response.customer_uuid)
            messages.success(request, 'Thank you!', extra_tags='alert')
    else:
        form = ResponseForm(questionnaire=questionnaire)
        print(form)
        # TODO sort by question_set
    return render(request, 'survey.html', {'response_form': form, 'questionnaire': questionnaire, 'question_set': question_set})


def survey_detail(request, id):
    try:
        department = Department.objects.get(id=id)
    except Department.DoesNotExist:
        raise Http404("No MyModel matches the given query.")

    department = Department.objects.get(id=id)
    question_set_items = QuestionSet.objects.filter(department=department)
    question_set = (c.name for c in question_set_items)
    print("Question for this department")
    print(question_set_items)
    if request.method == 'POST':
        form = ResponseForm(request.POST, department=department)
        if form.is_valid():
            response = form.save()
            form = ResponseForm(department=department)
            # return HttpResponseRedirect("/survey/%s" % response.customer_uuid)
            messages.success(request, 'Thank you!', extra_tags='alert')
    else:
        form = ResponseForm(department= department)
        print(form)
        # TODO sort by question_set
    return render(request, 'survey.html', {'response_form': form, 'department': department, 'question_set': question_set})


def reports(request, id):

    counts = {}
    # qs_answerbase = AnswerBase.objects.filter(response__questionnaire__department=id)
    qs_answerbase = AnswerRadio.objects.filter(Q(body="Wow! Excellent"))
    # for i in qs_answerbase:
        # counts[i] = (counts[i] + 1) if (i in counts) else 1

    # question = Questionnaire.objects.annotate(ans_count=Count('answerbase__response', filter=Q(answerbase__answerradio__body="Wow! Excellent")))

    context = {'response_list': qs_answerbase, 'counts': counts}
    return render(request, 'reports.html', context)

def get_data(request):

    labels = []
    default = []

    qs = AnswerBase.objects.all()
    # for i in qs:
    #     labels.append(i.answerradio.body)    
    #     default.append(i.answerradio.body)


    # for i in labels:
    #     counts[i] = (counts[i] + 1) if (i in counts) else 1

    data = {
        "Department": labels,
        "Happy": default,
    }
    return JsonResponse(data)

class ReportData(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):

        labels = []
        default_department = []
        
        qs = AnswerBase.objects.all()
        for ans in qs:
            labels.append(ans.answerradio.body)
            default_department.append(ans.answerradio.body)
        # answer_wow = AnswerRadio.objects.filter(body="Wow! Excellent").count()
        # answer_aa = AnswerRadio.objects.filter(body="Above Average").count()
        # answer_a = AnswerRadio.objects.filter(body="Average").count()
        # answer_ba = AnswerRadio.objects.filter(body="Below Average").count()
        # answer_p = AnswerRadio.objects.filter(body="Poor").count()
        # labels = ['Wow! Excellent', 'Above Average', 'Average', 'Below Average', 'Poor']
        # default_department = [answer_wow, answer_aa, answer_a, answer_ba, answer_p]
        data = {
            "labels": labels,
            "default": default_department,
        }
        return Response(data)