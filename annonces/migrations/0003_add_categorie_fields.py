
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('annonces', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorie',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='categorie',
            name='icone',
            field=models.CharField(blank=True, help_text="Nom de l'icône Font Awesome", max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='categorie',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
        ),
    ]

