# Generated by Django 5.1.4 on 2025-03-27 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disc', '0011_delete_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disc',
            name='status',
            field=models.CharField(choices=[('lost', 'Lost'), ('found', 'Found'), ('returned', 'Returned'), ('archived', 'Archived')], default='lost', max_length=10),
        ),
    ]
