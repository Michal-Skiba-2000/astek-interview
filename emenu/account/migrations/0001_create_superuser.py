from django.contrib.auth.models import User
from django.db import migrations


class Migration(migrations.Migration):
    """Migration that creates superuser"""
    initial = True

    dependencies = [
    ]

    @staticmethod
    def generate_superuser(apps, schema_editor):
        """Create superuser"""
        superuser_name = 'admin'
        superuser_email = 'admin@example.com'
        superuser_password = 'admin'

        superuser = User.objects.create_superuser(
            username=superuser_name,
            email=superuser_email,
            password=superuser_password)

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]
