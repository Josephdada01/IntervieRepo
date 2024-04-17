import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_doctor_doctor_id_alter_doctor_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='patient_id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular patient across whole hospital', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='doctor',
            name='doctor_id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular doctor across whole hospital', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='patient',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
