# Generated by Django 2.2.1 on 2019-05-01 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('context', '0009_auto_20190501_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity_relation_type',
            name='parent_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='context.Entity_Relation_Type'),
        ),
        migrations.AddField(
            model_name='entity_type',
            name='parent_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='context.Entity_Type'),
        ),
    ]
