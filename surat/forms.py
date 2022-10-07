from builtins import print

from django import forms
from django.conf import settings
from django.forms import ModelMultipleChoiceField

from .models import Dokumen, Fungsi
# from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput, MonthPickerInput
from django_select2.forms import Select2MultipleWidget
from surat.models import Klasifikasi, Fungsi, Dokumen, JenisDokumen, Profile
from django.contrib.auth.models import User
from django.template.defaultfilters import filesizeformat
from django.utils.translation import gettext_lazy as _


class DokumenForm(forms.ModelForm):
    class Meta:
        model = Dokumen
        fields = (
            'jenis_dokumen', 'klasifikasi', 'fungsi', 'tanggal', 'pejabat_penandatangan', 'tujuan', 'tujuan_eksternal',
            'perihal', 'file_dokumen')

        widgets = {
            'jenis_dokumen': forms.Select(
                attrs={
                    'class': 'form-control select2'
                }
            ),
            'klasifikasi': forms.Select(
                attrs={
                    'class': 'form-control select2'
                }
            ),
            'fungsi': forms.Select(
                attrs={
                    'class': 'form-control select2'
                }
            ),
            'perihal': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'cols': '40',
                    'row': '10',
                    'placeholder': 'Masukkan Perihal'
                }
            ),
            'tujuan': forms.SelectMultiple(
                attrs={
                    'class': 'form-control select2',
                    'multiple': 'multiple'
                }
            ),
            'tujuan_eksternal': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'cols': '40',
                    'row': '10',
                    'placeholder': 'Pisahkan Tujuan Eksternal dengan # di setiap tujuan'
                }
            ),
            'tanggal': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date',
                    'id': 'datepicker1'
                }
            ),

            'file_dokumen': forms.FileInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'pejabat_penandatangan': forms.TextInput(attrs={'class': 'form-control', }),
        }

        labels = {
            'jenis_dokumen': _('Jenis Dokumen'),
            'klasifikasi': _('Kode Klasifikasi'),
            'fungsi': _('Kode Fungsi'),
            'tujuan': _('Tujuan Dokumen'),
            'tujuan_eksternal': _('Tujuan Eksternal'),
            'tanggal': _('Tanggal'),
            'pejabat_penandatangan': _('Pembuat Dokumen'),
            'perihal': _('Perihal Dokumen'),
            'file_dokumen': _('File')
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        fungsi = kwargs.pop('fungsi')
        super(DokumenForm, self).__init__(*args, **kwargs)
        self.fields['fungsi'].queryset = Fungsi.objects.filter(id=fungsi)


class EditForm(forms.ModelForm):
    tanggal = forms.DateField(
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'id': 'datepicker'}
        )
    )

    class Meta:
        model = Dokumen
        fields = (
            'jenis_dokumen', 'klasifikasi', 'fungsi', 'tanggal', 'pejabat_penandatangan', 'tujuan', 'tujuan_eksternal',
            'perihal', 'file_dokumen')

        widgets = {
            'jenis_dokumen': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'klasifikasi': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'fungsi': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'perihal': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'cols': '40',
                    'row': '10',
                    'placeholder': 'Masukkan Perihal'
                }
            ),

            'tujuan': forms.SelectMultiple(
                attrs={
                    'class': 'js-example-basic-multiple'
                }
            ),
            'tujuan_eksternal': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'cols': '40',
                    'row': '10',
                    'placeholder': 'Pisahkan Tujuan Eksternal dengan # di setiap tujuan'
                }
            ),
            'file_dokumen': forms.ClearableFileInput(
                attrs={
                    'class': 'file-styled'
                }

            )
        }

        labels = {
            'jenis_dokumen': 'Jenis Dokumen',
            'klasifikasi': 'Kode Klasifikasi',
            'fungsi': 'Kode Fungsi',
            'tujuan': 'Tujuan Dokumen',
            'tujuan_eksternal': 'Tujuan Eksternal',
            'tanggal': 'Tanggal',
            'pejabat_penandatangan': 'Pembuat Dokumen',
            'perihal': 'Perihal Dokumen',
            'file_dokumen': 'File'
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        fungsi = kwargs.pop('fungsi')
        super(EditForm, self).__init__(*args, **kwargs)
        if user.is_admin:
            print("admin")
            self.fields['fungsi'].queryset = Fungsi.objects.all()
        elif user.is_staff or user.is_staff_dokumen:
            print(fungsi.fungsi.pk)
            self.fields['fungsi'].queryset = Fungsi.objects.filter(pk=fungsi.fungsi.pk)
