from django_meta_og.models import Content


def meta(request):
    return {"django_meta_og": Content.objects.all()}
