# Generated by Django 2.2.4 on 2019-08-21 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('context', '0017_auto_20190821_1833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entity_identifier_type',
            name='type_list',
            field=models.ManyToManyField(blank=True, null=True, to='context.Entity_Type'),
        ),
    ]
