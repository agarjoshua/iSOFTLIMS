from collections import UserDict, UserList
from django.test import TestCase,  Client
from django.urls import reverse
from academics.models import Session
from core import admin
from django.contrib.auth.models import User,Group, get_user_model
from django.contrib.messages import get_messages
from core.forms.guardianforms import AddGuardianForm, EditGuardianForm
from core.forms.hodforms import AddHodForm
from core.forms.institutionform import InstitutionForm
from core.forms.studentforms import AddStudentForm, EditStudentForm
from core.models import HOD, CustomUser, Department,Teacher, Students, Class, SessionYear, Staff, Guardian

class AdminHomeViewTestCase(TestCase):
    def test_admin_home_view(self):
        # create some test data
        Teacher.objects.create(name="John", age=30, subject="Maths")
        Students.objects.create(name="Alice", age=16, grade="10")
        Staff.objects.create(name="Bob", age=25, position="Manager")

        # make a GET request to the admin home page
        response = self.client.get(reverse("admin_home"))

        # check that the response contains the expected data
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1") # all_student_count
        self.assertContains(response, "1") # staff_count
        self.assertContains(response, "John") # staff_name_list
        self.assertContains(response, "Alice") # student_name_list
        self.assertContains(response, "Bob") # student_name_list

class AdminProfileViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            username="admining",
            email="admin@example.com",
            password="testpass123",
            # is_admin=True
        )
        self.client.login(email="admin@example.com", password="testpass123")

    def test_admin_profile_view_should_return_200_status_code(self):
        response = self.client.get(reverse("admin_profile"))
        self.assertEqual(response.status_code, 200)

    def test_admin_profile_view_should_use_correct_template(self):
        response = self.client.get(reverse("admin_profile"))
        self.assertTemplateUsed(response, "admin_template/admin_profile.html")

    def test_admin_profile_view_should_display_user_info(self):
        response = self.client.get(reverse("admin_profile"))
        self.assertContains(response, self.user.email)

    

class AdminProfileUpdateTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testadmin', password='testpass'
        )

    def test_admin_profile_update(self):
        # Log in the user
        self.client.login(username='testadmin', password='testpass')

        # Make a POST request to the admin_profile_update view
        response = self.client.post(reverse('admin_profile_update'), {
            'first_name': 'New',
            'last_name': 'Name',
            'password': 'newpassword'
        })

        # Check that the response is a redirect to the admin_profile view
        self.assertRedirects(response, reverse('admin_profile'))

        # Check that the user's profile was updated
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.first_name, 'New')
        self.assertEqual(updated_user.last_name, 'Name')
        self.assertTrue(updated_user.check_password('newpassword'))


class SchoolProfileTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com', password='testpass'
        )
        self.admin = Admin.objects.create(admin=self.user, institution='Test School')

    def test_school_profile_view(self):
        # Log in as the user
        self.client.login(email='testuser@example.com', password='testpass')

        # Make a GET request to the school_profile view
        response = self.client.get(reverse('school_profile'))

        # Check that the response has a successful status code
        self.assertEqual(response.status_code, 200)

        # Check that the view uses the correct template
        self.assertTemplateUsed(response, 'admin_template/school_profile.html')

        # Check that the view sets the correct context variables
        self.assertEqual(response.context['user'], self.user)
        self.assertIsInstance(response.context['form'], InstitutionForm)



class AddStaffTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="admin@test.com", password="testpass", is_admin=True
        )

    def test_add_staff_page(self):
        # Log in as admin user
        self.client.login(email="admin@test.com", password="testpass")

        # Make a GET request to the add_staff view
        response = self.client.get(reverse("add_staff"))

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the correct template was used to render the response
        self.assertTemplateUsed(response, "admin_template/add_staff_template.html")

class AddStaffSaveTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="admin@test.com", password="testpass", is_admin=True
        )

    def test_add_staff_save(self):
        # Log in as admin user
        self.client.login(email="admin@test.com", password="testpass")

        # Make a POST request to the add_staff_save view with valid data
        response = self.client.post(reverse("add_staff_save"), {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "password": "password",
            "address": "123 Main St",
            "check": False
        })

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the staff member was added to the database
        self.assertEqual(CustomUser.objects.filter(username="johndoe").count(), 1)

        # Make a POST request to the add_staff_save view with invalid data (GET request)
        response = self.client.get(reverse("add_staff_save"))

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that no staff member was added to the database
        self.assertEqual(CustomUser.objects.filter(username="invalid").count(), 0)



class ManageStaffTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a superuser for testing
        User = get_user_model()
        self.user = User.objects.create_superuser(
            email='test@test.com', password='testpass'
        )
        self.client.login(email='test@test.com', password='testpass')

        # Create some staff and teacher objects
        self.staff1 = Staff.objects.create(
            first_name='John',
            last_name='Doe',
            address='123 Main St'
        )
        self.staff2 = Staff.objects.create(
            first_name='Jane',
            last_name='Doe',
            address='456 Elm St'
        )
        self.teacher1 = Students.objects.create(
            first_name='Bob',
            last_name='Smith',
            email='bob@example.com'
        )

    def test_manage_staff_view_forbidden_for_non_admin(self):
        # Create a user without admin privileges
        User = get_user_model()
        non_admin_user = User.objects.create_user(
            email='nonadmin@test.com',
            password='testpass'
        )
        self.client.login(email='nonadmin@test.com', password='testpass')

        # Make a GET request to the manage_staff view
        response = self.client.get(reverse('manage_staff'))

        # Check that the response status code is 403 (forbidden)
        self.assertEqual(response.status_code, 403)

    def test_manage_staff_view_accessible_for_admin(self):
        # Make a GET request to the manage_staff view
        response = self.client.get(reverse('manage_staff'))

        # Check that the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

    def test_manage_staff_view_renders_correct_template(self):
        # Make a GET request to the manage_staff view
        response = self.client.get(reverse('manage_staff'))

        # Check that the response uses the correct template
        self.assertTemplateUsed(response, 'admin_template/manage_staff_template.html')

    def test_manage_staff_view_lists_staff_objects(self):
        # Make a GET request to the manage_staff view
        response = self.client.get(reverse('manage_staff'))

        # Check that the response contains the staff objects
        self.assertContains(response, self.staff1.first_name)
        self.assertContains(response, self.staff2.first_name)

    def test_manage_staff_view_lists_teacher_objects(self):
        # Make a GET request to the manage_staff view
        response = self.client.get(reverse('manage_staff'))

        # Check that the response contains the teacher objects
        self.assertContains(response, self.teacher1.first_name)


