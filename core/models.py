from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
"""


"""
# Create your models here.
class Institution(models.Model):

    INSTITUTION_TYPE = [
        ('1','Preprimary'),   
        ('2','Primary'),
        ('3','Secondary'),
        ('4','tertiary'),
        ('5','all')
    ]

    id = models.AutoField(primary_key=True)
    institution_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=255, default="institution")
    institution_type = models.CharField(max_length=255, choices=INSTITUTION_TYPE, default='5')

    # logo = models.FileField(default="")

class SessionYearModel(models.Model):
    id = models.AutoField(primary_key=True)
    session_start_year = models.DateField()
    session_end_year = models.DateField()
    objects = models.Manager()

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    cost = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class Grade(models.Model):
    id = models.AutoField(primary_key=True)
    grade_name = models.CharField(max_length=255)
    cost = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

class CustomUser(AbstractUser):
    user_type_data = ((1, "Admin"), (2, "Staff"), (3, "Student"), (4, "HOD"), (5,"Guardian"),(6,"Teacher"),(7,"Specialuser") )
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    objects = models.Manager()

class HOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.DO_NOTHING)
    phonenumber = models.CharField(max_length=12)
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.admin.first_name}  {self.admin.last_name}'


class Teacher(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=12)
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return self.user.name


class Staff(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.admin.first_name}  {self.admin.last_name}'


class Department(models.Model):
    id = models.AutoField(primary_key=True)
    institution_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=255, default="institution")
    head = models.ForeignKey(HOD, on_delete=models.DO_NOTHING, null=True)
    deputy = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, null=True)


class Guardian(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=12)
    bank = models.CharField(null=True, max_length=1000)
    gender = models.CharField(max_length=50)

    def __str__(self):
        return self.user.name


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    admission_number =  models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    gender = models.CharField(max_length=50)
    profile_pic = models.FileField()
    address = models.TextField()
    institution = models.ForeignKey(Institution, on_delete=models.DO_NOTHING, null=True)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(
        SessionYearModel, on_delete=models.DO_NOTHING, null=True
    )
    grade = models.ForeignKey(Grade, on_delete=models.DO_NOTHING, null=True)
    fee_balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    guardian = models.ForeignKey(Guardian, on_delete=models.DO_NOTHING, null=True, related_name='students')
    ##TODO: See how to best add a second guardian
    # second_guardian = models.ForeignKey(Guardian, on_delete=models.DO_NOTHING, null=True)
    objects = models.Manager()


class SpecialUser(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phonenumber = models.CharField(max_length=12)

    def __str__(self):
        return self.user.name

# Creating Django Signals

# It's like trigger in database. It will run only when Data is Added in CustomUser model


@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 1:
            Admin.objects.create(
                admin=instance,
                # institution=Institution.objects.get(id=1)
            )
        if instance.user_type == 2:
            Staff.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(
                admin=instance,
                # course_id=Courses.objects.get(id=1),
                # session_year_id=SessionYearModel.objects.get(id=1),
                address="",
                profile_pic="",
                gender="",
            )
        if instance.user_type == 4:
            HOD.objects.create(admin=instance)
        if instance.user_type == 5:
            Guardian.objects.create(admin=instance)
        if instance.user_type == 6:
            Teacher.objects.create(admin=instance)
        if instance.user_type == 7:
            Guardian.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.admin.save()
    if instance.user_type == 2:
        instance.staff.save()
    if instance.user_type == 3:
        instance.students.save()
    if instance.user_type == 4:
        instance.hod.save()
    if instance.user_type == 5:
        instance.guardian.save()
    if instance.user_type == 6:
        instance.teacher.save()
