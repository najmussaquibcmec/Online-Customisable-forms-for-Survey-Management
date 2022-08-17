from django.conf.urls import url, include
from django.contrib.auth import views
from django.contrib import admin
from django.urls import path
from forms.survey import views as survey_views


urlpatterns = [
	url(r'^admin/',admin.site.urls),
    url(r'^$', survey_views.main, name='main'),
    url(r'^login/$', views.LoginView.as_view(),{'template_name': 'registration/login.html'}, name='login'),
    url(r'^logout/$', survey_views.logout_request, name='logout'),
    url(r'^signup/$', survey_views.signup, name='signup'),
    url(r'^home/$', survey_views.home, name='home'),
    url(r'^password/$', survey_views.password, name='password'),
	  url(r'^createform/', survey_views.create, name="createform"),    
	  url(r'^formlist/', survey_views.formlist, name= "formlist"),
   	path('displayform/<pk>', survey_views.displayform, name="displayform"),
   	path('answer/<pk>', survey_views.answer, name="answer"),
    path('question/<pk>',survey_views.question, name="question"),
    
]
