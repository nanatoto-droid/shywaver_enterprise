from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import *

class Command(BaseCommand):
    help = 'Adds sample data to the database'

    def handle(self, *args, **kwargs):
        # Create sample business categories
        categories = [
            {'name': 'Graphic Design', 'slug': 'graphic-design'},
            {'name': 'Photography', 'slug': 'photography'},
            {'name': 'Web Development', 'slug': 'web-development'},
            {'name': 'Social Media Marketing', 'slug': 'social-media-marketing'},
            {'name': 'Handmade Products', 'slug': 'handmade-products'},
            {'name': 'Tutoring', 'slug': 'tutoring'},
            {'name': 'Fitness & Wellness', 'slug': 'fitness-wellness'},
            {'name': 'Fashion & Vintage', 'slug': 'fashion-vintage'},
        ]
        
        for cat in categories:
            obj, created = BusinessCategory.objects.get_or_create(name=cat['name'], defaults={'slug': cat['slug']})
            if created:
                self.stdout.write(f'Created category: {cat["name"]}')
        
        # Create sample menu items
        menu_items = [
            {'name': 'Espresso', 'category': 'coffee', 'description': 'Rich and bold single or double shot', 'price': 3.50, 'featured': True},
            {'name': 'Cappuccino', 'category': 'coffee', 'description': 'Smooth espresso with steamed milk and foam', 'price': 4.50, 'featured': True},
            {'name': 'Latte', 'category': 'coffee', 'description': 'Creamy espresso with steamed milk', 'price': 4.75, 'featured': True},
            {'name': 'Iced Americano', 'category': 'coffee', 'description': 'Refreshing cold espresso with water and ice', 'price': 4.00},
            {'name': 'Croissant', 'category': 'pastries', 'description': 'Buttery, flaky French pastry', 'price': 3.75, 'featured': True},
            {'name': 'Blueberry Muffin', 'category': 'pastries', 'description': 'Fresh blueberry muffin baked daily', 'price': 4.00},
            {'name': 'Chocolate Croissant', 'category': 'pastries', 'description': 'Crispy croissant with dark chocolate filling', 'price': 4.25},
            {'name': 'Turkey Sandwich', 'category': 'sandwiches', 'description': 'Fresh turkey, lettuce, tomato on whole wheat', 'price': 8.50},
            {'name': 'Veggie Wrap', 'category': 'sandwiches', 'description': 'Hummus, cucumber, bell peppers, spinach', 'price': 7.75},
            {'name': 'Caprese Panini', 'category': 'sandwiches', 'description': 'Fresh mozzarella, tomato, basil, balsamic', 'price': 9.00},
            {'name': 'Matcha Latte', 'category': 'specialty', 'description': 'Creamy green tea with steamed milk', 'price': 5.50},
            {'name': 'Açai Bowl', 'category': 'specialty', 'description': 'Açai berry base with granola, fruit, and honey', 'price': 9.50},
        ]
        
        for item in menu_items:
            obj, created = MenuItem.objects.get_or_create(name=item['name'], defaults=item)
            if created:
                self.stdout.write(f'Created menu item: {item["name"]}')
        
        # Create sample blog posts
        blog_posts = [
            {
                'title': '5 Tips for Student Entrepreneurs Starting Their First Business',
                'slug': '5-tips-student-entrepreneurs',
                'excerpt': 'Learn essential strategies to launch your business while balancing your academic responsibilities',
                'content': 'Starting a business while in school can be challenging but rewarding. Here are 5 essential tips:\n\n1. Start Small: Begin with a minimum viable product to test your idea.\n2. Time Management: Create a schedule that balances academics and business.\n3. Build a Support Network: Connect with other student entrepreneurs.\n4. Listen to Customers: Gather feedback and iterate quickly.\n5. Be Ready to Pivot: Adapt your business model based on what you learn.',
                'category': 'entrepreneurship',
                'read_time': 5,
                'is_published': True,
            },
            {
                'title': 'How to Build Your Personal Brand as a Student Creator',
                'slug': 'build-personal-brand-student-creator',
                'excerpt': 'Discover the secrets to building a strong personal brand that attracts customers and opportunities',
                'content': 'Building a personal brand is essential for student creators. Here is your guide:\n\nDefine Your Niche: Find what makes you unique.\nBe Consistent: Use the same visual identity across platforms.\nShare Your Journey: Document your progress and challenges.\nEngage with Your Audience: Respond to comments and messages.\nCollaborate with Others: Partner with fellow creators to expand your reach.',
                'category': 'marketing',
                'read_time': 7,
                'is_published': True,
            },
            {
                'title': 'The ShyWaver Hub: A Game Changer for Campus Entrepreneurs',
                'slug': 'shywaver-hub-game-changer',
                'excerpt': 'Explore how the ShyWaver Hub is transforming student entrepreneurship on campus',
                'content': 'The ShyWaver Hub provides a unique space for student entrepreneurs to connect, collaborate, and grow. With the Book Café for networking, the Boutique for retail exposure, and digital tools for finding collaborators, we are building a thriving entrepreneurial ecosystem.',
                'category': 'community',
                'read_time': 6,
                'is_published': True,
            },
        ]
        
        # Get or create a demo user
        demo_user, created = User.objects.get_or_create(
            username='demo_user',
            defaults={'email': 'demo@shywaver.com', 'is_active': True}
        )
        if created:
            demo_user.set_password('demo12345')
            demo_user.save()
            self.stdout.write('Created demo user: demo_user/demo12345')
            # Create profile for demo user
            UserProfile.objects.get_or_create(user=demo_user)
        
        # Create blog posts with demo user
        for post_data in blog_posts:
            obj, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults={
                    **post_data,
                    'author': demo_user,
                }
            )
            if created:
                self.stdout.write(f'Created blog post: {post_data["title"]}')
        
        # Create sample business
        businesses = [
            {
                'name': 'Luna Design Studio',
                'slug': 'luna-design-studio',
                'description': 'Custom logo design, branding packages, and social media graphics for student businesses',
                'services': 'Logo Design, Branding, Social Media Graphics, Print Design',
                'location': 'Campus Hub',
                'email': 'luna@lunadesign.com',
                'website': 'https://lunadesign.com',
                'rating': 4.9,
                'review_count': 24,
                'is_active': True,
            },
            {
                'name': 'Pixel Perfect Photography',
                'slug': 'pixel-perfect-photography',
                'description': 'Professional photography services for events, products, and portraits at affordable student rates',
                'services': 'Event Photography, Product Photography, Portraits, Editing',
                'location': 'Campus Hub',
                'email': 'pixel@perfectphoto.com',
                'rating': 4.8,
                'review_count': 18,
                'is_active': True,
            },
            {
                'name': 'Code Wizards',
                'slug': 'code-wizards',
                'description': 'Website design and development for student entrepreneurs and small businesses',
                'services': 'Web Design, E-commerce, App Development, SEO',
                'location': 'Campus Hub',
                'email': 'code@wizards.com',
                'rating': 4.7,
                'review_count': 15,
                'is_active': True,
            },
        ]
        
        graphic_design_cat = BusinessCategory.objects.get(slug='graphic-design')
        photography_cat = BusinessCategory.objects.get(slug='photography')
        web_dev_cat = BusinessCategory.objects.get(slug='web-development')
        
        business_categories = [graphic_design_cat, photography_cat, web_dev_cat]
        
        for i, business_data in enumerate(businesses):
            obj, created = Business.objects.get_or_create(
                slug=business_data['slug'],
                defaults={
                    **business_data,
                    'owner': demo_user,
                    'category': business_categories[i],
                }
            )
            if created:
                self.stdout.write(f'Created business: {business_data["name"]}')
        
        self.stdout.write(self.style.SUCCESS('Sample data added successfully!'))