from email.policy import default
from django.db import models
import uuid
from django.contrib.auth.models import User
from  django.conf import settings
from userProfile.models import Customer
from decimal import Decimal  # Import Decimal
from django.utils.text import slugify


# Create your models here.

        
class Category(models.Model):
    title = models.CharField(max_length=200)
    category_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    slug = models.SlugField(default= None)
    featured_product = models.OneToOneField('Product', on_delete=models.CASCADE, blank=True, null=True, related_name='featured_product')
    icon = models.CharField(max_length=100, default=None, blank = True, null=True)

    class Meta:
        verbose_name = ("Categories")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.title
    
class Review(models.Model):
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name = "reviews")
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(default="description")
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = ("Reviews")
        verbose_name_plural = ("Reviews")
    
    def __str__(self):
        return self.description
    

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    discount = models.BooleanField(default=False)
    image = models.ImageField(upload_to = 'img',  blank = True, null=True, default='')
    old_price = models.FloatField(default=100.00,help_text="this is the price if no discount, if is discount it become an old price")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    slug = models.SlugField(default=None)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    inventory = models.IntegerField(default=5)
    top_deal=models.BooleanField(default=False)
    flash_sales = models.BooleanField(default=False)
    discountValue = models.DecimalField(max_digits=5, decimal_places=2, default=0.00 , help_text="put discount value")
    

    # @property
    # def price(self):
    #     old_price_decimal = Decimal(str(self.old_price))  # Convert old_price to Decimal for accurate calculations
    #     print(f"Discount: {self.discount}, Discount Value: {self.discountValue}")  # Debugging info
        
    #     if self.discount and self.discountValue > 0:
    #         discount_amount = (self.discountValue / Decimal('100')) * old_price_decimal
    #         new_price = old_price_decimal - discount_amount
    #         print(f"Old Price: {old_price_decimal}, Discount Applied: {discount_amount}, New Price: {new_price}")
    #     else:
    #         new_price = old_price_decimal
    #         print(f"No discount applied. Price: {new_price}")
    #     return new_price

    
    @property
    def img(self):
        if self.image == "":
            self.image = ""
        
        return self.image
    
    class Meta:
        verbose_name = ("Products")
        verbose_name_plural = ("Products")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name = "images")
    image = models.ImageField(upload_to="img", default="", null=True, blank=True)

    class Meta:
        verbose_name = ("Product images")
        verbose_name_plural = ("Product Images")

    def __str__(self):
        return str(self.product)

class Cart(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null = True, blank=True)
    cart_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    session_id = models.CharField(max_length=100)
    

    @property
    def num_of_items(self):
        cartitems = self.cartitems_set.all()
        qtysum = sum([ qty.quantity for qty in cartitems])
        return qtysum
    
    @property
    def cart_total(self):
        cartitems = self.cartitems_set.all()
        qtysum = sum([ qty.subTotal for qty in cartitems])
        return qtysum
    
    class Meta:
        verbose_name = ("Cart")
        verbose_name_plural = ("Cart")

    def __str__(self):
        return str(self.cart_id)

class Cartitems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='cartitems')
    quantity = models.PositiveSmallIntegerField(default=0)
    
    
    @property
    def subTotal(self):
        total = self.quantity * self.product.price
        
        return total
    
    class Meta:
        verbose_name = ("Cart Items")
        verbose_name_plural = ("Cart Items")
        constraints = [
            models.CheckConstraint(check=models.Q(quantity__gt=0), name='quantity_positive')
        ]
    
    def __str__(self):
        return str(self.cart) # TODO
    
class Order(models.Model):
    
    
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    pending_status = models.CharField(
        max_length=50, choices=PAYMENT_STATUS_CHOICES, default='PAYMENT_STATUS_PENDING')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    
    def __str__(self):
        return self.pending_status
    
    @property 
    def total_price(self):
        items = self.items.all()
        total = sum([item.quantity * item.product.old_price for item in items])
        return total



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name = "items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    

    def __str__(self):
        return self.product.name
    
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , null=True)
    name = models.CharField(max_length=30)
    bio = models.TextField()
    picture = models.ImageField(upload_to = 'img', blank=True, null=True)
    
    def __str__(self):
        return str(self.user)

class SavedItem(models.Model):
    owner = models.ForeignKey(Customer, on_delete=models.CASCADE, null = True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    added = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = ("Saved Items")
        verbose_name_plural = ("Saved Items")
    
    def __str__(self):
        return str(self.id)