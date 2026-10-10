from django.db import migrations

def update_elan_image(apps, schema_editor):
    PortfolioConcept = apps.get_model('core', 'PortfolioConcept')
    for concept in PortfolioConcept.objects.all():
        title_lower = (concept.title or '').lower()
        slug_lower = (concept.slug or '').lower()
        img_str = str(concept.image_url or '')
        if 'elan' in slug_lower or 'elan' in title_lower or 'élan' in title_lower or 'photo-1512290900672' in img_str:
            concept.image_url = '/static/images/elan-dermatology.jpg'
            concept.save(update_fields=['image_url'])

def reverse_elan_image(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_analyticsevent_event_type_and_more'),
    ]

    operations = [
        migrations.RunPython(update_elan_image, reverse_elan_image),
    ]
