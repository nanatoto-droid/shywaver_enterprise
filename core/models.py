from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

class BusinessCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Business Categories"
    
    def __str__(self):
        return self.name

class Business(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(BusinessCategory, on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    services = models.TextField(help_text="List your services, separated by commas")
    image = models.ImageField(upload_to='businesses/', blank=True, null=True)
    location = models.CharField(max_length=200, default="Campus Hub")
    email = models.EmailField()
    website = models.URLField(blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    review_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def get_services_list(self):
        return [s.strip() for s in self.services.split(',')]
    
    def get_absolute_url(self):
        return reverse('business_detail', kwargs={'slug': self.slug})
    
    def average_rating(self):
        if self.review_count > 0:
            return self.rating
        return 0

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('entrepreneurship', 'Entrepreneurship'),
        ('marketing', 'Marketing'),
        ('community', 'Community'),
        ('business', 'Business'),
    ]
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='entrepreneurship')
    read_time = models.IntegerField(help_text="Estimated read time in minutes")
    views = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('coffee', 'Coffee'),
        ('pastries', 'Pastries'),
        ('sandwiches', 'Sandwiches'),
        ('specialty', 'Specialty'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - ${self.price}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    pickup_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"

class FounderTableReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    business_name = models.CharField(max_length=200)
    purpose = models.TextField()
    attendees = models.IntegerField(default=2)
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['date', 'time']
    
    def __str__(self):
        return f"{self.business_name} - {self.date} at {self.time}"

class PitchWallPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pitch_posts')
    title = models.CharField(max_length=200)
    description = models.TextField()
    business_profile_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='pitches/', blank=True, null=True)  # Add image field
    category = models.CharField(max_length=50, choices=[
        ('looking_for_cofounder', 'Looking for Co-founder'),
        ('seeking_team', 'Seeking Team Members'),
        ('idea_validation', 'Idea Validation'),
        ('seeking_investor', 'Seeking Investor'),
        ('looking_for_mentor', 'Looking for Mentor'),
        ('collaboration', 'Collaboration Opportunity'),
        ('other', 'Other'),
    ], default='other')
    skills_needed = models.CharField(max_length=500, blank=True, help_text="Comma-separated skills needed")
    interest_count = models.IntegerField(default=0)  # Track how many people are interested
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('pitch_detail', kwargs={'pk': self.id})
    
    def get_skills_list(self):
        if self.skills_needed:
            return [s.strip() for s in self.skills_needed.split(',')]
        return []
    
class PitchInterest(models.Model):
    pitch = models.ForeignKey(PitchWallPost, on_delete=models.CASCADE, related_name='interests')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['pitch', 'user']
    
    def __str__(self):
        return f"{self.user.username} interested in {self.pitch.title}"

class PitchComment(models.Model):
    pitch = models.ForeignKey(PitchWallPost, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.pitch.title}"    

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email

class BusinessReview(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['business', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.business.name} - {self.rating} stars"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    business_name = models.CharField(max_length=200, blank=True)
    website = models.URLField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class WaverBusinessPass(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='waver_pass')
    is_active = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Waver Pass"
    
class Book(models.Model):
    CATEGORY_CHOICES = [
        ('entrepreneurship', 'Entrepreneurship'),
        ('leadership', 'Leadership'),
        ('innovation', 'Innovation'),
        ('personal_growth', 'Personal Growth'),
        ('marketing', 'Marketing'),
        ('finance', 'Finance'),
        ('technology', 'Technology'),
        ('startup', 'Startup'),
    ]
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    cover_image = models.ImageField(upload_to='books/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='entrepreneurship')
    is_featured = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    pages = models.IntegerField(default=0, help_text="Number of pages")
    published_year = models.IntegerField(default=2024)
    publisher = models.CharField(max_length=100, blank=True)
    isbn = models.CharField(max_length=20, blank=True, help_text="ISBN number")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            import re
            self.slug = re.sub(r'[^\w\s-]', '', self.title.lower())
            self.slug = re.sub(r'[-\s]+', '-', self.slug)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'slug': self.slug})

class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['book', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.rating} stars"
