# Generated by Django 3.0.10 on 2020-10-30 21:09
import json

from django.db import migrations


def migrate_tax_rules(apps, schema_editor):
    TaxRule = apps.get_model('pretixbase', 'TaxRule')
    for tr in TaxRule.objects.filter(eu_reverse_charge=True):
        if tr.custom_rules and tr.custom_rules != '[]':
            # Custom rules take precedence
            continue
        r = [{
            'country': str(tr.home_country),
            'address_type': '',
            'action': 'vat'
        }, {
            'country': 'EU',
            'address_type': 'business_vat_id',
            'action': 'reverse'
        }, {
            'country': 'EU',
            'address_type': '',
            'action': 'vat'
        }, {
            'country': 'ZZ',
            'address_type': '',
            'action': 'no'
        }]
        tr.custom_rules = json.dumps(r)
        tr.save()


class Migration(migrations.Migration):
    dependencies = [
        ('pretixbase', '0169_checkinlist_gates'),
    ]

    operations = [
        migrations.RunPython(migrate_tax_rules, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name='taxrule',
            name='eu_reverse_charge',
        ),
        migrations.RemoveField(
            model_name='taxrule',
            name='home_country',
        ),
    ]