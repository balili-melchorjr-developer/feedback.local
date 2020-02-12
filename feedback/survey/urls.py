from django.conf.urls import url
from survey import views as survey_views
# Uncomment the next two lines to enable the admin:


urlpatterns = [
        url(r'^$', survey_views.home, name='home'),
        url(r'^questionnaire/(?P<id>\d+)/$', survey_views.questionnaire, name='questionnaire'),
        url(r'^reports/(?P<id>\d+)/$',survey_views.reports, name='reports'),
        url(r'^api/data/$', survey_views.get_data, name='api-data'),
        url(r'^api/report/data/$', survey_views.ReportData.as_view()),
        # url(r'^index/', survey_views.index, name='index'),
        # url(r'^question-set/(?P<id>\d+)/$', survey_views.question_set, name='question-set'),
        url(r'^question-set/(?P<id>\d+)/$', survey_views.survey, name='survey'),
]
    