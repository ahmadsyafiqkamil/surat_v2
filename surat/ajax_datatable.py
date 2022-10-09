from ajax_datatable.views import AjaxDatatableView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from .models import Profile
from django.db.models import Q

from .models import Dokumen, TujuanDokumen


class SuratAjaxView(AjaxDatatableView):
    model = Dokumen
    code = 'surat'
    title = 'Daftar surat'
    initial_order = [["nomor_surat_lengkap", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        # AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'nomor_surat_lengkap', 'title': "Nomor Surat", 'visible': True, },
        {'name': 'fungsi', 'title': "Pengirim", 'visible': True, 'orderable': True,},
        {'name': 'tanggal', 'title': "Tanggal", 'visible': True, },
        {'name': 'tujuan', 'visible': True, 'title': 'Tujuan Nota Dinas', 'm2m_foreign_field': 'tujuan__fungsi'},
        {'name': 'perihal', 'visible': True, 'title': 'Perihal', },
        {'name': 'file_dokumen', 'visible': True, 'title': 'Dokumen', },
        {'name': 'status', 'visible': True, 'title': 'Status', },
        {'name': 'action', 'title': 'Aksi', 'searchable': False, 'orderable': False, },
    ]

    def customize_row(self, row, obj):

        file = self.model.objects.get(id=row["pk"])
        if file.file_dokumen:
            path_file = file.file_dokumen.url
        else:
            path_file = "#"

        row['file_dokumen'] = """
               <a href="%s">file</a>
               """ % path_file

        fungsi = Profile.objects.get(user__username=self.request.user)
        status = TujuanDokumen.objects.get(dokumen_id=row["pk"], fungsi_id=fungsi.fungsi)
        if status.status is 1:
            text_status = "<p class='bg-primary'>SUDAH DIBACA</p>"
        else:
            text_status = "<p class='bg-info'>BELUM DIBACA</p>"

        row["status"] = text_status
        row['action'] = f"""
                                <a href="#" class="btn btn-primary" id="add" 
                                    onclick="detail('{row['pk']}'); " >
                                       Detail
                                    </a>
                            """


    def get_initial_queryset(self, request=None):
        fungsi = Profile.objects.values("fungsi").get(user=self.request.user)
        return self.model.objects.filter(
            Q(tujuan=fungsi["fungsi"]))


class SuratKeluarAjaxView(AjaxDatatableView):
    model = Dokumen
    code = 'surat'
    title = 'Daftar surat'
    initial_order = [["nomor_surat_lengkap", "asc"], ]
    length_menu = [[10, 20, 50, 100, -1], [10, 20, 50, 100, 'all']]
    search_values_separator = '+'

    column_defs = [
        # AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'nomor_surat_lengkap', 'title': "Nomor Surat", 'visible': True, },
        {'name': 'fungsi', 'title': "Pengirim", 'visible': True, },
        {'name': 'tanggal', 'title': "Tanggal", 'visible': True, },
        {'name': 'tujuan', 'visible': True, 'title': 'Tujuan Nota Dinas', 'm2m_foreign_field': 'tujuan__fungsi'},
        {'name': 'perihal', 'visible': True, 'title': 'Perihal', },
        {'name': 'file_dokumen', 'visible': True, 'title': 'Dokumen', },
        {'name': 'action', 'title': 'Aksi', 'searchable': False, 'orderable': False, },

    ]

    def customize_row(self, row, obj):

        file = self.model.objects.get(id=row["pk"])
        if file.file_dokumen:
            path_file = file.file_dokumen.url
        else:
            path_file = "#"
        row['file_dokumen'] = """
               <a href="%s">file</a>
               """ % path_file

        row['action'] = f"""
                                <a href="#" class="btn btn-primary" id="add" 
                                    onclick="detail('{row['pk']}'); " >
                                       Detail
                                    </a>
                                <a href="#" class="btn btn-info btn-edit" id="edit"
                                onclick="edit('{row['pk']}'); " >
                                   Edit
                                </a>
                                <a href="/hapus_surat/{row['pk']}" class="btn btn-danger" data-toggle="modal"
                                data-target="#delete-item-modal"
                                id="delete-item"
                                >
                                Delete
                                </a>
                            """

    def get_initial_queryset(self, request=None):
        fungsi = Profile.objects.values("fungsi").get(user=self.request.user)
        return self.model.objects.filter(
            Q(fungsi=fungsi["fungsi"]))
