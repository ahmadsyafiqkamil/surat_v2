from django.contrib import admin

# Register your models here.
from .models import Dokumen, Fungsi, JenisDokumen, Klasifikasi, Profile

# Register your models here.
admin.site.register(Klasifikasi)
admin.site.register(Fungsi)
admin.site.register(Dokumen)
admin.site.register(JenisDokumen)
admin.site.register(Profile)
