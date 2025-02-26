from django.db import migrations


def noop(apps, schema_editor):
    pass


def create_properties(apps, schema_editor):
    Namespace = apps.get_model('django_meta_og', 'Namespace')
    Property = apps.get_model('django_meta_og', 'Property')

    og, _ = Namespace.objects.get_or_create(prefix="og", defaults={"uri": "https://ogp.me/ns#"})
    for name in (
        # Basic
        "title",
        "type",
        "image",
        "url",
        # Optional
        "audio",
        "description",
        "determiner",
        "locale",
        "locale:alternate",
        "site_name",
        "video",
        # Image
        "image:url",
        "image:secure_url",
        "image:type",
        "image:width",
        "image:height",
        "image:alt",
        # Video
        "video",
        "video:secure_url",
        "video:type",
        "video:width",
        "video:height",
        # Audio
        "audio",
        "audio:secure_url",
        "audio:type",
    ):
        Property.objects.get_or_create(namespace=og, name=name)

    music, _ = Namespace.objects.get_or_create(prefix="music", defaults={"uri": "https://ogp.me/ns/music#"})
    for name in (
        "duration",
        "album",
        "album:disc",
        "album:track",
        "musician",
        "release_date",
        "creator",
    ):
        Property.objects.get_or_create(namespace=music, name=name)

    video, _ = Namespace.objects.get_or_create(prefix="video", defaults={"uri": "https://ogp.me/ns/video#"})
    for name in (
        "actor",
        "actor:role",
        "director",
        "writer",
        "duration",
        "release_date",
        "tag",
        "series",
    ):
        Property.objects.get_or_create(namespace=video, name=name)

    article, _ = Namespace.objects.get_or_create(prefix="article", defaults={"uri": "https://ogp.me/ns/article#"})
    for name in (
        "published_time",
        "modified_time",
        "expiration_time",
        "author",
        "section",
        "tag",
        "isbn",
        "release_date",
    ):
        Property.objects.get_or_create(namespace=article, name=name)

    profile, _ = Namespace.objects.get_or_create(prefix="profile", defaults={"uri": "https://ogp.me/ns/profile#"})
    for name in (
        "first_name",
        "last_name",
        "username",
        "gender",
    ):
        Property.objects.get_or_create(namespace=profile, name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('django_meta_og', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_properties, noop),
    ]
