# Generated by Django 4.1.13 on 2024-03-30 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_conversation_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file_id',
            field=models.CharField(max_length=50, null=True),
        ),
    ]