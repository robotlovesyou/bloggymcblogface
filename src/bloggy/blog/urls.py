from django.conf.urls import url

from . import views

app_name = 'blog'
urlpatterns = [
    url(r'^admin/login/', views.admin_login, name='login'),
    url(r'^admin/do_login/', views.admin_do_login, name="do_login"),
    url(r'^admin/$', views.admin, name='admin'),
    url(r'^(?P<article_id>[\w\-]+)/$', views.article, name='article'),
]
