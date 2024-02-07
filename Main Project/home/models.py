from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.conf import settings


class CustomUser(AbstractUser):
    
    EMPLOYER = 'employer'
    AGENT = 'agent'
    POLICE = 'police'

    ADMIN = 'admin'
    
    USER_TYPE_CHOICES = [
        (EMPLOYER, 'Employer'),
        (AGENT, 'Agent'),
        (POLICE, 'Police'),
        (ADMIN, 'Admin'),
    ]

    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    adhar_number = models.CharField(max_length=12, null=True, blank=True)
    license_number = models.CharField(max_length=10, null=True, blank=True)
    police_id = models.CharField(max_length=6, null=True, blank=True)
    uploaded_file = models.FileField(upload_to='uploaded_files/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    def save(self, *args, **kwargs):
        if not self.pk:  
            if self.user_type == self.ADMIN:
                self.is_verified = True 
            else:
                self.is_verified = False 
        
        super().save(*args, **kwargs)
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default=EMPLOYER  # Set a default role if needed
    )

    is_employer = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_police = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_picture', blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    profile_created_at = models.DateTimeField(auto_now_add=True)
    profile_modified_at = models.DateTimeField(auto_now=True)
    add_pf = models.FileField(upload_to='add_pf/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}"

class WorkCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return self.name

class MigratoryWorker(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    
    first_name = models.CharField(max_length=255)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    nationality = models.CharField(max_length=255)
    address = models.TextField()
    contact_number = models.CharField(max_length=15)
    adhar_number = models.CharField(max_length=12, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/')
    document = models.FileField(upload_to='documents')
    is_verified = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    category = models.ForeignKey(WorkCategory, on_delete=models.CASCADE,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    work_permit_verified = models.BooleanField(default=False)
    police = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='police_workers', limit_choices_to={'is_police': True},blank=True, null=True)
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='agent_workers', limit_choices_to={'is_agent': True})
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='employer_workers', limit_choices_to={'is_employer': True},blank=True, null=True)

    def __str__(self):
        return self.first_name
    
class Police(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, blank=True, null=True)
    badge_number = models.CharField(max_length=20)
    department = models.CharField(max_length=100, blank=True, null=True)
    rank = models.CharField(max_length=50, blank=True, null=True)
    service_years = models.PositiveIntegerField(blank=True, null=True)
    station_name = models.CharField(max_length=100, blank=True, null=True)
    station_address = models.CharField(max_length=150, blank=True, null=True)
    station_contact = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return self.badge_number
    


from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

    
class BookingWorker(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]

    DURATION_CHOICES = [
        ('days', 'Days'),
        ('months', 'Months'),
    ]

    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings_as_employer')
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings_as_agent')
    worker = models.ForeignKey(MigratoryWorker, on_delete=models.CASCADE, related_name='bookings')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    duration = models.PositiveIntegerField(default=1)  # You can change the default value as needed
    duration_unit = models.CharField(max_length=10, choices=DURATION_CHOICES, default='days')
    is_work_completed = models.BooleanField(default=False)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_accepted = models.DateTimeField(null=True, blank=True)
    date_declined = models.DateTimeField(null=True, blank=True)
    is_accepted = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2,blank=True,null=True)


    def __str__(self):
        return f'{self.employer} requested {self.worker} (Status: {self.status})'
    

class Payment(models.Model):
    
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    worker = models.ForeignKey(MigratoryWorker, on_delete=models.CASCADE,blank=True,null=True)
    booking = models.ForeignKey(BookingWorker, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    payment_receipt = models.FileField(upload_to='payment_receipts/', null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=255, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=255, null=True, blank=True)
    is_paid=models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Payment for Booking {self.booking}'