from tkinter import CASCADE
from django.db import models

from django.core.exceptions import ValidationError
import re

class Contact(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        ordering = ['-created_at']

class Deal(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('won', 'Won'),
        ('lost', 'Lost'),
    ]    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name= 'deals')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

    class Customer(models.Model):
        name = models.CharField(max_length=100)
        email= models.EmailField(unique=True)
        phone = models.CharField(max_length=20, blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f"{self.name}"
        
        class Meta:
            ordering = ['-created_at']

        def clean(self):
            #validate email uniqueness
            if Customer.objects.filter(email=self.email).exclude(pk=self.pk).exists():
                raise ValidationError("Email must be unique.")
            
            #validate Phone number format if  provided
            if self.phone:
                phone_pattern = r'^\+?1?\d{9,15}$|^\d{3}-\d{3}-\d{4}$'
                if not re.match(phone_pattern, self.phone):
                    raise ValidationError({"phone":"Invalid phone number format. Use +999999999 or 123-456-7890 format.  "})

class Product(models.Model):
    name= models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering =['-created_at']

    def clean(self):
        #Validate price is positive 
        if self.price <=0:
            raise ValidationError({"price":"Price must be greater than zero."})    
        #Validate stock is non-negative
        if self.stock <0:
            raise ValidationError({"stock": "Stock cannot be negative."})
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=CASCADE, related_name='orders')
    products = models.ManyToManyField(Product, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} -{self.customer.name}"
    
    class Meta:
        ordering =['-created_at']

    def calculate_total(self):
        """calculate total amount from all products"""
        total = sum(product.price for product in self.products.all())
        self.total_amount = total
        return total
