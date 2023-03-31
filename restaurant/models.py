from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, first_name=None, last_name=None, password=None, **extra_fields):
        """
        Creates and saves a user with the given usernname, email, first_name,
        last_name and password
        """
        if not username:
            raise ValueError("Users must have a valid username")
        user = self.model(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email, first_name,
        last_name, email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True) 
        
        user = self.create_user(
            username,
            email,
            first_name,
            last_name,
            password=password,
            **extra_fields,
        )
           
        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, blank=False, unique=True)
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False, unique=True)
    password = models.CharField(max_length=255, blank=False)
    
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'password']
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'




class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    num_guests = models.SmallIntegerField()
    booking_date = models.DateField()
    booking_slot = models.SmallIntegerField()
    
    def __str__(self) -> str:
        return f'{self.user.username} {self.num_guests}guests'
    
    
class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, unique=True)
    slug = models.SlugField()
    
    def __str__(self) -> str:
        return self.title
    
    
class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    description = models.CharField(max_length=1000, default='no description', null=True)
    inventory = models.SmallIntegerField()
    featured = models.BooleanField(db_index=True, default=False)
    
    def __str__(self) -> str:
        return self.title
    
    def get_item(self):
        return f'{self.title}: {str(self.price)}'
    

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('menuitem', 'user')
        
    def __str__(self) -> str:
        return self.user.username + " - " + self.menuitem.title + " " + str(self.quantity)

        
class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='delivery_crew', null=True)
    status = models.BooleanField(db_index=True, default=0)
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(db_index=True)

    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together = ('order', 'menuitem')