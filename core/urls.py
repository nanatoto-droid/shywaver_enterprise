from django.urls import path
from . import views

urlpatterns = [
    # index
    path('', views.index, name='index'),
    
    # Cafe Menu
    path('cafe-menu/', views.cafe_menu, name='cafe_menu'),
    path('book-nook/', views.book_nook, name='book_nook'),
    
    # Blog URLs - specific before detail
    path('blog/add/', views.add_blog_post, name='add_blog_post'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/edit/', views.edit_blog_post, name='edit_blog_post'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Business URLs - specific before detail
    path('business/add/', views.add_business, name='add_business'),
    path('business-exchange/', views.business_exchange, name='business_exchange'),
    path('business/<slug:slug>/edit/', views.edit_business, name='edit_business'),
    path('business/<slug:slug>/', views.business_detail, name='business_detail'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard & User Management
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Reservations & Pitch
    path('reserve-table/', views.reserve_founders_table, name='reserve_table'),
    path('create-pitch/', views.create_pitch_post, name='create_pitch'),
    
    # Newsletter
    path('newsletter-subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Cart
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),

    # Pitch URLs
    path('pitch/<int:pk>/', views.pitch_detail, name='pitch_detail'),
    path('pitch/create/', views.create_pitch, name='create_pitch'),
    path('pitch/<int:pk>/edit/', views.edit_pitch, name='edit_pitch'),
    path('pitch/<int:pk>/delete/', views.delete_pitch, name='delete_pitch'),

    # Book Nook URLs
    path('book-nook/add/', views.add_book, name='add_book'),
    path('book-nook/', views.book_nook, name='book_nook'),
    path('book-nook/<slug:slug>/edit/', views.edit_book, name='edit_book'),
    path('book-nook/<slug:slug>/delete/', views.delete_book, name='delete_book'),
    path('book-nook/<slug:slug>/', views.book_detail, name='book_detail'),

]
