from django.db import models
from core.models import Students

# Create your models here.
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    compulsory_classes = models.ForeignKey("ClusterClass",on_delete=models.DO_NOTHING,null=True)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.course_name

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_date = models.DateField()
    session_end_date = models.DateField()
    is_current = models.BooleanField(default=False)
    objects = models.Manager()

    def __str__(self):
        if self.is_current:
            return ('Current Session')
        return f'from - {self.session_start_date} to - {self.session_end_date}'
    class Meta:
        ordering = ['id']

    def get_next(self):
        return Session.objects.filter(id__gt=self.id).order_by('id').first()
    
    def get_previous(self):
        return Session.objects.filter(id__lt=self.id).order_by('-id').first()
    
    def get_first(self):
        return Session.objects.order_by('id').first()

    def get_last(self):
        return Session.objects.order_by('id').last()

class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    student = models.ForeignKey("core.Students", models.DO_NOTHING)
    is_active = models.BooleanField(default=False)
    enrollment_date = models.DateField(auto_now=True)
    objects = models.Manager()
    
    class Meta:
        unique_together = ('session', 'student')

class GradeLevel(models.Model):
    id = models.AutoField(primary_key=True)
    grade_name = models.CharField(max_length=50)
    cost = models.IntegerField()
    compulsory_classes = models.ForeignKey("ClusterClass", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.grade_name

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=50, null=True)
    class_code = models.CharField(max_length=50, null=True)
    teacher = models.ForeignKey("core.Teacher", on_delete=models.DO_NOTHING, null=True)
    gradelevel = models.ManyToManyField(GradeLevel)
    session_id = models.ForeignKey(Session, on_delete=models.DO_NOTHING, null=True)
    is_elective = models.BooleanField(default=False)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    cost = models.IntegerField()
    objects = models.Manager()

    def __str__(self):
        return self.class_name


class ClassEnrollment(models.Model):
    id = models.AutoField(primary_key=True)
    selected_class = models.ForeignKey("Class", on_delete=models.DO_NOTHING)
    student = models.ForeignKey('core.Students', on_delete=models.DO_NOTHING)
    objects = models.Manager()

class ClassAttendance(models.Model):
    id = models.AutoField(primary_key=True)
    datetime = models.DateTimeField()
    present = models.ManyToManyField('core.Students', blank=True)
    absent = models.ManyToManyField('core.Students', blank=True, related_name='absentees')
    classroom = models.ForeignKey('Class', on_delete=models.CASCADE)
    objects = models.Manager()

    def __str__(self):
        return f'{self.classroom} attendance for {self.datetime.date()}'


class ClusterClass(models.Model):
    id = models.AutoField(primary_key=True)
    cluster_class_name = models.CharField(max_length=100)
    classes = models.ManyToManyField(Class)
    objects = models.Manager()

    def __str__(self):
        return self.cluster_class_name

class DiscplinaryCases(models.Model):
    id = models.AutoField(primary_key=True)
    displinary_action = models.CharField(max_length=255)
    discplinary_case_notes = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    resumption_date = models.DateTimeField()
    notes = models.CharField(max_length=255)
    objects = models.Manager()


## EXAM MANAGEMENT MODELS!!!
class Exam(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    exam_type = models.ForeignKey('Examtype', on_delete=models.CASCADE)
    exam_date = models.DateTimeField()
    is_compulsory = models.BooleanField(default=True)
    exam_class = models.ForeignKey('Class', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

class ExamType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class GradeRange(models.Model):
    id = models.AutoField(primary_key=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='grade_ranges')
    grade = models.CharField(max_length=1, choices=(('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')))
    min_score = models.IntegerField()
    max_score = models.IntegerField()

    def __str__(self):
        return f'{self.exam}: {self.grade} ({self.min_score}-{self.max_score})'
    
class ExamRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    exams = models.ForeignKey('Exam', on_delete=models.CASCADE, null=True)
    student = models.ForeignKey('core.Students',on_delete=models.CASCADE,null=True)
    date_registered = models.DateTimeField(auto_now=True)
    registered = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

class ExamResult(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    grade = models.CharField(max_length=1)
    score = models.IntegerField()

    def __str__(self) -> str:
        return f'Name - {self.student} exam - {self.exam} grade - {self.grade}'

class Transcripts(models.Model):
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    class_results = models.JSONField(null=True)
    sessions = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    score = models.FloatField()
    grade = models.CharField(max_length=255)
    passed = models.BooleanField(default=False)
    remarks = models.TextField()

    def __str__(self):
        return self.student
    

class AcademicCommunications(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    USER_CHOICES = (
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('notice', 'General Notice')
    )
    communication_method = models.CharField(
        max_length=10,
        choices=USER_CHOICES,
        default='email'
    )
    def __str__(self):
        return f"{self.title} - {self.communication_method}"
