# Generated by Django 4.1.4 on 2023-04-30 09:38

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ("academics", "0016_classattendance"),
        ("core", "0003_admintype_applicant_alter_admin_institution_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="admin",
            name="admin_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="core.admintype"
            ),
        ),
        migrations.AlterField(
            model_name="admin",
            name="institution",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.institution",
            ),
        ),
        migrations.AlterField(
            model_name="admintype",
            name="name",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="county",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="current_address",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="date_of_birth",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="email",
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="expected_completion_date",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female"), ("O", "Other")],
                max_length=1,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="id_or_passport_number",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="nationality",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="other_names",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="permanent_address",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="photo_1",
            field=models.ImageField(null=True, upload_to="applicant_photos"),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="photo_2",
            field=models.ImageField(null=True, upload_to="applicant_photos"),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="programme_level",
            field=models.CharField(
                choices=[
                    ("PGD", "Postgraduate Diploma"),
                    ("MSc", "Masters"),
                    ("PhD", "Doctorate"),
                ],
                max_length=3,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="special_needs",
            field=models.CharField(
                choices=[("Y", "Yes"), ("N", "No")], max_length=1, null=True
            ),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="start_date",
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="surname",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="applicant",
            name="telephone",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="department",
            name="deputy",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.staff",
            ),
        ),
        migrations.AlterField(
            model_name="department",
            name="description",
            field=models.CharField(default="institution", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="department",
            name="head",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="core.hod"
            ),
        ),
        migrations.AlterField(
            model_name="guardian",
            name="bank",
            field=models.CharField(max_length=2550, null=True),
        ),
        migrations.AlterField(
            model_name="hod",
            name="institution",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.institution",
            ),
        ),
        migrations.AlterField(
            model_name="institution",
            name="bank_details",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="institution",
            name="contact_details",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="institution",
            name="country",
            field=django_countries.fields.CountryField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name="institution",
            name="currency",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="institution",
            name="examination_centre_number",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="institution",
            name="institution_location_hierarchy",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="institution",
            name="institution_statutory_numbers",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="institution",
            name="logo",
            field=models.FileField(null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="staff",
            name="description",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="staff",
            name="institution",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.institution",
            ),
        ),
        migrations.AlterField(
            model_name="staff",
            name="name",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="students",
            name="address",
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name="students",
            name="bio_data",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="students",
            name="grade",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="academics.gradelevel",
            ),
        ),
        migrations.AlterField(
            model_name="students",
            name="index_number",
            field=models.CharField(max_length=20, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="students",
            name="institution",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.institution",
            ),
        ),
        migrations.AlterField(
            model_name="students",
            name="name",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="students",
            name="profile_pic",
            field=models.FileField(null=True, upload_to=""),
        ),
        migrations.AlterField(
            model_name="students",
            name="registration_number",
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="students",
            name="relationships",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="students",
            name="religion",
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="students",
            name="session_year_id",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="academics.session",
            ),
        ),
        migrations.AlterField(
            model_name="students",
            name="sponsor_contact",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="students",
            name="student_contact",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="bank_account",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="bank_details",
            field=models.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="industrial_training_number",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="institution",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="core.institution",
            ),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="nhif",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="phonenumber",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="pin_tax_number",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="secondary_bank_account",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="secondary_phone_number",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="social_security_number",
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name="teacher",
            name="statutory_numbers",
            field=models.JSONField(null=True),
        ),
    ]