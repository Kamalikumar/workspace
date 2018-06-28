from django.conf.urls import url


from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^todo$',views.suggestion,name='todo'),
    url(r'update/(?P<task_id>[0-9]+)/$',views.update,name='update_items'),
    url(r'delete/(?P<task_id>[0-9]+)/$',views.delete_list,name='existing_list'),
    url(r'^password/$',views.password,name='password'),
     # url(r'^edit-post/(?P<pk>\d+)/$', views.edit_post, name='edit_post'),
    url(r'^(?P<pk>[0-9]+)$', views.get_detail, name='movies')
]