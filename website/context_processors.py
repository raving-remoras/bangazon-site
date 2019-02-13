<<<<<<< HEAD
from website.models import RecommendedProduct

def recommendation_count(request):
    count = 0
    if request.user.is_authenticated:
        sql = f"""
                SELECT * FROM website_recommendedproduct
                WHERE recommended_to_id = {request.user.customer.id}
        """

        rec_products = RecommendedProduct.objects.raw(sql)
        if rec_products:
            for prod in rec_products:
                count += 1


    return {"rec_count": count}
=======
from .models import ProductType

def categories_processor(request):
    product_categories = ProductType.objects.raw(f"""
        SELECT * FROM website_producttype
    """)
    return{"product_categories": product_categories}
>>>>>>> master
