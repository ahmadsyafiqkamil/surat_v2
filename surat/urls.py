from django.urls import path, re_path
from .views import *
# from .ajax_datatable import KajianAjaxView

app_name = 'kajian'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    # re_path('kajian_edit/(?P<pk>[-\w]*)$', KajianEditView.as_view(), name='kajian_edit'),
    # re_path('mark-as-read/(?P<slug>\d+)/$', mark_as_read, name='mark_as_read'),

]
