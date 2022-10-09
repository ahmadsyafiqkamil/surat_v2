from django.db import models
import uuid
from .validator import validate_file_extension
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core import serializers


#
#
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


def _upload_path(instance, filename):
    return instance.get_upload_path(filename)


class Klasifikasi(models.Model):
    kode = models.CharField(max_length=5, verbose_name='Kode Klasifikasi')
    nama_klasifikasi = models.CharField(max_length=100, verbose_name='Nama Klasifikasi')

    class Meta:
        db_table = 'tbl_klasifikasi'

    def __str__(self):
        return "{} - {}".format(self.kode, self.nama_klasifikasi)


class Fungsi(models.Model):
    kode = models.CharField(max_length=10, verbose_name='Kode Fungsi')
    fungsi = models.CharField(max_length=100, verbose_name='Fungsi / Bidang Teknis')

    # koordinator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='koordinator',verbose_name='Koordinator Fungsi')

    class Meta:
        db_table = 'tbl_fungsi'

    def __str__(self):
        return self.fungsi


#
#
class JenisDokumen(models.Model):
    kode = models.CharField(max_length=10, verbose_name='Kode Dokumen')
    jenis_dokumen = models.CharField(max_length=255, verbose_name='Jenis Dokumen')

    class Meta:
        db_table = 'tbl_jenis_dokumen'

    def __str__(self):
        return self.jenis_dokumen


class Dokumen(models.Model):
    pilihan_status = [
        ('0', 'BELUM DIBACA'),
        ('1', 'SUDAH DIBACA'),
        # ('2', 'DISPOSISI'),
        # ('3', 'BATAL'),

    ]
    id = models.UUIDField('id', default=uuid.uuid4, primary_key=True, unique=True,
                          null=False, blank=False, editable=False)
    nomor_surat_lengkap = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nomor Surat Lengkap')
    nomor_surat = models.IntegerField(verbose_name='Nomor Surat')
    tanggal = models.DateField(verbose_name='Tanggal')
    pejabat_penandatangan = models.CharField(max_length=255, verbose_name='Pembuat Dokumen')
    tujuan = models.ManyToManyField(Fungsi, through='TujuanDokumen', through_fields=('dokumen', 'fungsi'),
                                    related_name='tujuan_dokumen')
    perihal = models.TextField(blank=True, null=True, verbose_name='Perihal')
    fungsi = models.ForeignKey(Fungsi, on_delete=models.CASCADE, verbose_name='Fungsi', related_name='fungsi_pengirim')
    jenis_dokumen = models.ForeignKey(JenisDokumen, on_delete=models.CASCADE, verbose_name='Jenis Dokumen',
                                      related_name='jenis')
    klasifikasi = models.ForeignKey(Klasifikasi, on_delete=models.CASCADE, verbose_name='Tujuan Dokumen',
                                    related_name='klasifikasi_dokumen')
    file_dokumen = models.FileField(upload_to='document/%Y-%m-%d/', validators=[validate_file_extension], null=True,
                                    blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Pengirim',
                             related_name='pengirim')
    tujuan_eksternal = models.TextField(blank=True, null=True, verbose_name='Tujuan Eksternal')
    status = models.CharField(max_length=10, choices=pilihan_status, default=0, null=True)

    class Meta:
        db_table = 'tbl_dokumen'

    def __str__(self):
        return self.nomor_surat_lengkap


#
#
class TujuanDokumen(models.Model):
    # status
    # 0 = unread
    # 1 = readS
    pilihan_status = [
        ('0', 'BELUM DIBACA'),
        ('1', 'SUDAH DIBACA'),
        # ('2', 'DISPOSISI'),
        # ('3', 'BATAL'),

    ]
    dokumen = models.ForeignKey(Dokumen, on_delete=models.CASCADE)
    fungsi = models.ForeignKey(Fungsi, on_delete=models.CASCADE, related_name="fungsi_tujuan")
    status = models.IntegerField(verbose_name="Status", null=True, blank=True, default=0, choices=pilihan_status)

    class Meta:
        db_table = 'tbl_tujuan_dokumen'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fungsi = models.ForeignKey(Fungsi, on_delete=models.CASCADE, blank=True, null=True, related_name="fungsi_profile")

    # satker = models.CharField(max_length=100, null=True, blank=True, )

    def __str__(self):
        return f"{self.user}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
