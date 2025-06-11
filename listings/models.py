# 


from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import itertools
from django.contrib.auth.models import User

User = get_user_model()

PROPERTY_TYPE_CHOICES = [
    ('apartment', 'Apartment'),
    ('bedsitter', 'Bedsitter'),
    ('house', 'House'),
    ('single_room', 'Single Room'),
    ('studio', 'Studio'),
    ('other', 'Other'),
]

STATUS_CHOICES = [
    ('available', 'Available'),
    ('rented', 'Rented'),
    ('pending', 'Pending'),
]

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=150)
    description = models.TextField()
    location = models.CharField(max_length=255)
    rent = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField(default=1)
    bathrooms = models.PositiveIntegerField(default=1)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    image = models.ImageField(upload_to='listing_images/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=False, null=False)
    is_published = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            for i in itertools.count(1):
                if not Listing.objects.filter(slug=slug).exists():
                    break
                slug = f"{base_slug}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Inquiry(models.Model):
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey('Listing', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Inquiry for {self.listing.title} by {self.name}'
    

class Booking(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, default='Pending')  # e.g., Pending, Approved, Rejected

    def __str__(self):
         return f"Booking by {self.user} for {self.listing}"