from django.test import TestCase
from django_orm_sugar import exec_sql_template
from app.models import UserProfile


# Create your tests here.
class TestTemplateLoading(TestCase):
    def setUp(self):
        names = ['Bob', 'Alice', 'Third Party']
        for n in names:
            UserProfile.objects.create(name=n)

    def test_queryset(self):
        results = exec_sql_template(UserProfile, 'select_user_profile.sql', {'search_term': 'Bob'})
        self.assertEqual(results[0].name, 'Bob')