# Generated by Django 5.1.4 on 2025-01-04 04:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='answer_text',
        ),
        migrations.AddField(
            model_name='answer',
            name='scale_answer',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='yes_no_answer',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('YN', 'Yes/No'), ('SC', 'Scale (1-10)')], default='YN', max_length=2),
        ),
    ]
