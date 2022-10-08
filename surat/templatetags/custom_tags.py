from django import template
from django.contrib.auth.models import Group
from ..models import Dokumen, Profile

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.filter(name='check_profile')
def check_profile(id_dokumen, nama_user):
    print(id_dokumen)
    print(nama_user)
    dokumen = Dokumen.objects.get(id=id_dokumen)
    fungsi_tujuan = [i.fungsi for i in dokumen.tujuan.all()]
    fungsi = Profile.objects.values("fungsi__fungsi").get(user__username=nama_user)
    return True if fungsi["fungsi__fungsi"] in fungsi_tujuan else False
