from django.test import TestCase,  Client
from django.urls import reverse
from core.forms.institutionform import InstitutionForm
from core.models import CustomUser, Teacher, Students, Staff

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
        updated_user = User.objects.get(id=self.user.id)
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
        user = User.objects.get(id=self.user.id)
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
