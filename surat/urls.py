from django.urls import path, re_path
from .views import *

from .ajax_datatable import SuratAjaxView,SuratKeluarAjaxView

app_name = 'surat'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('daftar_surat/', SuratListView.as_view(), name='daftar-surat'),
    path('SuratAjaxView/', SuratAjaxView.as_view(), name='surat_ajax_view'),
    path('SuratKeluarAjaxView/', SuratKeluarAjaxView.as_view(), name='surat_keluar_ajax_view'),
    path('TambahSurat/', TambahSurat.as_view(), name='tambah_surat'),
    re_path('hapus_surat/(?P<pk>[-\w]*)$', DeleteSurat.as_view(), name='hapus_surat'),
    re_path('edit_surat/(?P<pk>[-\w]*)$', EditSurat.as_view(), name='edit_surat'),
    re_path('detail_surat/(?P<pk>[-\w]*)$', DetailSurat.as_view(), name='detail_surat'),
    re_path('update_status/(?P<pk>[-\w]*)$', UpdateStatus, name='update_status'),
    # re_path('kajian_edit/(?P<pk>[-\w]*)$', KajianEditView.as_view(), name='kajian_edit'),
    # re_path('mark-as-read/(?P<slug>\d+)/$', mark_as_read, name='mark_as_read'),

]

