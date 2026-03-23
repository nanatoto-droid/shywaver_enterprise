from .models import MenuItem, BusinessCategory

def site_context(request):
    return {
        'menu_categories': MenuItem.CATEGORY_CHOICES if hasattr(MenuItem, 'CATEGORY_CHOICES') else [],
        'business_categories': BusinessCategory.objects.all() if hasattr(BusinessCategory, 'objects') else [],
    }