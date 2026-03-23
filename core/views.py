from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Avg
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import PitchWallPostForm, PitchInterestForm, PitchCommentForm

def home(request):
    featured_menu = MenuItem.objects.filter(featured=True, is_available=True)[:6]
    recent_blogs = BlogPost.objects.filter(is_published=True).order_by('-created_at')[:3]
    top_businesses = Business.objects.filter(is_active=True).order_by('-rating')[:6]
    pitch_posts = PitchWallPost.objects.filter(is_active=True).order_by('-created_at')[:6]
    
    context = {
        'featured_menu': featured_menu,
        'recent_blogs': recent_blogs,
        'top_businesses': top_businesses,
        'pitch_posts': pitch_posts,
    }
    return render(request, 'home.html', context)

def cafe_menu(request):
    menu_items = MenuItem.objects.filter(is_available=True)
    categories = MenuItem.CATEGORY_CHOICES
    
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    if search_query:
        menu_items = menu_items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if category_filter:
        menu_items = menu_items.filter(category=category_filter)
    
    context = {
        'menu_items': menu_items,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
    }
    return render(request, 'cafe_menu.html', context)

def blog(request):
    posts = BlogPost.objects.filter(is_published=True).order_by('-created_at')
    
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    if category_filter:
        posts = posts.filter(category=category_filter)
    
    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'search_query': search_query,
        'selected_category': category_filter,
    }
    return render(request, 'blog.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, is_published=True)
    post.views += 1
    post.save()
    
    related_posts = BlogPost.objects.filter(
        category=post.category, is_published=True
    ).exclude(id=post.id)[:3]
    
    context = {
        'post': post,
        'related_posts': related_posts,
    }
    return render(request, 'blog_detail.html', context)

def business_exchange(request):
    businesses = Business.objects.filter(is_active=True)
    categories = BusinessCategory.objects.all()
    
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    if search_query:
        businesses = businesses.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(services__icontains=search_query)
        )
    
    if category_filter:
        businesses = businesses.filter(category__slug=category_filter)
    
    paginator = Paginator(businesses, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'businesses': page_obj,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
    }
    return render(request, 'business_exchange.html', context)

def business_detail(request, slug):
    business = get_object_or_404(Business, slug=slug, is_active=True)
    reviews = business.reviews.all().order_by('-created_at')
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = BusinessReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.business = business
            review.user = request.user
            review.save()
            
            avg_rating = business.reviews.aggregate(Avg('rating'))['rating__avg']
            business.rating = avg_rating
            business.review_count = business.reviews.count()
            business.save()
            
            messages.success(request, 'Review submitted successfully!')
            return redirect('business_detail', slug=business.slug)
    else:
        form = BusinessReviewForm()
    
    context = {
        'business': business,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'business_detail.html', context)

@login_required
def dashboard(request):
    user_businesses = request.user.businesses.all()
    user_blog_posts = request.user.blog_posts.all()
    user_orders = request.user.orders.all().order_by('-created_at')[:10]
    user_reservations = FounderTableReservation.objects.filter(user=request.user).order_by('-date')
    user_pitch_posts = PitchWallPost.objects.filter(user=request.user)
    
    has_waver_pass = hasattr(request.user, 'waver_pass') and request.user.waver_pass.is_active
    
    context = {
        'businesses': user_businesses,
        'blog_posts': user_blog_posts,
        'orders': user_orders,
        'reservations': user_reservations,
        'pitch_posts': user_pitch_posts,
        'has_waver_pass': has_waver_pass,
    }
    return render(request, 'dashboard.html', context)

