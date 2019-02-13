from .models import ProductType

def categories_processor(request):
    product_categories = ProductType.objects.raw(f"""
        SELECT * FROM website_producttype
    """)
    return{"product_categories": product_categories}