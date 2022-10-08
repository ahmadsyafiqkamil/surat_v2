from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from notifications.utils import slug2id
from .models import Dokumen, Profile
from .forms import DokumenForm
from django.urls import reverse_lazy
from django.db.models import Max
from notifications.signals import notify
from django.contrib.auth.models import User


# Create your views here.
class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'content/home.html'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    success_url = '/'


class SuratListView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'content/daftar_surat.html'


class TambahSurat(LoginRequiredMixin, generic.edit.CreateView):
    model = Dokumen
    template_name = 'content/surat.html'
    form_class = DokumenForm
    redirect_field_name = 'redirect_to'

    # success_url = reverse_lazy("surat:daftar-surat")

    def get_form_kwargs(self):
        kwargs = super(TambahSurat, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        fungsi = Profile.objects.values("fungsi").get(user=self.request.user)
        kwargs.update({'fungsi': fungsi['fungsi']})
        return kwargs

    def form_valid(self, form):
        post = form.save(commit=False)
        bulan = form.cleaned_data['tanggal'].strftime('%m')
        tahun = int(form.cleaned_data['tanggal'].strftime('%Y'))
        id_klasifikasi = form.cleaned_data['klasifikasi'].pk
        kode_klasifikasi = form.cleaned_data['klasifikasi'].kode
        kode_fungsi = form.cleaned_data['fungsi'].kode
        kode_dokumen = form.cleaned_data['jenis_dokumen'].kode
        tujuan_dokumen = form.cleaned_data['tujuan']
        nomor_surat = 0
        nomor = Dokumen.objects.filter(klasifikasi=id_klasifikasi, tanggal__year=tahun).aggregate(Max('nomor_surat'))
        nomor_terakhir = nomor['nomor_surat__max']
        tahun_terakhir = Dokumen.objects.filter(klasifikasi=id_klasifikasi).order_by('-tanggal').values_list("tanggal",
                                                                                                             flat=True)[
                         :1]

        # ini masih masalah
        if tahun_terakhir.first() is None:
            print("1", tahun_terakhir.first())
            nomor_surat = 1

        elif tahun_terakhir.first().year == tahun:
            print("3", tahun_terakhir.first())
            if nomor_terakhir == 0:
                nomor_surat = 1
            else:
                nomor_surat = nomor_terakhir + 1

        elif tahun_terakhir.first().year <= tahun:
            print("2", tahun_terakhir.first())
            nomor_surat = 1

        print("nomor surat baru", nomor_surat)
        post.nomor_surat_lengkap = "{}.{}/{}/{}/{}/{}".format(kode_dokumen, nomor_surat, kode_klasifikasi, bulan,
                                                              tahun, kode_fungsi)
        tujuan = self.request.POST.getlist('tujuan')
        print(len(tujuan))
        post.user = self.request.user
        post.nomor_surat = nomor_surat
        print("{}.{}/{}/{}/{}/{}".format(kode_dokumen, nomor_surat, kode_klasifikasi, bulan, tahun, kode_fungsi))
        post.save()
        form.save_m2m()
        for i, v in enumerate(tujuan):
            penerima = Profile.objects.filter(fungsi_id=v)
            for i in penerima:
                user_penerima = User.objects.get(username=i)
                notify.send(self.request.user, recipient=user_penerima, verb=f'test')

        return redirect("surat:daftar-surat")


class DeleteSurat(generic.edit.DeleteView):
    model = Dokumen
    success_url = reverse_lazy('surat:daftar-surat')


class EditSurat(LoginRequiredMixin, generic.edit.UpdateView):
    model = Dokumen
    template_name = 'content/surat.html'
    form_class = DokumenForm

    def form_valid(self, form):
        post = form.save(commit=False)
        bulan = form.cleaned_data['tanggal'].strftime('%m')
        tahun = int(form.cleaned_data['tanggal'].strftime('%Y'))
        id_klasifikasi = form.cleaned_data['klasifikasi'].pk
        kode_klasifikasi = form.cleaned_data['klasifikasi'].kode
        kode_fungsi = form.cleaned_data['fungsi'].kode
        kode_dokumen = form.cleaned_data['jenis_dokumen'].kode
        nomor_surat = 0
        nomor = Dokumen.objects.filter(klasifikasi=id_klasifikasi, tanggal__year=tahun).aggregate(Max('nomor_surat'))
        nomor_terakhir = nomor['nomor_surat__max']
        tahun_terakhir = Dokumen.objects.filter(klasifikasi=id_klasifikasi).order_by('-tanggal').values_list("tanggal",
                                                                                                             flat=True)[
                         :1]
        id_klasifikasi_terakhir = Dokumen.objects.get(id=self.kwargs.get('pk')).klasifikasi_id
        nomor_sekarang = Dokumen.objects.get(id=self.kwargs.get('pk')).nomor_surat
        if id_klasifikasi == id_klasifikasi_terakhir:
            nomor_surat = nomor_sekarang
        else:
            print(nomor_terakhir)
            print(tahun)
            # ini masih masalah
            if tahun_terakhir.first() is None:
                print("1", tahun_terakhir.first())
                nomor_surat = 1

            elif tahun_terakhir.first().year == tahun:
                print("3", tahun_terakhir.first())
                if nomor_terakhir == 0:
                    nomor_surat = 1
                else:
                    nomor_surat = nomor_terakhir + 1

            elif tahun_terakhir.first().year <= tahun:
                print("2", tahun_terakhir.first())
                nomor_surat = 1

        print("nomor surat baru", nomor_surat)
        post.nomor_surat_lengkap = "{}.{}/{}/{}/{}/{}".format(kode_dokumen, nomor_surat, kode_klasifikasi, bulan,
                                                              tahun, kode_fungsi)

        print(self.request.POST.getlist('tujuan'))
        post.user = self.request.user
        post.nomor_surat = nomor_surat
        print("{}.{}/{}/{}/{}/{}".format(kode_dokumen, nomor_surat, kode_klasifikasi, bulan, tahun, kode_fungsi))
        post.save()
        form.save_m2m()
        tujuan = self.request.POST.getlist('tujuan')
        for i, v in enumerate(tujuan):
            penerima = Profile.objects.filter(fungsi_id=v)
            for i in penerima:
                user_penerima = User.objects.get(username=i)
                notify.send(self.request.user, recipient=user_penerima, verb=f'test edit nomor surat {nomor_surat}')

        return redirect("surat:daftar-surat")

    def get_form_kwargs(self):
        kwargs = super(EditSurat, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        fungsi = Profile.objects.values("fungsi").get(user=self.request.user)
        print(fungsi['fungsi'])
        kwargs.update({'fungsi': fungsi['fungsi']})
        return kwargs


class DetailSurat(LoginRequiredMixin, generic.DetailView):
    model = Dokumen
    template_name = 'content/detail_surat.html'


def UpdateStatus(request, pk):
    Dokumen = Dokumen.objects.get(id=pk)
    Dokumen.status = 1
    return reverse_lazy('surat:detail_surat', kwargs={'pk': pk})
