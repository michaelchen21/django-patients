# Generated by Django 2.2.4 on 2019-08-13 23:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GlassesPrescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.IntegerField(blank=True, null=True)),
                ('exam_date', models.DateTimeField(blank=True, null=True)),
                ('od', models.CharField(blank=True, max_length=255, null=True)),
                ('os', models.CharField(blank=True, max_length=255, null=True)),
                ('va_right', models.CharField(blank=True, max_length=255, null=True)),
                ('va_left', models.CharField(blank=True, max_length=255, null=True)),
                ('pd', models.FloatField(blank=True, null=True)),
                ('conj', models.CharField(blank=True, max_length=255, null=True)),
                ('sclera', models.CharField(blank=True, max_length=255, null=True)),
                ('tears', models.CharField(blank=True, max_length=255, null=True)),
                ('cornea', models.CharField(blank=True, max_length=255, null=True)),
                ('iris', models.CharField(blank=True, max_length=255, null=True)),
                ('antc', models.CharField(blank=True, max_length=255, null=True)),
                ('cc', models.CharField(blank=True, max_length=255, null=True)),
                ('lll', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'glasses_prescription',
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_2', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.CharField(blank=True, max_length=1, null=True)),
                ('downstairs', models.BooleanField(blank=True, null=True)),
            ],
            options={
                'db_table': 'patient',
            },
        ),
        migrations.CreateModel(
            name='Insurance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('insurance_id', models.CharField(blank=True, max_length=255, null=True)),
                ('insurance_id_2', models.CharField(blank=True, max_length=255, null=True)),
                ('can_call', models.BooleanField(blank=True, null=True)),
                ('called', models.BooleanField(blank=True, null=True)),
                ('patient', models.ForeignKey(blank=True, db_column='patient', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Patient')),
            ],
            options={
                'db_table': 'insurance',
            },
        ),
        migrations.CreateModel(
            name='Glasses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('brand', models.CharField(blank=True, max_length=255, null=True)),
                ('model', models.CharField(blank=True, max_length=255, null=True)),
                ('color', models.CharField(blank=True, max_length=255, null=True)),
                ('frame', models.CharField(blank=True, max_length=100, null=True)),
                ('lens', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_lens', models.CharField(blank=True, max_length=255, null=True)),
                ('additional_comments', models.TextField(blank=True, null=True)),
                ('price', models.CharField(blank=True, max_length=255, null=True)),
                ('patient', models.ForeignKey(blank=True, db_column='patient', null=True, on_delete=django.db.models.deletion.CASCADE, to='app.Patient')),
                ('prescription', models.ForeignKey(blank=True, db_column='prescription', null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.GlassesPrescription')),
            ],
            options={
                'db_table': 'glasses',
            },
        ),
    ]
