from django.conf.urls import url
from survey import views as survey_views
# Uncomment the next two lines to enable the admin:

urlpatterns = [
        url(r'^$', survey_views.index, name='home'),
        url(r'^survey/(?P<id>\d+)/$', survey_views.survey_detail, name='survey_detail'),
        url(r'^question_set/(?P<id>\d+)/$', survey_views.survey_select, name='survey_select'),
]