@login_required
def add_business(request):
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            # Generate slug from name
            import re
            business.slug = re.sub(r'[^\w\s-]', '', business.name.lower())
            business.slug = re.sub(r'[-\s]+', '-', business.slug)
            # Check for uniqueness
            original_slug = business.slug
            counter = 1
            while Business.objects.filter(slug=business.slug).exists():
                business.slug = f"{original_slug}-{counter}"
                counter += 1
            business.save()
            messages.success(request, 'Business listed successfully!')
            return redirect('business_detail', slug=business.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BusinessForm()
    
    return render(request, 'add_business.html', {'form': form})

@login_required
def edit_business(request, slug):
    business = get_object_or_404(Business, slug=slug, owner=request.user)
    
    if request.method == 'POST':
        form = BusinessForm(request.POST, request.FILES, instance=business)
        if form.is_valid():
            form.save()
            messages.success(request, 'Business updated successfully!')
            return redirect('business_detail', slug=business.slug)
    else:
        form = BusinessForm(instance=business)
    
    return render(request, 'edit_business.html', {'form': form, 'business': business})

@login_required
def add_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Generate slug from title
            import re
            post.slug = re.sub(r'[^\w\s-]', '', post.title.lower())
            post.slug = re.sub(r'[-\s]+', '-', post.slug)
            # Check for uniqueness
            original_slug = post.slug
            counter = 1
            while BlogPost.objects.filter(slug=post.slug).exists():
                post.slug = f"{original_slug}-{counter}"
                counter += 1
            post.save()
            messages.success(request, 'Blog post published successfully!')
            return redirect('blog_detail', slug=post.slug)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = BlogPostForm()
    
    return render(request, 'add_blog_post.html', {'form': form})

@login_required
def edit_blog_post(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, author=request.user)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('blog_detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'edit_blog_post.html', {'form': form, 'post': post})

@login_required
def reserve_founders_table(request):
    if request.method == 'POST':
        form = FounderTableReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()
            messages.success(request, 'Table reserved successfully! Please wait for confirmation.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = FounderTableReservationForm()
    
    return render(request, 'reserve_table.html', {'form': form})

@login_required
def create_pitch_post(request):
    if request.method == 'POST':
        form = PitchWallPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            messages.success(request, 'Pitch posted successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PitchWallPostForm()
    
    return render(request, 'create_pitch.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to ShyWaver Enterprises!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def profile(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'profile.html', {'form': form})

def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, 'Successfully subscribed to newsletter!')
            else:
                messages.info(request, 'You are already subscribed to our newsletter.')
        else:
            messages.error(request, 'Invalid email address.')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def add_to_cart(request):
    if request.method == 'POST' and request.user.is_authenticated:
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))
        
        menu_item = get_object_or_404(MenuItem, id=item_id)
        
        order, created = Order.objects.get_or_create(
            user=request.user,
            status='pending',
            defaults={'total': 0}
        )
        
        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            menu_item=menu_item,
            defaults={'quantity': quantity, 'price': menu_item.price}
        )
        
        if not created:
            order_item.quantity += quantity
            order_item.save()
        
        order.total = sum(item.price * item.quantity for item in order.items.all())
        order.save()
        
        return JsonResponse({'success': True, 'total': str(order.total)})
    
    return JsonResponse({'success': False, 'message': 'Please login to add items to cart'}, status=400)
    from django.contrib.auth.decorators import login_required
    from django.db.models import Count
    from .forms import PitchWallPostForm, PitchInterestForm, PitchCommentForm

def pitch_detail(request, pk):
    pitch = get_object_or_404(PitchWallPost, pk=pk, is_active=True)
    interests = pitch.interests.all().order_by('-created_at')
    comments = pitch.comments.all().order_by('-created_at')
    
    # Check if current user has already expressed interest
    user_interest = None
    if request.user.is_authenticated:
        user_interest = PitchInterest.objects.filter(pitch=pitch, user=request.user).first()
    
    # Handle interest form
    interest_form = PitchInterestForm()
    comment_form = PitchCommentForm()
    
    if request.method == 'POST':
        if 'interest_submit' in request.POST and request.user.is_authenticated:
            interest_form = PitchInterestForm(request.POST)
            if interest_form.is_valid():
                interest = interest_form.save(commit=False)
                interest.pitch = pitch
                interest.user = request.user
                interest.save()
                # Increment interest count
                pitch.interest_count += 1
                pitch.save()
                messages.success(request, 'Your interest has been recorded! The pitch creator will be notified.')
                return redirect('pitch_detail', pk=pitch.pk)
        
        elif 'comment_submit' in request.POST and request.user.is_authenticated:
            comment_form = PitchCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.pitch = pitch
                comment.user = request.user
                comment.save()
                messages.success(request, 'Comment posted successfully!')
                return redirect('pitch_detail', pk=pitch.pk)
    
    context = {
        'pitch': pitch,
        'interests': interests,
        'comments': comments,
        'interest_form': interest_form,
        'comment_form': comment_form,
        'user_interest': user_interest,
        'interest_count': pitch.interest_count,
    }
    return render(request, 'pitch_detail.html', context)

@login_required
def create_pitch(request):
    if request.method == 'POST':
        form = PitchWallPostForm(request.POST, request.FILES)
        if form.is_valid():
            pitch = form.save(commit=False)
            pitch.user = request.user
            pitch.save()
            messages.success(request, 'Your pitch has been posted successfully!')
            return redirect('pitch_detail', pk=pitch.pk)
    else:
        form = PitchWallPostForm()
    
    return render(request, 'create_pitch.html', {'form': form})

@login_required
def edit_pitch(request, pk):
    pitch = get_object_or_404(PitchWallPost, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = PitchWallPostForm(request.POST, request.FILES, instance=pitch)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your pitch has been updated!')
            return redirect('pitch_detail', pk=pitch.pk)
    else:
        form = PitchWallPostForm(instance=pitch)
    
    return render(request, 'edit_pitch.html', {'form': form, 'pitch': pitch})

@login_required
def delete_pitch(request, pk):
    pitch = get_object_or_404(PitchWallPost, pk=pk, user=request.user)
    
    if request.method == 'POST':
        pitch.delete()
        messages.success(request, 'Your pitch has been deleted.')
        return redirect('home')
    
    return render(request, 'delete_pitch.html', {'pitch': pitch})

def book_nook(request):
    books = Book.objects.filter(available=True).order_by('-is_featured', '-created_at')
    featured_books = books.filter(is_featured=True)[:6]
    categories = Book.CATEGORY_CHOICES
    
    # Search and filter
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if category_filter:
        books = books.filter(category=category_filter)
    
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'books': page_obj,
        'featured_books': featured_books,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_filter,
    }
    return render(request, 'book_nook.html', context)

def book_detail(request, slug):
    book = get_object_or_404(Book, slug=slug, available=True)
    reviews = book.reviews.all().order_by('-created_at')
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = BookReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('book_detail', slug=book.slug)
    else:
        form = BookReviewForm()
    
    context = {
        'book': book,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'book_detail.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('book_detail', slug=book.slug)
    else:
        form = BookForm()
    
    return render(request, 'add_book.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_book(request, slug):
    book = get_object_or_404(Book, slug=slug)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f'Book "{book.title}" updated successfully!')
            return redirect('book_detail', slug=book.slug)
    else:
        form = BookForm(instance=book)
    
    return render(request, 'edit_book.html', {'form': form, 'book': book})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_book(request, slug):
    book = get_object_or_404(Book, slug=slug)
    
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Book deleted successfully!')
        return redirect('book_nook')
    
    return render(request, 'delete_book.html', {'book': book})