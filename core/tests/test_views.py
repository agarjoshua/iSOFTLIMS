from django.test import TestCase,  Client
from django.urls import reverse
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
        self.user = User.objects.create_user(
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