class EditStaffTestCase(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = CustomUser.objects.create_user(
            email="admin@test.com", password="testpass", is_admin=True
        )
        self.client.login(email="admin@test.com", password="testpass")

        # Create a staff user to be edited
        self.staff_user = CustomUser.objects.create_user(
            email="staff@test.com", password="testpass", user_type=2
        )
        self.staff_user.staff.address = "123 Main St"
        self.staff_user.save()

    def test_edit_staff(self):
        # Make a GET request to the edit_staff view for the staff user
        response = self.client.get(reverse("edit_staff", args=[self.staff_user.id]))

        # Check that the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # Check that the staff user's data is displayed in the form
        self.assertContains(response, self.staff_user.first_name)
        self.assertContains(response, self.staff_user.last_name)
        self.assertContains(response, self.staff_user.username)
        self.assertContains(response, self.staff_user.email)
        self.assertContains(response, self.staff_user.staff.address)

        # Make a POST request to the edit_staff view with updated data
        response = self.client.post(reverse("edit_staff", args=[self.staff_user.id]), {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "johndoe@example.com",
            "address": "456 Main St"
        })

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the staff user's data was updated in the database
        updated_staff_user = CustomUser.objects.get(id=self.staff_user.id)
        self.assertEqual(updated_staff_user.first_name, "John")
        self.assertEqual(updated_staff_user.last_name, "Doe")
        self.assertEqual(updated_staff_user.username, "johndoe")
        self.assertEqual(updated_staff_user.email, "johndoe@example.com")
        self.assertEqual(updated_staff_user.staff.address, "456 Main St")


class EditStaffSaveTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='admin', password='password'
        )
        self.staff = Staff.objects.create(
            admin=self.user,
            address='123 Main St.'
        )
        self.data = {
            'staff_id': self.staff.id,
            'username': 'newusername',
            'email': 'newemail@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'address': '456 Other St.'
        }
        self.url = reverse('edit_staff_save')

    def test_edit_staff_save_success(self):
        # Log in the user
        self.client.login(username='admin', password='password')

        # Make a POST request to the edit_staff_save view
        response = self.client.post(self.url, self.data)

        # Check that the response is a redirect to the edit_staff view
        self.assertRedirects(response, reverse('edit_staff', args=[self.staff.id]))

        # Check that the staff model was updated
        updated_staff = Staff.objects.get(id=self.staff.id)
        self.assertEqual(updated_staff.address, self.data['address'])

        # Check that the user model was updated
        updated_user = UserList.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, self.data['username'])
        self.assertEqual(updated_user.email, self.data['email'])
        self.assertEqual(updated_user.first_name, self.data['first_name'])
        self.assertEqual(updated_user.last_name, self.data['last_name'])

        # Check that a success message was sent
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Staff Updated Successfully.')

    def test_edit_staff_save_failure(self):
        # Log in the user
        self.client.login(username='admin', password='password')

        # Make a POST request to the edit_staff_save view with invalid data
        invalid_data = self.data.copy()
        invalid_data['email'] = 'not_an_email'
        response = self.client.post(self.url, invalid_data)

        # Check that the response is a redirect to the edit_staff view
        self.assertRedirects(response, reverse('edit_staff', args=[self.staff.id]))

        # Check that the staff and user models were not updated
        staff = Staff.objects.get(id=self.staff.id)
        self.assertEqual(staff.address, self.data['address'])
        user = UserDict.objects.get(id=self.user.id)
        self.assertEqual(user.username, self.user.username)
        self.assertEqual(user.email, self.user.email)
        self.assertEqual(user.first_name, self.user.first_name)
        self.assertEqual(user.last_name, self.user.last_name)

        # Check that an error message was sent
        messages = list(response.context.get('messages'))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Failed to Update Staff.')


class DeleteStaffTestCase(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_user(
            username='admin', password='adminpassword', is_staff=True, is_superuser=True
        )
        self.staff = Staff.objects.create(admin=self.admin, address='Test Address')

    def test_delete_staff(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('delete_staff', args=[self.staff.id]))

        # Check that the response is a redirect to manage_staff view
        self.assertRedirects(response, reverse('manage_staff'))

        # Check that the staff has been deleted
        self.assertFalse(Staff.objects.filter(id=self.staff.id).exists())
        self.assertFalse(CustomUser.objects.filter(id=self.admin.id).exists())

    def test_delete_staff_failure(self):
        self.client.login(username='admin', password='adminpassword')
        response = self.client.post(reverse('delete_staff', args=[999])) # passing invalid staff id

        # Check that the response is a redirect to manage_staff view
        self.assertRedirects(response, reverse('manage_staff'))

        # Check that the staff has not been deleted
        self.assertTrue(Staff.objects.filter(id=self.staff.id).exists())
        self.assertTrue(CustomUser.objects.filter(id=self.admin.id).exists())
        

class AddStudentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user(
            email='testadmin@example.com', password='testpass', is_admin=True
        )

    def test_add_student_view(self):
        # Log in as the user
        self.client.login(email='testadmin@example.com', password='testpass')

        # Make a GET request to the add_student view
        response = self.client.get(reverse('add_student'))

        # Check that the response has a successful status code
        self.assertEqual(response.status_code, 200)

        # Check that the view uses the correct template
        self.assertTemplateUsed(response, 'admin_template/add_student_template.html')

        # Check that the view sets the correct context variables
        self.assertIsInstance(response.context['form'], AddStudentForm)


class AddStudentSaveViewTestCase(TestCase):
    def setUp(self):
        # Set up a test client and create a new admin user
        self.client = Client()
        self.admin_user = CustomUser.objects.create_user(
            username='admin', password='password', email='admin@example.com', user_type=1)

        # Define some student data to use in the tests
        self.student_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'password123',
            'address': '123 Main St',
            'session_year_id': 1,
            'gender': 'M'
        }

        # Create a test session year object
        self.session_year = Session.objects.create(id=1, session_start_year=2022)

        # Create a test institution admin object
        self.institution_admin = admin.objects.create(admin=self.admin_user, institution='My University')
    

    def test_add_student_save_view(self):
        # Log in as the admin user
        self.client.login(username='admin', password='password')

        # Make a POST request to the add_student_save view with the test student data and a test profile picture file
        url = reverse('add_student_save')
        with open('test.jpg', 'rb') as f:
            response = self.client.post(url, data=self.student_data, files={'profile_pic': f})

        # Check that the response status code is 302 (indicating a redirect to the add_student page)
        self.assertEqual(response.status_code, 302)

        # Check that the response redirects to the correct URL
        self.assertRedirects(response, reverse('add_student'))

        # Check that a new user object has been created with the correct data
        self.assertEqual(CustomUser.objects.count(), 2)
        new_student = CustomUser.objects.last()
        self.assertEqual(new_student.username, 'johndoe')
        self.assertEqual(new_student.email, 'johndoe@example.com')
        self.assertEqual(new_student.user_type, 3)  # should be a student
        self.assertEqual(new_student.students.address, '123 Main St')
        self.assertEqual(new_student.students.session_year_id, self.session_year)
        self.assertEqual(new_student.students.gender, 'M')
        self.assertEqual(new_student.students.institution, self.institution_admin.institution)

