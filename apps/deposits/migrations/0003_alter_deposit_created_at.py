from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('deposits', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
