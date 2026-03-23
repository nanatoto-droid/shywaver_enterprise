from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Business, BlogPost, MenuItem, FounderTableReservation, PitchWallPost, BusinessReview, UserProfile
from .models import (
    Business, BlogPost, MenuItem, FounderTableReservation, 
    PitchWallPost, BusinessReview, UserProfile, PitchInterest, PitchComment, Book, BookReview
)

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar', 'phone', 'business_name', 'website']

class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['name', 'category', 'description', 'services', 'image', 'location', 'email', 'website']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'services': forms.Textarea(attrs={'rows': 3, 'placeholder': 'e.g., Logo Design, Branding, Social Media Graphics'}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'excerpt', 'content', 'image', 'read_time']
        widgets = {
            'excerpt': forms.Textarea(attrs={'rows': 3}),
            'content': forms.Textarea(attrs={'rows': 10}),
        }

class FounderTableReservationForm(forms.ModelForm):
    class Meta:
        model = FounderTableReservation
        fields = ['date', 'time', 'business_name', 'purpose', 'attendees']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class PitchWallPostForm(forms.ModelForm):
    class Meta:
        model = PitchWallPost
        fields = ['title', 'category', 'description', 'skills_needed', 'business_profile_url', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 6, 'placeholder': 'Describe your idea, what you\'re looking for, and what you can offer...'}),
            'skills_needed': forms.Textarea(attrs={'rows': 2, 'placeholder': 'e.g., Python, React, Marketing, UI/UX Design'}),
            'business_profile_url': forms.URLInput(attrs={'placeholder': 'https://linkedin.com/in/yourprofile or https://yourportfolio.com'}),
        }

class PitchInterestForm(forms.ModelForm):
    class Meta:
        model = PitchInterest
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell them why you\'re interested and what you can bring to the table...'}),
        }

class PitchCommentForm(forms.ModelForm):
    class Meta:
        model = PitchComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Leave a comment or question...'}),
        }
class BusinessReviewForm(forms.ModelForm):
    class Meta:
        model = BusinessReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} stars") for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class NewsletterForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'placeholder': 'Enter your email',
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
    }))

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'cover_image', 'category', 
                  'is_featured', 'available', 'pages', 'published_year', 
                  'publisher', 'isbn']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write a detailed description of the book...'}),
            'title': forms.TextInput(attrs={'placeholder': 'Book title'}),
            'author': forms.TextInput(attrs={'placeholder': 'Author name'}),
            'publisher': forms.TextInput(attrs={'placeholder': 'Publisher name'}),
            'isbn': forms.TextInput(attrs={'placeholder': 'ISBN-13 or ISBN-10'}),
        }

class BookReviewForm(forms.ModelForm):
    class Meta:
        model = BookReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, f"{i} stars") for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your thoughts about this book...'}),
        }