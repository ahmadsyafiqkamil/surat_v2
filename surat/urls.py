from django.urls import path, re_path
from .views import *

from .ajax_datatable import SuratAjaxView

app_name = 'surat'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('daftar_surat/', SuratListView.as_view(), name='daftar-surat'),
    path('SuratAjaxView/', SuratAjaxView.as_view(), name='surat_ajax_view'),
    path('TambahSurat/', TambahSurat.as_view(), name='tambah_surat'),
    # re_path('kajian_edit/(?P<pk>[-\w]*)$', KajianEditView.as_view(), name='kajian_edit'),
    # re_path('mark-as-read/(?P<slug>\d+)/$', mark_as_read, name='mark_as_read'),

]
