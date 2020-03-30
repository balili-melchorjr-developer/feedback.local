from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render
from django.template import RequestContext
from django.urls import URLResolver
from django.contrib import messages
from django.db.models import Q, Count
from collections import Counter
import datetime

from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()

# Create your views here.

from .models import Question, Questionnaire, QuestionSet, Department, AnswerRadio, AnswerBase
from .forms import ResponseForm

def home(request):
    department = Department.objects.all().order_by('name')
    context = {'department_list': department}
    return render(request, 'home.html', context)

def questionnaire(request, id):    
    questionnaire = Questionnaire.objects.filter(department=id).order_by('name')
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


def reports(request, pk):

    counts = {}
    department = Department.objects.get(pk=pk)
    qs_answerbase = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(Q(body="Patient") | Q(body="Significant other (Relative or Friend)")).values("body").annotate(counts=Count("body"))
    # qs_answerbase = AnswerRadio.objects.filter)
    # for i in qs_answerbase:
        # counts[i] = (counts[i] + 1) if (i in counts) else 1   

    # question = Questionnaire.objects.annotate(ans_count=Count('answerbase__response', filter=Q(answerbase__answerradio__body="Wow! Excellent")))
    qs = Question.objects.filter(questionnaire__department=pk).filter(text="How was your overall experience?").values_list("choices", flat=True)
    qs_list = []
    for item in qs:
        qs_list += item.split(",")

    qs_new = []
    for i in range(len(qs_list)):
        answer_wow = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=1).filter(body=qs_list[i]).count()
        qs_new.append(answer_wow)
    # qs_answerradio = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk)
    # qs_answer = qs_answerradio._set.select_related()

    # qs_qs = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).values('body').annotate(ans_count = Count('body'))
    # d = {}
    # qs_new = {d['body']: d['ans_count'] for f in qs_qs}
    # i = 0
    # qs_new = []
    # while i < len(qs_list):
    #     answer_wow = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=1).filter(**{qs_list: qs_list}).count()
    #     qs_new.append(answer_wow)
    #     i += 1    
   

    # for answer in qs_answer:
    #     if qs_new not in (answer.answerbase_ptr.response.questionnaire.id):
    #         qs_new[answer.answerbase_ptr.response.questionnaire.id] = {
    #             'answer': answer.answerbase_ptr.response.questionnaire.id,
    #             'count': 0
    #         }

    #     qs_new[answer.answerbase_ptr.response.questionnaire.id]['count'] += 1



    # ans_filter = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).values_list("body")
    # for i in ans_filter:
    #     i = 
    # i = 0
    # qs_new = {}
    # while i < len(qs_list):
    # answer_wow = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=1).filter(body=qs_new).count()
    # for i in answer_wow:        
        # i += 1        
        # qs_new[i] = (qs_new[i] + 1) if (i in qs_new) else 1 

    context = {'department': department, 'response_list': qs_answerbase, 'counts': counts, 'qs_list': qs_list, 'qs_new': qs_new}
    return render(request, 'reports.html', context)

def get_data(request, pk):

    labels = []
    default = []

    # qs_filter = AnswerBase.objects.get(response__questionnaire=pk)
    qs = AnswerRadio.objects.values("body").annotate(counts=Count("body"))
    
    # qs = AnswerRadio.objects.all()
    for i in qs:
        labels.append(i)    
        default.append(i)

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

    def get(self, request, pk, format=None):
        
        qs = Question.objects.filter(pk=1).filter(text="How was your overall experience?").values_list("choices", flat=True)
        qs_list = []
        for item in qs:
            qs_list += item.split(",")       

        # qs = Question.objects.filter(questionnaire=pk).values("choices").annotate(counts=Count("choices"))
        # qs = AnswerRadio.objects.filter(body="Poor").values("body").annotate(counts=Count("body")) 
        # qs = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire_id=15).filter(body="Above Average").values("body").annotate(counts=Count("body"))   

        # for ans in qs:
        #     labels.append(ans["choices"])
        #     default_department.append(ans["counts"])

        # qs_question = Question.objects.filter(questionnaire=pk).filter(text="How was your overall experience?").only("choices")
        # choices = qs_question.choices.split(',')
        # qs_choice = []
        # for c in choices:
        #     c = c.strip()
        #     answer_wow = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="Wow! Excellent").count()
           
                    
        # answer_wow = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=15).filter(body="Wow! Excellent").count()
        # answer_aa = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=15).filter(body="Above Average").count()
        # answer_a = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=15).filter(body="Average").count()
        # answer_ba = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=15).filter(body="Below Average").count()
        # answer_p = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=15).filter(body="Poor").count()

        answer_wow = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="Wow! Excellent").count()
        answer_aa = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="Above Average").count()
        answer_a = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="Average").count()
        answer_ba = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="Below Average").count()
        answer_p = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="Poor").count()
       
        labels = ['Wow! Excellent', 'Above Average', 'Average', 'Below Average', 'Poor']
        default_department = [answer_wow, answer_aa, answer_a, answer_ba, answer_p]

        data = {
            "labels": labels,
            "default": default_department,
        }

        answer_10 = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="10").count()
        answer_9 = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="9").count()
        answer_8 = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="8").count()
        answer_7 = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="7").count()
        answer_6 = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="6").count()
        answer_5 = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="5").count()
        answer_4 = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="4").count()
        answer_3 = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="3").count()
        answer_2 = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="2").count()
        answer_1 = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="1").count()


        labels2 = ['10', '9', '8', '7', '6', '5', '4', '3', '2', '1']
        default_department2 = [answer_10, answer_9, answer_8, answer_7, answer_6, answer_5, answer_4, answer_3, answer_2, answer_1]

        data2 = {
            "labels": labels2,
            "default": default_department2,
        }

        i_answer_wow = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="Wow! Excellent").count()
        i_answer_aa = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="Above Average").count()
        i_answer_a = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="Average").count()
        i_answer_ba = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="Below Average").count()
        i_answer_p = AnswerRadio.objects.filter(answerbase_ptr__response__questionnaire=pk).filter(body="Poor").count()

        labels3 = ['Wow! Excellent', 'Above Average', 'Average', 'Below Average', 'Poor']
        default_department3 = [i_answer_wow, i_answer_aa, i_answer_a, i_answer_ba, i_answer_p]

        data3 = {
            "labels": labels3,
            "default": default_department3,
        }

        report_arr = [data, data2, data3]

        return Response(report_arr)

def dashboard(request):
    department = Department.objects.all().order_by('name')
    context = {'department_list': department}
    return render(request, 'dashboard.html', context)