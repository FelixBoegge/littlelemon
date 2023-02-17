from django.test import TestCase
from restaurant.models import Menu


class MenuTest(TestCase):
    def test_get_item(self):
        item = Menu.objects.create(title='Pizza', price=12.50, inventory=15)
        itemstr = item.get_item()
        
        self.assertEqual(itemstr, "Pizza: 12.5")