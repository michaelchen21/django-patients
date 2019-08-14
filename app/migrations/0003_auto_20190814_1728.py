# Generated by Django 2.2.2 on 2019-08-14 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20190814_1048'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='patient',
            name='Last name, first name, date of birth constraint',
        ),
        migrations.RenameField(
            model_name='patient',
            old_name='date_of_birth',
            new_name='dob',
        ),
        migrations.AlterField(
            model_name='glasses',
            name='price',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddConstraint(
            model_name='patient',
            constraint=models.UniqueConstraint(fields=('last_name', 'first_name', 'dob'), name='Last name, first name, date of birth constraint'),
        ),
    ]