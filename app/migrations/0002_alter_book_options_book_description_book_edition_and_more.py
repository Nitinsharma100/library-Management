# Generated by Django 5.1.1 on 2024-11-10 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['category', 'title']},
        ),
        migrations.AddField(
            model_name='book',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='edition',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='publication_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='category',
            field=models.CharField(choices=[('BUSINESS', 'Business'), ('SCIENCE', 'Science'), ('COMPUTER', 'Computer Science'), ('MATHEMATICS', 'Mathematics'), ('PHYSICS', 'Physics'), ('CHEMISTRY', 'Chemistry'), ('BIOLOGY', 'Biology'), ('ECONOMICS', 'Economics'), ('MANAGEMENT', 'Management'), ('MARKETING', 'Marketing'), ('FINANCE', 'Finance'), ('LITERATURE', 'Literature'), ('HISTORY', 'History'), ('PHILOSOPHY', 'Philosophy'), ('OTHER', 'Other')], max_length=20),
        ),
    ]
