from django.db import models
# from ISOFTLIMS.core.models import Students

# Create your models here.
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_date = models.DateField()
    session_end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        return f'from - {self.session_start_date} to - {self.session_end_date}'

class Enrollment(models.Model):
    enrollment_id = models.AutoField(primary_key=True)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    student = models.ForeignKey("core.Students", models.DO_NOTHING)
    enrollment_date = models.DateField(auto_now=True)
    objects = models.Manager()
    
    class Meta:
        unique_together = ('session', 'student')

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=50, null=True)
    class_code = models.CharField(max_length=50, null=True)
    teacher = models.ForeignKey("core.Teacher", on_delete=models.DO_NOTHING, null=True)
    gradelevel = models.ManyToManyField("GradeLevel", blank=True)
    session_id = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)
    is_elective = models.BooleanField(default=False)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    cost = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return self.class_name

class ClusterClass(models.Model):
    id = models.IntegerField(primary_key=True)
    cluster_class_name = models.CharField(max_length=100)
    classes = models.ManyToManyField("Class", blank=True)
    objects = models.Manager()

class ClassEnrollment(models.Model):
    id = models.AutoField(primary_key=True)
    selected_class = models.ForeignKey("Class", on_delete=models.DO_NOTHING)
    student = models.ForeignKey('core.Students', on_delete=models.DO_NOTHING)
    objects = models.Manager()

class GradeLevel(models.Model):
    id = models.AutoField(primary_key=True)
    grade_name = models.CharField(max_length=50)
    cost = models.IntegerField()
    compulsory_classes = models.ForeignKey(ClusterClass, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.grade_name

class DiscplinaryCases(models.Model):
    id = models.AutoField(primary_key=True)
    displinary_action = models.CharField(max_length=255)
    discplinary_case_notes = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    resumption_date = models.DateTimeField()
    notes = models.CharField(max_length=255)
    objects = models.Manager()
