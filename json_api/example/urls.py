from django.conf.urls import url
from example import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'ajax/more/$', view=views.more_poems),
    url(r'ajax/add/$', view=views.add),
    url(r'^index/$', views.index,name='index'),
]