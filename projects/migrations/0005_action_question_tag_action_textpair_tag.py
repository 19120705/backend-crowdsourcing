# Generated by Django 4.2.1 on 2023-05-29 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_type_label_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='action_question',
            name='tag',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('maybe', 'Maybe')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='action_textpair',
            name='tag',
            field=models.CharField(choices=[('synonymous', 'synonymous'), ('opposite', 'opposite')], default=2, max_length=20),
            preserve_default=False,
        ),
    ]