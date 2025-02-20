# Generated by Django 5.1.3 on 2024-11-19 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=3, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='demo.faculty')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches', to='demo.subject')),
            ],
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot_time', models.CharField(choices=[('1', 'Slot 1: 7:30 AM - 9:30 AM'), ('2', 'Slot 2: 10:00 AM - 12:00 AM'), ('3', 'Slot 3: 12:30 AM - 2:30 PM'), ('4', 'Slot 4: 3:00 PM - 5:00 PM'), ('5', 'Slot 5: 5:30 PM - 7:30 PM')], max_length=1)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='demo.batch')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='demo.faculty')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='demo.room')),
            ],
            options={
                'ordering': ['slot_time'],
                'unique_together': {('room', 'slot_time')},
            },
        ),
    ]
