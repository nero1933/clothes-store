# Generated by Django 4.2.14 on 2024-08-19 08:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_bool', models.BooleanField(default=False)),
                ('stripe_checkout_id', models.CharField(max_length=500)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='ecommerce.order')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
