# Generated manually to change telephone from IntegerField to CharField

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0002_alter_utilisateur_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='telephone',
            field=models.CharField(blank=True, help_text='Format : +222 12 34 56 78', max_length=20, null=True),
        ),
    ]

