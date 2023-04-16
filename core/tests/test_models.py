from django.test import TestCase
from core.models import HOD, Admin, CustomUser, Department, Institution, Staff
from django.utils import timezone
# from django.core.urlresolvers import reverse
# from whatever.forms import WhateverForm

# models test
class InstitutionModelTestCase(TestCase):
    def test_create_institution(self):
        institution = Institution.objects.create(
            name='Test Institution',
            country='US',
            institution_order='1',
            institution_cluster='1',
            institution_category='1',
            institution_gender_category='1',
            institution_accomodation_type='1',
            institution_status='1',
            institution_type='1',
            institution_in_ASAL_area=False,
            institution_residence='1',
        )

        self.assertEqual(institution.name, 'Test Institution')
        self.assertEqual(institution.country, 'US')


# class AdminModelTestCase(TestCase):
#     def setUp(self):
#         self.user = CustomUser.objects.create(
#             email='testuser1@examplee.com', password='testpassword2'
#         )
#         self.institution = Institution.objects.create(
#             name='Test Institutions', institution_order='3'
#         )
#         self.admin = Admin.objects.create(
#             admin=self.user, institution=self.institution
#         )

#     def test_admin_model(self):
#         admin = Admin.objects.get(id=self.admin.id)
#         self.assertEqual(admin.admin, self.user)
#         self.assertEqual(admin.institution, self.institution)

## Tests for Departmemnt model
# import uuid

# from django.test import TestCase
# from core.models import Department, HOD, Staff, CustomUser, Institution


# class DepartmentTestCase(TestCase):

#     def setUp(self):
#         self.user = CustomUser.objects.create(
#             first_name='John',
#             last_name='Doe',
#             email='john.doe@example.com',
#         )
#         self.hod = HOD.objects.create(
#             admin=self.user,
#             phonenumber='1234567890',
#             institution=Institution.objects.create(name='Test Institution'),
#         )
#         self.staff = Staff.objects.create(name='Staff Name')

#     def test_create_department(self):
#         department = Department.objects.create(
#             name='Test Department',
#             head=self.hod,
#             deputy=self.staff
#         )
#         self.assertIsNotNone(department.id)
#         self.assertIsNotNone(department.institution_code)
#         self.assertEqual(department.name, 'Test Department')
#         self.assertEqual(department.description, 'institution')
#         self.assertEqual(department.head, self.hod)
#         self.assertEqual(department.deputy, self.staff)

#     def test_update_department(self):
#         department = Department.objects.create(
#             name='Test Department',
#             head=self.hod,
#             deputy=self.staff
#         )
#         department.name = 'New Department Name'
#         department.description = 'New description'
#         department.save()
#         department.refresh_from_db()
#         self.assertEqual(department.name, 'New Department Name')
#         self.assertEqual(department.description, 'New description')

#     def test_delete_department(self):
#         department = Department.objects.create(
#             name='Test Department',
#             head=self.hod,
#             deputy=self.staff
#         )
#         department.delete()
#         with self.assertRaises(Department.DoesNotExist):
#             Department.objects.get(id=department.id)

#     def test_set_head_and_deputy_to_none(self):
#         department = Department.objects.create(
#             name='Test Department',
#             head=self.hod,
#             deputy=self.staff
#         )
#         department.head = None
#         department.deputy = None
#         department.save()
#         department.refresh_from_db()
#         self.assertIsNone(department.head)
#         self.assertIsNone(department.deputy)

#     def test_institution_code_is_unique(self):
#         department1 = Department.objects.create(
#             name='Department 1',
#             head=self.hod,
#             deputy=self.staff
#         )
#         department2 = Department.objects.create(
#             name='Department 2',
#             head=self.hod,
#             deputy=self.staff
#         )
#         self.assertNotEqual(department1.institution_code, department2.institution_code)
