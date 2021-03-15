# Generated by Django 3.1.7 on 2021-03-11 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20210310_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='policy',
        ),
        migrations.RemoveField(
            model_name='individual',
            name='policy',
        ),
        migrations.AddField(
            model_name='policy',
            name='companyNumber',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.company'),
        ),
        migrations.AddField(
            model_name='policy',
            name='individualNumber',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='clients.individual'),
        ),
    ]