class ManageStudentViewTest(TestCase):
    def setUp(self):
        # create an admin user
        self.admin_user = User.objects.create_user(
            username='admin',
            password='testpassword',
            is_staff=True,
            is_superuser=True,
        )

    def test_manage_student_view(self):
        # create a test student
        student = Students.objects.create(
            first_name='John',
            last_name='Doe',
            username='jdoe',
            email='jdoe@example.com',
            password='testpassword',
            address='123 Main St',
            session_year_id=1,
            gender='M',
            profile_pic='test.png'
        )
        # simulate a logged-in admin user
        self.client.force_login(self.admin_user)
        # make a GET request to the manage_student view
        response = self.client.get(reverse('manage_student'))
        # assert that the response contains the student's first name
        self.assertContains(response, student.first_name)
        # assert that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

    def test_manage_student_view_unauthenticated(self):
        # simulate an unauthenticated user
        response = self.client.get(reverse('manage_student'))
        # assert that the user is redirected to the login page
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('manage_student'))

    def test_manage_student_view_non_admin(self):
        # create a non-admin user
        user = User.objects.create_user(
            username='user',
            password='testpassword',
            is_staff=False,
            is_superuser=False,
        )
        # simulate a logged-in non-admin user
        self.client.force_login(user)
        # make a GET request to the manage_student view
        response = self.client.get(reverse('manage_student'))
        # assert that the user is redirected to the dashboard
        self.assertRedirects(response, reverse('dashboard'))

class EditStudentViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='admin', password='secret', is_staff=True, is_superuser=True
        )
        self.client.login(username='admin', password='secret')
        self.student = Students.objects.create(
            admin=self.user, address='123 Main St', gender='M'
        )

    def test_edit_student_view(self):
        # Issue a GET request to the edit student page
        url = reverse('edit_student', args=[self.student.id])
        response = self.client.get(url)

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the context contains the student ID, username, and a form
        expected_context = {
            'id': self.student.id,
            'username': self.user.username,
            'form': EditStudentForm(
                initial={
                    'email': self.user.email,
                    'username': self.user.username,
                    'first_name': self.user.first_name,
                    'last_name': self.user.last_name,
                    'address': self.student.address,
                    'class_id': None,  # Replace with actual class ID if applicable
                    'gender': self.student.gender,
                    'session_year_id': None,  # Replace with actual session year ID if applicable
                }
            )
        }
        self.assertDictEqual(response.context, expected_context)

        # Check that the rendered HTML contains the student's username and address
        self.assertContains(response, self.user.username)
        self.assertContains(response, self.student.address)



class TestEditStudent(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            password='password123',
            is_staff=True,
            is_superuser=True
        )
        self.client.login(username='admin', password='password123')
        self.class_ = Class.objects.create(
            name='Class A',
            section='A',
        )
        self.session_year = SessionYear.objects.create(
            session_start_year=2022,
            session_end_year=2023,
        )
        self.student = Students.objects.create(
            admin=self.user,
            address='123 Main St',
            class_id=self.class_,
            gender='M',
            session_year_id=self.session_year,
        )
        self.url = reverse('edit_student', args=[self.student.admin.id])

    def test_get_edit_student(self):
        response = self.client.get(self.url)
        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, EditStudentForm)
        self.assertContains(response, self.student.admin.username)
        self.assertContains(response, self.student.address)
        self.assertContains(response, self.class_.name)
        self.assertContains(response, self.student.gender)
        self.assertContains(response, str(self.session_year))

    def test_post_edit_student(self):
        new_address = '456 Elm St'
        new_gender = 'F'
        new_session_year = SessionYear.objects.create(
            session_start_year=2023,
            session_end_year=2024,
        )
        response = self.client.post(self.url, {
            'address': new_address,
            'class_id': self.class_.id,
            'gender': new_gender,
            'session_year_id': new_session_year.id,
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('manage_student'))
        updated_student = Students.objects.get(admin=self.student.admin)
        self.assertEqual(updated_student.address, new_address)
        self.assertEqual(updated_student.gender, new_gender)
        self.assertEqual(updated_student.session_year_id, new_session_year)




class AdminHomeViewTestCase(TestCase):
    def test_admin_home_view(self):
        # create some test data
        session = Session.objects.create(session_start_year=2022, session_end_year=2023, term='First')
        class_obj = Class.objects.create(class_name='Grade 1')
        student = Students.objects.create(
            first_name="Alice",
            last_name="Smith",
            email="alice.smith@example.com",
            username="alice123",
            address="123 Main St",
            gender="F",
            session_year_id=session,
            class_id=class_obj,
        )
        teacher = Teacher.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            username="johndoe",
            subject="Maths",
        )
        staff = Staff.objects.create(
            first_name="Bob",
            last_name="Johnson",
            email="bob.johnson@example.com",
            username="bjohnson",
            position="Manager",
        )

        # authenticate as an admin user
        User = get_user_model()
        user = User.objects.create_user(username='admin', password='testpass')
        user.is_staff = True
        user.is_superuser = True
        user.save()
        self.client.login(username='admin', password='testpass')

        # make a GET request to the admin home page
        response = self.client.get(reverse("admin_home"))

        # check that the response contains the expected data
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1") # all_student_count
        self.assertContains(response, "1") # staff_count
        self.assertContains(response, "John") # staff_name_list
        self.assertContains(response, "Alice") # student_name_list
        self.assertContains(response, "Bob") # staff_name_list



class DeleteStudentsViewTestCase(TestCase):

    def setUp(self):
        # Create a user with admin privilege
        self.admin_user = User.objects.create_user(
            username="admin", password="adminpassword")
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        # Login as admin
        self.client.login(username="admin", password="adminpassword")

        # Create a sample student
        self.student = Students.objects.create(
            admin=CustomUser.objects.create(username="student1"),
            name="John Doe",
            age=18,
            grade="12"
        )

    def test_delete_student_success(self):
        response = self.client.post(reverse("delete_student", kwargs={"student_id": self.student.id}))
        self.assertEqual(response.status_code, 302)  # expect a redirect
        self.assertRedirects(response, reverse("manage_student"))  # expect a redirect to manage_student
        self.assertFalse(Students.objects.filter(id=self.student.id).exists())  # check that the student is deleted

    def test_delete_student_failure(self):
        # Pass an invalid student ID to simulate a failure
        response = self.client.post(reverse("delete_student", kwargs={"student_id": "invalid_id"}))
        self.assertEqual(response.status_code, 302)  # expect a redirect
        self.assertRedirects(response, reverse("manage_student"))  # expect a redirect to manage_student
        self.assertTrue(Students.objects.filter(id=self.student.id).exists())  # check that the student still exists



class ManageGuardiansViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.manage_guardians_url = reverse("manage_guardians")

    def test_manage_guardians_view(self):
        # create some test data
        Guardian.objects.create(name="John", email="john@example.com")
        Guardian.objects.create(name="Alice", email="alice@example.com")

        # make a GET request to the manage guardians page
        response = self.client.get(self.manage_guardians_url)

        # check that the response contains the expected data
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "John") # guardian name
        self.assertContains(response, "john@example.com") # guardian email
        self.assertContains(response, "Alice") # guardian name
        self.assertContains(response, "alice@example.com") # guardian email

        

class AddGuardianViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(
            username='admin', password='admin123', email='admin@example.com')
        self.client.login(username='admin', password='admin123')

    def test_add_guardian_view(self):
        response = self.client.get(reverse('add_guardian'))

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AddGuardianForm)
        self.assertTemplateUsed(response, 'admin_template/add_guardian_template.html')

    def test_add_guardian_post(self):
        data = {'name': 'John Doe', 'email': 'johndoe@example.com', 'phone': '1234567890'}
        response = self.client.post(reverse('add_guardian'), data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('add_guardian'))
        self.assertEqual(Guardian.objects.count(), 1)
        self.assertEqual(Guardian.objects.first().name, 'John Doe')
        self.assertEqual(Guardian.objects.first().email, 'johndoe@example.com')
        self.assertEqual(Guardian.objects.first().phone, '1234567890')


class AddGuardianSaveViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('add_guardian_save')
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='adminpass',
            user_type=1,
            is_staff=True,
            is_superuser=True
        )
        self.client.login(username='admin', password='adminpass')

         #Test if a new guardian can be added with valid form data
    def test_add_guardian_valid_form(self):
       
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'johndoe',
            'email': 'johndoe@example.com',
            'password': 'johndoe123',
            'phonenumber': '1234567890',
            'bank': 'Example Bank',
            'gender': 'M',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('add_guardian'))
        self.assertEqual(Guardian.objects.count(), 1)
        self.assertEqual(Guardian.objects.first().user.username, 'johndoe')
        self.assertEqual(Guardian.objects.first().phonenumber, '1234567890')
        self.assertEqual(Guardian.objects.first().bank, 'Example Bank')
        self.assertEqual(Guardian.objects.first().gender, 'M')
        self.assertContains(response, 'Guardian Added Successfully!')
        
         #Test if a new guardian cannot be added with invalid form data
    def test_add_guardian_invalid_form(self):
        data = {
            'first_name': '',
            'last_name': '',
            'username': '',
            'email': '',
            'password': '',
            'phonenumber': '',
            'bank': '',
            'gender': '',
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('add_guardian'))
        self.assertEqual(Guardian.objects.count(), 0)
        self.assertContains(response, 'Failed to Add Guardian!')

        #Test if a new guardian cannot be added with invalid HTTP method
    def test_add_guardian_invalid_method(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('add_guardian'))
        self.assertEqual(Guardian.objects.count(), 0)
        self.assertContains(response, 'Invalid Method')
        
        #Test if a new guardian cannot be added by unauthorized user
    def test_add_guardian_unauthorized_access(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin_login')+'?next='+self.url)
        self.assertEqual(Guardian.objects.count(), 0)



class EditGuardianTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Create a test admin user
        self.admin_user = User.objects.create_user(
            username="admin_test_user",
            password="test_password",
            email="admin_test_user@example.com",
        )

        # Create a test guardian user
        self.guardian_user = CustomUser.objects.create_user(
            username="guardian_test_user",
            password="test_password",
            email="guardian_test_user@example.com",
            user_type=5,
        )
        self.guardian = Guardian.objects.create(
            admin=self.guardian_user,
            phonenumber="1234567890",
            bank="Test Bank",
            gender="M",
        )

    def test_edit_guardian_view_with_valid_guardian_id(self):
        """
        Test that the edit_guardian view returns the expected response with a valid guardian ID.
        """
        self.client.login(username="admin_test_user", password="test_password")

        # Use reverse to generate the URL for the edit_guardian view
        url = reverse("edit_guardian", args=[self.guardian.id])

        # Issue a GET request to the URL
        response = self.client.get(url)

        # Check that the response has a 200 status code
        self.assertEqual(response.status_code, 200)

        # Check that the response uses the expected template
        self.assertTemplateUsed(response, "admin_template/edit_guardian_template.html")

        # Check that the response context contains the expected data
        self.assertEqual(response.context["id"], self.guardian.id)
        self.assertEqual(response.context["username"], self.guardian.admin.username)
        self.assertIsInstance(response.context["form"], EditGuardianForm)

    def test_edit_guardian_view_with_invalid_guardian_id(self):
        """
        Test that the edit_guardian view returns a 404 response with an invalid guardian ID.
        """
        self.client.login(username="admin_test_user", password="test_password")

        # Use an invalid guardian ID for the URL
        url = reverse("edit_guardian", args=[999])

        # Issue a GET request to the URL
        response = self.client.get(url)

        # Check that the response has a 404 status code
        self.assertEqual(response.status_code, 404)

    def test_edit_guardian_view_with_unauthenticated_user(self):
        """
        Test that the edit_guardian view redirects to the login page for an unauthenticated user.
        """
        # Use a valid guardian ID for the URL
        url = reverse("edit_guardian", args=[self.guardian.id])

        # Issue a GET request to the URL
        response = self.client.get(url)

        # Check that the response has a 302 status code
        self.assertEqual(response.status_code, 302)

        # Check that the response redirects to the expected URL (the login page)
        self.assertRedirects(response, "/accounts/login/?next=" + url)


class TestDeleteStudentView(TestCase):
    def setUp(self):
        # create an admin user for authentication
        self.admin = User.objects.create_user(username='admin', password='pass')
        self.admin.is_staff = True
        self.admin.is_superuser = True
        self.admin.save()

        # create a guardian to be deleted
        self.guardian = Guardian.objects.create(
            admin=self.admin,
            phonenumber='1234567890',
            bank='Bank of America',
            gender='M'
        )

        # create a client and login as admin
        self.client = Client()
        self.client.login(username='admin', password='pass')

    def test_delete_student(self):
        # get the url for deleting the guardian
        url = reverse('delete_student', args=[self.guardian.id])

        # make a POST request to delete the guardian
        response = self.client.post(url)

        # check that the guardian was deleted successfully
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('manage_guardians'))
        self.assertFalse(Guardian.objects.filter(admin=self.admin).exists())
        self.assertContains(response, "Guardian Deleted Successfully.")

    def test_delete_student_invalid_id(self):
        # get the url for deleting a guardian with an invalid id
        url = reverse('delete_student', args=[999])

        # make a POST request to delete the guardian
        response = self.client.post(url)

        # check that the guardian was not deleted and an error message is displayed
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('manage_guardians'))
        self.assertTrue(Guardian.objects.filter(admin=self.admin).exists())
        self.assertContains(response, "Failed to Delete Guardian.")

    def test_delete_student_not_authenticated(self):
        # create a new client without authentication
        client = Client()

        # get the url for deleting the guardian
        url = reverse('delete_student', args=[self.guardian.id])

        # make a POST request to delete the guardian
        response = client.post(url)

        # check that the user is redirected to the login page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/login/?next=' + url)

        # check that the guardian was not deleted and an error message is displayed
        self.assertTrue(Guardian.objects.filter(admin=self.admin).exists())
        self.assertContains(response, "Please login to continue.")



class ManageHodsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create an admin user
        admin_user = User.objects.create_user(username="admin", password="adminpassword")
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        
        # Create a HOD
        HOD.objects.create(admin=admin_user, department="Computer Science")

    def setUp(self):
        # Log in the admin user for each test
        self.client = Client()
        logged_in = self.client.login(username="admin", password="adminpassword")
        self.assertTrue(logged_in)

    def test_manage_hods_view(self):
        # Test that the manage_hods view returns a 200 OK status code
        response = self.client.get(reverse("manage_hods"))
        self.assertEqual(response.status_code, 200)

        # Test that the correct template is used
        self.assertTemplateUsed(response, "admin_template/manage_hod_template.html")

        # Test that the HOD is in the context
        hods = response.context["hod"]
        self.assertEqual(len(hods), 1)
        self.assertEqual(hods[0].department, "Computer Science")

    def test_manage_hods_view_not_logged_in(self):
        # Test that the user is redirected to the login page if not logged in
        self.client.logout()
        response = self.client.get(reverse("manage_hods"))
        self.assertRedirects(response, "/accounts/login/?next=/manage_hods/")

    def test_manage_hods_view_not_admin(self):
        # Create a non-admin user and test that they are redirected to the home page
        user = User.objects.create_user(username="testuser", password="testpassword")
        logged_in = self.client.login(username="testuser", password="testpassword")
        self.assertTrue(logged_in)
        response = self.client.get(reverse("manage_hods"))
        self.assertRedirects(response, "/")

    def test_manage_hods_view_no_hods(self):
        # Test that the manage_hods view returns an empty list if there are no HODs
        HOD.objects.all().delete()
        response = self.client.get(reverse("manage_hods"))
        hods = response.context["hod"]
        self.assertEqual(len(hods), 0)


# define the test class
class TestAddHodView(TestCase):
    
    # define the setup method to be executed before every test
    def setUp(self):
        self.client = Client()
        self.admin_user = CustomUser.objects.create_user(
            username='admin', password='adminpassword', user_type=1)
        self.client.login(username='admin', password='adminpassword')
        self.url = reverse('add_hod')
        self.hod_info = {
            'email': 'hodemail@test.com',
            'username': 'hodusername',
            'first_name': 'John',
            'last_name': 'Doe',
            'department': 'Computer Science',
            'gender': 'Male',
            'profile_pic': '',
            'password1': 'testpassword',
            'password2': 'testpassword'
        }

    # define the test method to test the add_hod view
    def test_add_hod_view(self):
        response = self.client.get(self.url)

        # assert that the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # assert that the correct template is used
        self.assertTemplateUsed(response, 'admin_template/add_hod_template.html')

        # assert that the form used in the template is an instance of AddHodForm
        self.assertIsInstance(response.context['form'], AddHodForm)

        # make a post request with the hod information
        response = self.client.post(self.url, self.hod_info, format='multipart')

        # assert that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # assert that the hod is added to the database
        self.assertTrue(HOD.objects.filter(admin__email='hodemail@test.com').exists())

        # assert that the hod's user type is set to 2 (HOD)
        hod_user = CustomUser.objects.get(email='hodemail@test.com')
        self.assertEqual(hod_user.user_type, 2)

        # assert that a success message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'HOD Added Successfully!')

    # define the test method to test the add_hod view with invalid data
    def test_add_hod_view_with_invalid_data(self):
        # set hod email to an invalid email format
        self.hod_info['email'] = 'invalidemail'

        # make a post request with the hod information containing invalid email
        response = self.client.post(self.url, self.hod_info, format='multipart')

        # assert that the response status code is 200 (success)
        self.assertEqual(response.status_code, 200)

        # assert that the form used in the template is an instance of AddHodForm
        self.assertIsInstance(response.context['form'], AddHodForm)

        # assert that a form error message is displayed
        form = response.context['form']
        self.assertTrue(form.has_error('email'))

        # assert that the hod is not added to the database
        self.assertFalse(HOD.objects.filter(admin__email='invalidemail').exists())

        # assert that no success message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 0)



class EditHodTestCase(TestCase):
    def setUp(self):
        # Creating an admin user for testing purposes
        self.admin_user = User.objects.create_user(
            username="testadmin",
            password="testpass123",
            email="testadmin@test.com",
            first_name="Test",
            last_name="Admin",
        )
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        # Creating a HOD user for testing purposes
        self.hod_user = User.objects.create_user(
            username="testhod",
            password="testpass123",
            email="testhod@test.com",
            first_name="Test",
            last_name="HOD",
        )
        self.hod = HOD.objects.create(
            admin=self.hod_user, department="Test Department", phonenumber="1234567890"
        )

    def test_edit_hod(self):
        # Logging in as admin
        self.client.login(username="testadmin", password="testpass123")

        # Navigating to edit HOD page
        response = self.client.get(reverse("edit_hod", args=[self.hod.admin.id]))

        # Checking if the status code is OK
        self.assertEqual(response.status_code, 200)

        # Checking if the context contains the necessary form fields
        self.assertIn("form", response.context)
        form = response.context["form"]
        self.assertIn("email", form.fields)
        self.assertIn("username", form.fields)
        self.assertIn("first_name", form.fields)
        self.assertIn("last_name", form.fields)
        self.assertIn("phonenumber", form.fields)

        # Filling the form with new data
        data = {
            "email": "newtesthod@test.com",
            "username": "newtesthod",
            "first_name": "New Test",
            "last_name": "HOD",
            "phonenumber": "0987654321",
        }
        response = self.client.post(reverse("edit_hod", args=[self.hod.admin.id]), data=data)

        # Checking if the HOD data has been updated in the database
        self.hod.refresh_from_db()
        self.assertEqual(self.hod.admin.email, "newtesthod@test.com")
        self.assertEqual(self.hod.admin.username, "newtesthod")
        self.assertEqual(self.hod.admin.first_name, "New Test")
        self.assertEqual(self.hod.admin.last_name, "HOD")
        self.assertEqual(self.hod.phonenumber, "0987654321")

        # Checking if the response is a redirect to the manage HODs page
        self.assertRedirects(response, reverse("manage_hods"))



class EditHodSaveTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a test admin user
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@test.com', password='password'
        )
        # Create a test HOD
        self.hod = HOD.objects.create(
            admin=self.admin, department='Test Department', phonenumber='1234567890'
        )

    def test_edit_hod_save_POST(self):
        # Log in as admin
        self.client.login(username='admin', password='password')

        # Make a POST request to the edit_hod_save URL with form data
        response = self.client.post(reverse('edit_hod_save'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@test.com',
            'username': 'johndoe',
            'phonenumber': '9876543210'
        })

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the HOD object was updated with the new data
        self.hod.refresh_from_db()
        self.assertEqual(self.hod.admin.first_name, 'John')
        self.assertEqual(self.hod.admin.last_name, 'Doe')
        self.assertEqual(self.hod.admin.email, 'johndoe@test.com')
        self.assertEqual(self.hod.admin.username, 'johndoe')
        self.assertEqual(self.hod.phonenumber, '9876543210')

    def test_edit_hod_save_GET(self):
        # Log in as admin
        self.client.login(username='admin', password='password')

        # Make a GET request to the edit_hod_save URL
        response = self.client.get(reverse('edit_hod_save'))

        # Check that the response status code is 405 (method not allowed)
        self.assertEqual(response.status_code, 405)

    def test_edit_hod_save_invalid_form_data(self):
        # Log in as admin
        self.client.login(username='admin', password='password')

        # Make a POST request to the edit_hod_save URL with invalid form data
        response = self.client.post(reverse('edit_hod_save'), {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@test.com',
            'username': 'johndoe',
            'phonenumber': 'invalid_phone_number'
        })

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the HOD object was not updated
        self.hod.refresh_from_db()
        self.assertNotEqual(self.hod.admin.first_name, 'John')
        self.assertNotEqual(self.hod.admin.last_name, 'Doe')
        self.assertNotEqual(self.hod.admin.email, 'johndoe@test.com')
        self.assertNotEqual(self.hod.admin.username, 'johndoe')
        self.assertNotEqual(self.hod.phonenumber, 'invalid_phone_number')



class DeleteHodTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # create admin user
        self.admin_user = User.objects.create_user(username='admin', password='testpassword')
        self.admin_group = Group.objects.create(name='admin')
        self.admin_group.user_set.add(self.admin_user)

        # create hod user
        self.hod_user = User.objects.create_user(username='hod', password='testpassword')
        self.hod_group = Group.objects.create(name='hod')
        self.hod_group.user_set.add(self.hod_user)

        # create hod object
        self.hod = HOD.objects.create(admin=self.hod_user, department='Test Department', phonenumber='123456789')

    def test_delete_hod(self):
        # log in as admin
        self.client.login(username='admin', password='testpassword')

        # delete hod
        response = self.client.post(reverse('delete_hod', args=[self.hod.id]))

        # assert that the response is a redirect
        self.assertEqual(response.status_code, 302)

        # assert that the hod has been deleted
        with self.assertRaises(HOD.DoesNotExist):
            HOD.objects.get(admin=self.hod_user)

        # assert that a success message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'HOD Deleted Successfully.')

    def test_delete_hod_unauthenticated(self):
        # delete hod without logging in
        response = self.client.post(reverse('delete_hod', args=[self.hod.id]))

        # assert that the response is a redirect to login
        self.assertRedirects(response, '/accounts/login/?next=/delete_hod/' + str(self.hod.id))

        # assert that the hod has not been deleted
        self.assertTrue(HOD.objects.filter(admin=self.hod_user).exists())

        # assert that an error message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You must be logged in as an admin to delete a HOD.')

    def test_delete_hod_unauthorized(self):
        # log in as hod
        self.client.login(username='hod', password='testpassword')

        # delete hod
        response = self.client.post(reverse('delete_hod', args=[self.hod.id]))

        # assert that the response is a redirect to dashboard
        self.assertRedirects(response, '/dashboard/')

        # assert that the hod has not been deleted
        self.assertTrue(HOD.objects.filter(admin=self.hod_user).exists())

        # assert that an error message is displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'You do not have permission to delete a HOD.')


class ManageDepartmentsTestCase(TestCase):
    
    def setUp(self):
        # Create a test admin user
        self.admin_user = CustomUser.objects.create_user(
            email="admin@test.com",
            password="testpass123",
            is_admin=True
        )

    def test_manage_departments(self):
        # Create a test department
        department = Department.objects.create(name="Test Department")

        # Log in as admin
        self.client.login(email="admin@test.com", password="testpass123")

        # Send a GET request to the manage departments page
        response = self.client.get("/manage_departments/")

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the test department is in the context
        self.assertIn(department, response.context["department"])

        # Check that the manage_department_template.html template is used in the response
        self.assertTemplateUsed(response, "admin_template/manage_department_template.html")



class AddDepartmentTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # create admin user
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword')
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        # create HOD user
        self.hod_user = User.objects.create_user(username='hod', password='hodpassword')
        self.hod_user.is_staff = True
        self.hod_user.save()
        self.hod = HOD.objects.create(admin=self.hod_user)

        # create staff user
        self.staff_user = User.objects.create_user(username='staff', password='staffpassword')
        self.staff_user.is_staff = True
        self.staff_user.save()
        self.staff = Staff.objects.create(admin=self.staff_user)

    def test_add_department_view_with_admin(self):
        # authenticate admin user
        self.client.login(username='admin', password='adminpassword')

        # send post request to add department
        response = self.client.post(reverse('add_department'), {
            'department_name': 'Test Department',
            'department_code': 'TEST',
            'department_hod': self.hod.id,
            'department_staff': [self.staff.id],
        })

        # check if department is created
        department = Department.objects.filter(department_name='Test Department', department_code='TEST')
        self.assertEqual(department.count(), 1)

        # check if department hod and staff are assigned
        department = department.first()
        self.assertEqual(department.department_hod, self.hod)
        self.assertEqual(list(department.department_staff.all()), [self.staff])

        # check if response is redirecting to manage departments
        self.assertRedirects(response, reverse('manage_departments'))

    def test_add_department_view_with_non_admin(self):
        # authenticate staff user
        self.client.login(username='staff', password='staffpassword')

        # send post request to add department
        response = self.client.post(reverse('add_department'), {
            'department_name': 'Test Department',
            'department_code': 'TEST',
            'department_hod': self.hod.id,
            'department_staff': [self.staff.id],
        })

        # check if department is not created
        department = Department.objects.filter(department_name='Test Department', department_code='TEST')
        self.assertEqual(department.count(), 0)

        # check if response is redirecting to home page
        self.assertRedirects(response, reverse('home'))



class TestAddDepartmentSaveView(TestCase):

    def setUp(self):
        # Create a test user with admin privilege
        self.admin_user = User.objects.create_user(
            username='admin_user',
            password='testpass123',
            is_staff=True,
            is_superuser=True,
        )
        # Create HOD and Staff objects for testing
        self.hod = HOD.objects.create(
            admin=self.admin_user,
            name='Test HOD',
            email='test_hod@test.com',
        )
        self.staff = Staff.objects.create(
            admin=self.admin_user,
            name='Test Staff',
            email='test_staff@test.com',
        )
    
    def test_add_department_save_view_post(self):
        # Log in as admin user
        self.client.login(username='admin_user', password='testpass123')
        # Make a POST request to add a new department
        response = self.client.post(reverse('add_department_save'), {
            'name': 'Test Department',
            'desc': 'Test Department Description',
            'head': self.hod.admin.id,
            'deputy': self.staff.admin.id,
        })
        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        # Check that the department was created successfully
        self.assertTrue(Department.objects.filter(name='Test Department').exists())
        # Check that the success message was displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Department Added Successfully!')
    
    def test_add_department_save_view_invalid_method(self):
        # Log in as admin user
        self.client.login(username='admin_user', password='testpass123')
        # Make a GET request to add a new department (invalid method)
        response = self.client.get(reverse('add_department_save'))
        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        # Check that the error message was displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Invalid Method ')
    
    def test_add_department_save_view_unauthenticated_user(self):
        # Make a POST request to add a new department (unauthenticated user)
        response = self.client.post(reverse('add_department_save'), {
            'name': 'Test Department',
            'desc': 'Test Department Description',
            'head': self.hod.admin.id,
            'deputy': self.staff.admin.id,
        })
        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)
        # Check that the department was not created
        self.assertFalse(Department.objects.filter(name='Test Department').exists())
        # Check that the user was redirected to the login page
        self.assertRedirects(response, '/accounts/login/?next=' + reverse('add_department_save'))


