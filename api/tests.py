from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class ApiTestBase(TestCase):
    def get_url(self, action="list", **kwargs):
        return reverse(f"api:api-user-{action}", kwargs={**kwargs})

    def create_user(
        first_name="jhon",
        last_name="doe",
        username="jhondoe",
        email="jhondoe@email.com",
        birth_date="1990-12-01",
        password="P@ssword123"
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            birth_date=birth_date,
            password=password,
        )

    def create_many_users(self, amount=5):
        user_list = []
        for i in range(0, amount):
            values = {
                "last_name": f"LastName{i+1}",
                "username": f"username{i+1}",
                "email": f"email{i+1}@email.com",
                "birth_date": "1995-11-09",
                "password": "P@ssword123",
            }
            user = self.create_user(**values)
            user_list.append(user)
        return user_list

    def get_tokens(self, authentication_field=None, password=None):
        if not authentication_field or not password:
            user = self.create_user()
        response = self.client.post(
            reverse("api:token_obtain_pair"),
            {
                "authentication_field": "jhondoe@email.com" or authentication_field,
                "password": "P@ssword123" or password,
            },
        )
        return {
            "access": response.data.get("access"),
            "refresh": response.data.get("refresh"),
            "user": user
        }

    def refresh_token(self, refresh_token):
        response = self.client.post(
            reverse("api:token_refresh"), {"refresh": refresh_token}
        )
        return response.data.get("access")

    def verify_token(self, access_token):
        response = self.client.post(
            reverse("api:token_verify"), {"token": access_token}
        )
        return response.status_code


class ApiTest(ApiTestBase):
    def test_if_a_unregistered_user_cant_obtain_token_pair(self):
        tokens = self.get_tokens(
            authentication_field="test@email.com", password="Anypassword"
        )
        self.assertIsNone(tokens.get("access"))
        self.assertIsNone(tokens.get("refresh"))

    def test_if_a_registesred_user_can_obtain_token_pair(self):
        tokens = self.get_tokens()
        self.assertIsNotNone(tokens.get("access"))
        self.assertIsNotNone(tokens.get("refresh"))

    def test_if_a_registered_user_receives_a_valid_token(self):
        tokens = self.get_tokens()
        status_code = self.verify_token(tokens.get("access"))
        self.assertEqual(status_code, 200)

    def test_if_a_registesred_user_can_refresh_access_token(self):
        tokens = self.get_tokens()
        access_after = self.refresh_token(tokens.get("refresh"))
        self.assertNotEqual(tokens.get("access"), access_after)

    def test_if_api_return_status_code_200_on_list(self):
        tokens = self.get_tokens()
        access_token = tokens.get("access")
        response = self.client.get(
            self.get_url(),
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_if_api_list_users(self):
        users_list = self.create_many_users()
        access_token = self.get_tokens().get("access")
        response = self.client.get(
            self.get_url(),
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        i = 0
        for user in response.data:
            if i == 5:
                break
            user_test = users_list[i]
            self.assertEqual(user.get("username"),user_test.username)
            self.assertEqual(user.get("email"),user_test.email)
            i += 1

    def test_if_api_user_return_status_code_401_if_user_not_authenticated_on_list(self):
        response = self.client.get(reverse("api:api-user-list"))
        self.assertEqual(response.status_code, 401)

    def test_if_api_return_status_code_200_on_retrieve(self):
        access_token = self.get_tokens().get("access")
        response = self.client.get(
            self.get_url(action="detail",pk=1),
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 200)

    def test_if_api_retrieve_user(self):
        token = self.get_tokens().get("access")
        response = self.client.get(
            self.get_url(action="detail",pk=1),
            HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        self.assertEqual(response.data.get("username"), "jhondoe")
        self.assertEqual(response.data.get("email"), "jhondoe@email.com")


    def test_if_api_return_status_code_401_if_user_not_authenticated_on_retrieve(self):
        response = self.client.get(
            self.get_url(action="detail",pk=1)
        )
        self.assertEqual(response.status_code, 401)
    
    def test_if_api_return_status_code_201_on_create(self):
        response = self.client.post(
            self.get_url(),
            data={
                "username": "usertest",
                "email": "usertest@email.com",
                "birth_date": "1989-10-25",
                "password": "P@ssword123"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("username"), "usertest")
        self.assertEqual(response.data.get("email"), "usertest@email.com")
    
    def test_if_api_return_status_code_204_on_delete(self):
        tokens = self.get_tokens()
        access_token=tokens.get("access")
        user=tokens.get("user")
        response=self.client.delete(
            self.get_url("detail", pk=user.pk),
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 204)

    def test_if_user_cant_delete_other_user(self):
        user_other = self.create_user("crueger","freddy","freddy@email.com")
        tokens = self.get_tokens()
        user = tokens.get("user")
        access_token=tokens.get("access")
        response=self.client.delete(
            self.get_url("detail", pk=user_other.pk),
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )
        self.assertEqual(response.status_code, 403)


    