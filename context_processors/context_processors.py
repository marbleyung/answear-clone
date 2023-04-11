from shop.models import *


def include_genders(request):
    genders = ItemGender.objects.all()
    return {'genders': genders}


def include_header_types(request):
    header_types = ItemType.objects.all()[::-1]
    return {'header_types': header_types}
