from django.db import models

# Create your models here.
class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_date = models.DateField()
    session_end_date = models.DateField()
    objects = models.Manager()

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    cost = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    class_capacity = models.CharField(max_length=100)
    streams_per_lass = models.CharField(max_length=100)
    # Sample data
    # {
    #   "maximum_examinable_subjects" : "6",
    #   "minimum_examinable_subjects": "6"
    #   "final_exam_basis": "????"
    #   "pass_mark":"60%"
    # }
    exam_data = models.JSONField()
    lecturer_max_subject = models.CharField(max_length=100)
    student_teacher_ratio = models.CharField(max_length=100)
    curriculum_description = models.CharField(max_length=255)


class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    grade_name = models.CharField(max_length=255)
    cost = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class ExtraCurricularActivities(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    notes = models.CharField(max_length=255)


class DiscplinaryCases(models.Model):
    id = models.AutoField(primary_key=True)
    displinary_action = models.CharField(max_length=255)
    discplinary_case_notes = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    resumption_date = models.DateTimeField()
    notes = models.CharField(max_length=255)

