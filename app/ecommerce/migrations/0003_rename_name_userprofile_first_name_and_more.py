# Generated by Django 4.2.10 on 2024-02-16 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_alter_userprofile_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(default='q', max_length=255),
            preserve_default=False,
        ),
    ]
