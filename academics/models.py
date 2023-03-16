from django.db import models
# from ISOFTLIMS.core.models import Students

# Create your models here.
class Session(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_date = models.DateField()
    session_end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    objects = models.Manager()


class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    student = models.ForeignKey("core.Students", models.DO_NOTHING)
    enrollment_date = models.DateField(auto_now=True)
    objects = models.Manager()

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=50, null=True)
    class_code = models.CharField(max_length=50, null=True)
    teacher = models.ForeignKey("core.Teacher", on_delete=models.DO_NOTHING, null=True)
    grade = models.ForeignKey("Grade", on_delete=models.DO_NOTHING, null=True)
    session_id = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)
    is_elective = models.BooleanField(default=False)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    cost = models.IntegerField()
    objects = models.Manager()


class ClassEnrollment(models.Model):
    id = models.AutoField(primary_key=True)
    selected_class = models.ForeignKey("Class", on_delete=models.DO_NOTHING)
    student = models.ForeignKey('core.Students', on_delete=models.DO_NOTHING)
    objects = models.Manager()


class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    grade_name = models.CharField(max_length=50)
    cost = models.IntegerField()
    # TODO: There needs to be a proper way of handling the multiple foreign keys?
    compulsory_classes = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class DiscplinaryCases(models.Model):
    id = models.AutoField(primary_key=True)
    displinary_action = models.CharField(max_length=255)
    discplinary_case_notes = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    resumption_date = models.DateTimeField()
    notes = models.CharField(max_length=255)
    objects = models.Manager()
