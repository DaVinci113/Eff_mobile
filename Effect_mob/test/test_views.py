from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from Effect_mob.ads.models import Ad


class BaseAdTestCase(TestCase):
    """Базовый класс для тестов объявлений"""

    def setUp(self):
        """Настройка базы данных"""
        self.user1 = User.objects.create_user(
                    username='user1',
                    email='user1@user1.com',
                    password='user1'
                )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@user2.com',
            password='user2'
        )
        self.client.login(username='user1', password='user1')

        # Создаем тестовые объявления
        self.ad1 = self.create_ad(
            user=self.user1,
            title='setup_title',
            description='setup_description',
            image_url='setup url',
            condition='setup condition'
        )

        self.ad2 = self.create_ad(
            user=self.user2,
            title='setup_title2',
            description='setup_description2',
            image_url='setup url2',
            condition='setup condition2'
        )

        def create_ad(self, user, title, description, image_url, condition):
            """Создает тестовое объявление"""
            return Ad.objects.create(
                user=user,
                title=title,
                description=description,
                image_url=image_url,
                condition=condition,
                created_at='2025-04-12 21:43:11.864522'
            )

        def get_ad_data(self, title='test_title', description='test_description'):
            """Возвращает тестовые данные для объявления"""
            return {
                'title': title,
                'description': description,
                'image_url': 'https://yandex.ru/images/search?source.jpg',
                'condition': 'NEW',
                'created_at': '2025-04-12 21:43:11.864522'
            }

class AdTestCase(BaseAdTestCase):
    """Тесты для объявлений"""

    def test_used_correct_template(self):
        """Тест корректности шаблона"""
        response = self.client.get(reverse('ads:ads-list'))
        self.assertTemplateUsed(response, 'ads/ads_list.html')

    def test_ad_create_view(self):
        """Тест создания объявления"""
        ad_id = self.ad1.id
        response = self.client.get(f'/ads/user_ads/update/{ad_id}/')
        self.assertEqual(response.status_code, 200)

        start_title = self.ad1.title
        data = self.get_ad_data(title='update setup title')
        response_after = self.client.post(f'/ads/user_ads/update/{ad_id}/', data=data)
        self.assertEqual(response_after.status_code, 302)
        self.assertNotEqual(start_title, Ad.objects.get(id=ad_id).title)

    def test_ad_delete_view(self):
        """Тест удаления объявления"""
        self.assertEqual(Ad.objects.count(), 2)
        response = self.client.post(f'/ads/user_ads/delete/{self.ad1.id}/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Ad.objects.count(), 1)

    def test_ad_search_view(self):
        """Тест поиска по чужим объявлениям"""
        self.create_ad(
            user=self.user2,
            title='setup_title3',
            description='setup_description3',
            image_url='setup url3',
            condition='setup condition3'
        )
        data = {'q': 'setup_title'}
        response = self.client.get(reverse('ads:ad-search'), data=data)
        self.assertEqual(
            response.text.count(self.user2.username),
            Ad.objects.filter(user=self.user2).count()
        )

    def test_user_ad_search_view(self):
        """Тест поиска по своим объявлениям"""
        data = {'q': 'setup_title'}
        response = self.client.get(reverse('ads:user-ad-search'), data=data)
        self.assertEqual(
            response.text.count(self.user1.username) - 1,
            Ad.objects.filter(user=self.user1).count()
        )
