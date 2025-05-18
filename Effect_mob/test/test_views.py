from django.contrib.auth.models import User
from django.db.models import Q
from django.test import TestCase
from django.urls import reverse
from ads.models import Ad


class AdTestCase(TestCase):

    def setUp(self):
        """Настройка базы данных"""

        set_up_user = User.objects.create_user(username='user1', email='user1@user1.com', password='user1')
        set_up_user2 = User.objects.create_user(username='user2', email='user2@user2.com', password='user2')
        self.client.login(username='user1', password='user1')
        Ad.objects.create(
            user=set_up_user,
            title='setup_title',
            description='setup_description',
            image_url = 'setup url',
            condition='setup condition',
            created_at='2025-04-12 21:43:11.864522',
        )
        Ad.objects.create(
            user=set_up_user2,
            title='setup_title2',
            description='setup_description2',
            image_url='setup url2',
            condition='setup condition2',
            created_at='2025-04-12 21:43:11.864522',
        )

    #
    def test_used_correct_template(self):
        """Тест корректности шаблона"""

        response = self.client.get(reverse('ads:ads-list'))
        self.assertTemplateUsed(response, 'ads/ads_list.html')

    def test_ad_create_view(self):
        """Тест создания объявления"""

        self.assertEqual(Ad.objects.count(), 2)
        data = {
            'title': 'title112233',
            'description': 'description1',
            'image_url': 'https://yandex.ru/images/search?source.jpg',
            'condition': 'NEW',
            'created_at': '2025-04-12 21:43:11.864522'
        }
        response = self.client.post(reverse('ads:ad-create'), data=data)
        print(response.text)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ad.objects.filter(title='title112233'))
        self.assertEqual(Ad.objects.count(), 3)

    def test_ad_update_view(self):
        """Тест обновления данных объявления"""

        ad_id = 1
        response = self.client.get(f'/ads/user_ads/update/{ad_id}/')
        self.assertEqual(response.status_code, 200)
        ad = Ad.objects.get(id=ad_id)
        start_title = ad.title
        data = {
            'title': 'update setup title',
            'description': 'description1',
            'image_url': 'https://yandex.ru/images/search?source.jpg',
            'condition': 'NEW',
            'created_at': '2025-04-12 21:43:11.864522'
        }
        response_after = self.client.post('/ads/user_ads/update/1/', data=data)
        self.assertEqual(response_after.status_code, 302)
        self.assertNotEqual(start_title, Ad.objects.get(id=ad_id).title)

    def test_ad_delete_view(self):
        """Тест удаления объявления"""

        self.assertEqual(Ad.objects.count(), 2)
        ad_pk = 1
        response = self.client.post(f'/ads/user_ads/delete/{ad_pk}/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 1)

    def test_ad_search_view(self):
        """Тест поиска по чужим объявлениям"""

        user = User.objects.filter(~Q(id=1))[0]
        Ad.objects.create(
            user=User.objects.get(username=user),
            title='setup_title3',
            description='setup_description3',
            image_url='setup url3',
            condition='setup condition3',
            created_at='2025-04-12 21:43:11.864522',
        )
        data = {
            'q': 'setup_title'
        }
        response = self.client.get(reverse('ads:ad-search'), data=data)
        self.assertEqual(response.text.count(user.username), Ad.objects.filter(user=user).count())

    def test_user_ad_search_view(self):
        """Тест поиска по своим объявлениям"""

        user = User.objects.get(id=1)

        data = {
            'q': 'setup_title'
        }
        response = self.client.get(reverse('ads:user-ad-search'), data=data)
        self.assertEqual(response.text.count(user.username)-1, Ad.objects.filter(user=user).count())