from collections import UserDict, UserList
from django.test import TestCase,  Client
from django.urls import reverse
from academics.models import Session
from core import admin
from core.forms.institutionform import InstitutionForm
from core.forms.studentforms import AddStudentForm, EditStudentForm
from core.models import CustomUser,get_user_model, Teacher, Students, Staff

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


class EditStudentTestCase(TestCase):
    def setUp(self):
        # Set up the request factory and test client
        self.factory = RequestFactory()
        self.client = Client()

        # Create an admin user for testing
        self.admin_user = User.objects.create_user(username="testadmin", password="testpassword", is_staff=True, is_superuser=True)
        self.client.login(username="testadmin", password="testpassword")

        # Create a student for testing
        self.student = Students.objects.create(
            admin=self.admin_user,
            address="123 Main St",
            class_id=1,
            gender="M",
            session_year_id=1
        )

    def test_edit_student_form_initial_data(self):
        # Get the edit student page for the created student
        response = self.client.get(reverse("edit_student", kwargs={"student_id": self.student.admin.id}))

        # Check that the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Check that the form initial data is correctly filled from the database
        form = response.context["form"]
        self.assertEqual(form.fields["email"].initial, self.admin_user.email)
        self.assertEqual(form.fields["username"].initial, self.admin_user.username)
        self.assertEqual(form.fields["first_name"].initial, self.admin_user.first_name)
        self.assertEqual(form.fields["last_name"].initial, self.admin_user.last_name)
        self.assertEqual(form.fields["address"].initial, self.student.address)
        self.assertEqual(form.fields["class_id"].initial, self.student.class_id.id)
        self.assertEqual(form.fields["gender"].initial, self.student.gender)
        self.assertEqual(form.fields["session_year_id"].initial, self.student.session_year_id.id)

    def test_edit_student_form_submission(self):
        # Submit a form to edit the created student
        form_data = {
            "email": "newemail@example.com",
            "username": "newusername",
            "first_name": "New",
            "last_name": "Name",
            "address": "456 Elm St",
            "class_id": 2,
            "gender": "F",
            "session_year_id": 2
        }
        response = self.client.post(reverse("edit_student", kwargs={"student_id": self.student.admin.id}), form_data)

        # Check that the response redirects to the manage student page
        self.assertRedirects(response, reverse("manage_student"))

        # Check that the student data was updated correctly in the database
        updated_student = Students.objects.get(id=self.student.id)
        self.assertEqual(updated_student.admin.email, form_data["email"])
        self.assertEqual(updated_student.admin.username, form_data["username"])
        self.assertEqual(updated_student.admin.first_name, form_data["first_name"])
        self.assertEqual(updated_student.admin.last_name, form_data["last_name"])
        self.assertEqual(updated_student.address, form_data["address"])
        self.assertEqual(updated_student.class_id.id, form_data["class_id"])
        self.assertEqual(updated_student.gender, form_data["gender"])
        self.assertEqual(updated_student.session_year_id.id, form_data["session_year_id"])
