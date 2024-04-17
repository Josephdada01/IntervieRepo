# Generated by Django 5.0.2 on 2024-04-17 13:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0005_patient_patient_id_alter_doctor_doctor_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='patient_id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular doctor across whole hospital', primary_key=True, serialize=False),
        ),
    ]