class TestEditDepartment(TestCase):
    def setUp(self):
        # create a test admin user
        self.admin = User.objects.create_user(
            username='test_admin',
            email='test_admin@example.com',
            password='test_password'
        )
        self.admin.is_staff = True
        self.admin.is_superuser = True
        self.admin.save()

        # create a test HOD
        self.hod = HOD.objects.create(
            admin=self.admin,
            name='Test HOD',
            email='test_hod@example.com',
            password='test_password',
            address='Test Address'
        )

        # create a test staff member
        self.staff = Staff.objects.create(
            admin=self.admin,
            name='Test Staff',
            email='test_staff@example.com',
            password='test_password',
            address='Test Address',
            phone='1234567890'
        )

        # create a test department
        self.department = Department.objects.create(
            name='Test Department',
            desc='Test Description',
            head=self.hod,
            deputy=self.staff
        )

    def test_get_edit_department_page(self):
        # test that a GET request to the edit_department page returns the correct template and context data
        self.client.force_login(self.admin)
        response = self.client.get(reverse('edit_department', args=[self.department.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_template/edit_department_template.html')
        self.assertEqual(response.context['department'], self.department)
        self.assertEqual(response.context['department_id'], self.department.id)
        self.assertQuerysetEqual(response.context['staff'], ['<Staff: Test Staff>'])
        self.assertQuerysetEqual(response.context['hod'], ['<HOD: Test HOD>'])

    def test_edit_department_success(self):
        # test that a POST request to the edit_department page with valid data successfully edits the department
        self.client.force_login(self.admin)
        response = self.client.post(reverse('edit_department', args=[self.department.id]), {
            'name': 'New Department Name',
            'desc': 'New Department Description',
            'head': self.hod.id,
            'deputy': self.staff.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('edit_department', args=[self.department.id]))
        self.department.refresh_from_db()
        self.assertEqual(self.department.name, 'New Department Name')
        self.assertEqual(self.department.desc, 'New Department Description')
        self.assertEqual(self.department.head, self.hod)
        self.assertEqual(self.department.deputy, self.staff)

    def test_edit_department_failure(self):
        # test that a POST request to the edit_department page with invalid data fails to edit the department
        self.client.force_login(self.admin)
        response = self.client.post(reverse('edit_department', args=[self.department.id]), {
            'name': '',
            'desc': 'New Department Description',
            'head': self.hod.id,
            'deputy': self.staff.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('edit_department', args=[self.department.id]))
        self.department.refresh_from_db()
        self.assertNotEqual(self.department.desc, 'New Department Description')



class EditDepartmentSaveTest(TestCase):
    def setUp(self):
        self.client = Client()

        # Create an admin user for testing
        self.admin_user = User.objects.create_user(
            username='admin',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )

        # Create some test data for the departments, staff and HODs
        self.department = Department.objects.create(
            name='Test Department',
            desc='This is a test department'
        )

        self.staff = Staff.objects.create(
            admin=self.admin_user,
            name='Test Staff',
            email='test_staff@test.com',
            password='test123'
        )

        self.hod = HOD.objects.create(
            admin=self.admin_user,
            department=self.department,
            name='Test HOD',
            email='test_hod@test.com',
            password='test123'
        )

    def test_edit_department_save_with_valid_data(self):
        # Log in as admin user
        self.client.login(username='admin', password='admin123')

        # Make a POST request with valid data to edit the department
        response = self.client.post(
            reverse('edit_department_save'),
            {
                'name': 'Updated Department Name',
                'desc': 'This is an updated department',
                'head': self.hod.admin.id,
                'deputy': self.staff.admin.id,
                'department_id': self.department.id
            }
        )

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the department was updated with the new data
        updated_department = Department.objects.get(id=self.department.id)
        self.assertEqual(updated_department.name, 'Updated Department Name')
        self.assertEqual(updated_department.desc, 'This is an updated department')
        self.assertEqual(updated_department.head, self.hod)
        self.assertEqual(updated_department.deputy, self.staff)

        # Check that a success message was displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Department upated Successfully!')

    def test_edit_department_save_with_invalid_data(self):
        # Log in as admin user
        self.client.login(username='admin', password='admin123')

        # Make a POST request with invalid data (department ID doesn't exist)
        response = self.client.post(
            reverse('edit_department_save'),
            {
                'name': 'Updated Department Name',
                'desc': 'This is an updated department',
                'head': self.hod.admin.id,
                'deputy': self.staff.admin.id,
                'department_id': 9999
            }
        )

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the department was not updated
        not_updated_department = Department.objects.get(id=self.department.id)
        self.assertNotEqual(not_updated_department.name, 'Updated Department Name')
        self.assertNotEqual(not_updated_department.desc, 'This is an updated department')
        self.assertNotEqual(not_updated_department.head, self.hod)
        self.assertNotEqual(not_updated_department.deputy, self.staff)

        # Check that an error message was displayed
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Failed to upate Department!')




class ManageSessionTestCase(TestCase):
    
    # Define a setUp method to set up the test client, admin user, and session object
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword')
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
        self.client.login(username='admin', password='adminpassword')
        self.session = Session.objects.create(session_start_year=2022, session_end_year=2023)

    # Define a test method to test if the manage session page loads successfully and displays the created session
    def test_manage_session_page(self):
        response = self.client.get(reverse('manage_session'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_template/manage_session_template.html')
        self.assertContains(response, '2022-2023')

    # Define a test method to test if the manage session page displays a message when there are no sessions available
    def test_manage_session_page_with_no_sessions(self):
        # Delete the session object created in the setUp method
        self.session.delete()
        # Send a GET request to the manage session page
        response = self.client.get(reverse('manage_session'))
        # Assert that the page loads successfully, uses the correct template, and displays the message "No session available"
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_template/manage_session_template.html')
        self.assertContains(response, 'No session available')

    # Define a test method to test if an unauthorized user is redirected to the login page when trying to access the manage session page
    def test_manage_session_page_unauthorized_access(self):
        # Log out the admin user
        self.client.logout()
        # Send a GET request to the manage session page
        response = self.client.get(reverse('manage_session'))
        # Assert that the user is redirected to the login page with the correct redirect URL
        self.assertRedirects(response, '/login/?next=/manage_session/')

   

class AddSessionTestCase(TestCase):
    
    def setUp(self):
        # Create a client to simulate a user interacting with the application
        self.client = Client()

        # Create an admin user to log in to the application
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword')
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

        # Log in as the admin user
        self.client.login(username='admin', password='adminpassword')

    def test_add_session_page(self):
        # Test that the add session page is accessible
        response = self.client.get(reverse('add_session'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_template/add_session_template.html')

    def test_add_session_page_unauthorized_access(self):
        # Test that a non-logged in user is redirected to the login page when trying to access the add session page
        self.client.logout()
        response = self.client.get(reverse('add_session'))
        self.assertRedirects(response, '/login/?next=/add_session/')
 


class AddSessionSaveTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword')
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
        self.client.login(username='admin', password='adminpassword')

    def test_add_session_save_with_valid_data(self):
        #Tests the add_session_save view with valid POST data and expects a successful session year creation
        response = self.client.post(reverse('add_session_save'), data={
            'session_start_date': '2023-09-01',
            'session_end_date': '2024-06-30',
            'is_current': 'on',
        })
        self.assertEqual(response.status_code, 302)  # Expects a redirect after POST
        self.assertRedirects(response, reverse('add_session'))  # Redirects to the add_session page
        self.assertEqual(Session.objects.count(), 1)  # Expects one session to be created
        session = Session.objects.first()  # Get the created session
        self.assertEqual(session.session_start_date.year, 2023)  # Expects the correct start year
        self.assertEqual(session.session_end_date.year, 2024)  # Expects the correct end year
        self.assertTrue(session.is_current)  # Expects is_current to be True

    def test_add_session_save_with_invalid_data(self):
        #Tests the add_session_save view with invalid POST data and expects error messages
        response = self.client.post(reverse('add_session_save'), data={
            'session_start_date': '2023-09-01',
            'session_end_date': '',
            'is_current': 'on',
        })
        self.assertEqual(response.status_code, 302)  # Expects a redirect after POST
        self.assertRedirects(response, reverse('add_session'))  # Redirects to the add_session page
        self.assertEqual(Session.objects.count(), 0)  # Expects no session to be created
        messages = list(response.wsgi_request._messages)  # Get the messages after the redirect
        self.assertEqual(len(messages), 1)  # Expects one message to be displayed
        self.assertEqual(str(messages[0]), "Failed to Add Session Year Due to incomplete or incorrect entry of fields (i.e {'session_end_date': ['This field is required.']})")  # Expects the correct error message

    def test_add_session_save_with_no_post_data(self):
        #Tests the add_session_save view with no POST data and expects a redirect with error message
        response = self.client.get(reverse('add_session_save'))
        self.assertEqual(response.status_code, 302)  # Expects a redirect after GET
        self.assertRedirects(response, reverse('add_session'))  # Redirects to the add_session page
        messages = list(response.wsgi_request._messages)  # Get the messages after the redirect
        self.assertEqual(len(messages), 1)  # Expects one message to be displayed
        self.assertEqual(str(messages[0]), "Invalid Method")  # Expects the correct error message



class EditSessionTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(username='admin', password='adminpassword')
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()
        self.client.login(username='admin', password='adminpassword')
        self.session_year = Session.objects.create(
            session_start_date='2023-09-01',
            session_end_date='2024-06-30',
            is_current=True
        )

    def test_edit_session_with_valid_session_id(self):
        #Tests the edit_session view with a valid session ID and expects a successful render of the edit session template
        response = self.client.get(reverse('edit_session', args=[self.session_year.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_template/edit_session_template.html')
        self.assertEqual(response.context['session_year'], self.session_year)

    def test_edit_session_with_invalid_session_id(self):
        #Tests the edit_session view with an invalid session ID and expects a redirect with an error message

        response = self.client.get(reverse('edit_session', args=[100]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('session_years'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Session year not found.")

    def test_edit_session_with_no_session_id(self):
        #Tests the edit_session view with no session ID and expects a redirect with an error message

        response = self.client.get(reverse('edit_session'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('session_years'))
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Session year not found.")



class EditSessionSaveViewTest(TestCase):
    def test_edit_session_save_view(self):
        # Create a session year
        session_year = Session.objects.create(
            session_start_year=2022,
            session_end_year=2023,
            is_current=True
        )

        # Create a POST request with updated session year details
        data = {
            'session_id': session_year.id,
            'session_start_year': 2021,
            'session_end_year': 2022,
            'is_current': 'on'
        }
        response = self.client.post(reverse('edit_session_save'), data=data)

        # Check that the session year was updated
        self.assertEqual(response.status_code, 302)
        updated_session_year = Session.objects.get(id=session_year.id)
        self.assertEqual(updated_session_year.session_start_year, 2021)
        self.assertEqual(updated_session_year.session_end_year, 2022)
        self.assertTrue(updated_session_year.is_current)

        # Try to update session year with invalid data
        invalid_data = {
            'session_id': session_year.id,
            'session_start_year': '',
            'session_end_year': '',
            'is_current': ''
        }
        response = self.client.post(reverse('edit_session_save'), data=invalid_data)
        self.assertEqual(response.status_code, 302)

        # Check that the session year was not updated
        updated_session_year = Session.objects.get(id=session_year.id)
        self.assertEqual(updated_session_year.session_start_year, 2021)
        self.assertEqual(updated_session_year.session_end_year, 2022)
        self.assertTrue(updated_session_year.is_current)



class DeleteSessionViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='testuser', password='testpass')
        user.is_staff = True
        user.is_superuser = True
        user.save()

    def setUp(self):
        self.client.login(username='testuser', password='testpass')

    def test_delete_session_success(self):
        # Create a session year
        session_year = Session.objects.create(
            session_start_year=2022,
            session_end_year=2023,
            is_current=True
        )

        # Send a DELETE request to delete the session year
        response = self.client.delete(reverse('delete_session', args=[session_year.id]))

        # Check that the session year was deleted and a success message is displayed
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Session.objects.filter(id=session_year.id).exists())
        self.assertContains(response, "Session Deleted Successfully.")

    def test_delete_session_failure(self):
        # Try to delete a non-existent session year
        response = self.client.delete(reverse('delete_session', args=[100]))

        # Check that the session year was not deleted and an error message is displayed
        self.assertEqual(response.status_code, 302)
        self.assertContains(response, "Failed to Delete Session.")


class TestCheckEmailExist(TestCase):
        # Define the setup method that will run before each test
    def setUp(self):
        self.client = Client()
        self.url = reverse('check_email_exist')

        # Test case for when email exists in the database
    def test_email_exists(self):
        # Create a user object
        user = CustomUser.objects.create(
        email='test@example.com',
        password='password123'
    )

        # Make a POST request to the check_email_exist view with the email of the user created
        response = self.client.post(self.url, {'email': user.email})

        # Assert that the status code is 200 and the response content is 'true'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'true')

        # Test case for when email does not exist in the database
    def test_email_does_not_exist(self):
        # Make a POST request to the check_email_exist view with a nonexistent email
        response = self.client.post(self.url, {'email': 'nonexistent@example.com'})

        # Assert that the status code is 200 and the response content is 'false'
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'false')


class TestCheckUsernameExist(TestCase):
        # Set up the test client and URL
    def setUp(self):
        self.client = Client()
        self.url = reverse('check_username_exist')

        # Test if the username exists in the database
    def test_username_exists(self):
        user = CustomUser.objects.create(
        username='testuser',
        email='test@example.com',
        password='password123'
    )
        response = self.client.post(self.url, {'username': user.username})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'true')

        # Test if the username does not exist in the database
    def test_username_does_not_exist(self):
        response = self.client.post(self.url, {'username': 'nonexistentuser'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'false')

        # Test if an empty username is submitted
    def test_empty_username(self):
        response = self.client.post(self.url, {'username': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'false')

        # Test if a whitespace-only username is submitted
    def test_whitespace_username(self):
        response = self.client.post(self.url, {'username': '   '})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'false')

