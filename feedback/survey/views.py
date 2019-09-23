from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.urls import URLResolver
from django.contrib import messages
import datetime


# Create your views here.

from .models import Question, Department, QuestionSet
from .forms import ResponseForm

def index(request):
    department_list = Department.objects.all()
    context = {'department_list': department_list}
    return render(request, 'index.html', context)

def survey_select(request, id):
    try:
        department = Department.objects.get(id=id)
    except Department.DoesNotExist:
        raise Http404("No MyModel matches the given query.")
    department = Department.objects.get(id=id)
    questionset_list = QuestionSet.objects.filter(department=department)
    context = {'questionset_list': questionset_list}
    return render(request, 'question_set.html', context)

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
        form = ResponseForm(department=department)
        print(form)
        # TODO sort by question_set
    return render(request, 'survey.html', {'response_form': form, 'department': department, 'question_set': question_set})
