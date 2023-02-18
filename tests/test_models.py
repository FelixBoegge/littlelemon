from django.test import TestCase
from restaurant.models import MenuItem


class MenuTest(TestCase):
    def test_get_item(self):
        item = MenuItem.objects.create(title='Pizza', price=12.50, inventory=15)
        itemstr = item.get_item()
        
        self.assertEqual(itemstr, "Pizza: 12.5")