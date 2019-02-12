from website.models import RecommendedProduct

def recommendation_count(request):
    sql = f"""
            SELECT * FROM website_recommendedproduct
            WHERE recommended_to_id = {request.user.customer.id}
    """

    rec_products = RecommendedProduct.objects.raw(sql)
    count = 0
    if rec_products:
        for prod in rec_products:
            count += 1

    return {"rec_count": count}