# Generated by Django 5.1.1 on 2024-11-10 10:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('isbn', models.CharField(max_length=13, unique=True)),
                ('category', models.CharField(choices=[('FICTION', 'Fiction'), ('NON_FICTION', 'Non-Fiction'), ('REFERENCE', 'Reference'), ('MAGAZINE', 'Magazine')], max_length=20)),
                ('author', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('AVAILABLE', 'Available'), ('ISSUED', 'Issued')], default='AVAILABLE', max_length=20)),
                ('added_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('membership_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('ACTIVE', 'Active'), ('INACTIVE', 'Inactive'), ('SUSPENDED', 'Suspended')], default='ACTIVE', max_length=20)),
                ('total_fines', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='BookIssue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('due_date', models.DateTimeField()),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('fine_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('is_returned', models.BooleanField(default=False)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.book')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.member')),
            ],
        ),
    ]
