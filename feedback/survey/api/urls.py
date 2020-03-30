from django.conf.urls import url
from .views import DepartmentListAPIView
# Uncomment the next two lines to enable the admin:

urlpatterns = [
        url(r'^$', DepartmentListAPIView.as_view(), name='list'),
        # url(r'^questionnaire/(?P<id>\d+)/$', survey_views.questionnaire, name='questionnaire'),
        # # url(r'^index/', survey_views.index, name='index '),
        # # url(r'^question-set/(?P<id>\d+)/$', survey_views.question_set, name='question-set'),
        # url(r'^question-set/(?P<id>\d+)/$', survey_views.survey, name='survey'),
]
    