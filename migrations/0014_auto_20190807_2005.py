# Generated by Django 2.2.4 on 2019-08-07 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('context', '0013_entity_relation_relation_through'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity_relation_type_trait',
            name='required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='entity_type_trait',
            name='required',
            field=models.BooleanField(default=False),
        ),
    ]