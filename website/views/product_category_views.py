from website.models import Product, ProductType
from django.shortcuts import render

def product_categories(request):
    """Returns all product categories and their associated products when a user selects the product categories view

    Author: Kelly Morin
    Returns:
        render - product_category.html template
    """
    if not request.user.is_authenticated:
        product_by_category = Product.objects.raw(f"""
            SELECT * FROM website_product
            JOIN website_producttype ON website_producttype.id = website_product.product_type_id
            WHERE website_product.delete_date IS null
            ORDER BY website_product.product_type_id
        """)
    else:
        user_id = request.user.customer.id
        product_by_category = Product.objects.raw(f"""
            SELECT * FROM website_product
            JOIN website_producttype ON website_producttype.id = website_product.product_type_id
            WHERE website_product.delete_date IS null AND website_product.seller_id IS NOT {user_id}
            ORDER BY website_product.product_type_id
        """)

    product_per_category = dict()

    for product in product_by_category:
        if product.get_available_count != 0:
            try:
                product_per_category[product.name].append(product)
            except KeyError:
                product_per_category[product.name] = list()
                product_per_category[product.name].append(product)

    context = {"product_per_category": product_per_category}

    return render(request, 'product_category.html', context)

def product_by_category(request, category_id):
    if not request.user.is_authenticated:
        product_category_name = ProductType.objects.raw(f"""
            SELECT * FROM website_producttype
            WHERE website_producttype.id IS {category_id}
        """)[0]

        product_by_category = Product.objects.raw(f"""
            SELECT * FROM website_product
            JOIN website_producttype ON website_producttype.id = website_product.product_type_id
            WHERE website_product.delete_date IS null AND website_product.product_type_id = {category_id}
            ORDER BY website_product.product_type_id
        """)

    else:
        product_category_name = ProductType.objects.raw(f"""
            SELECT * FROM website_producttype
            WHERE website_producttype.id IS {category_id}
        """)[0]
        user_id = request.user.customer.id
        product_by_category = Product.objects.raw(f"""
            SELECT * FROM website_product
            JOIN website_producttype ON website_producttype.id = website_product.product_type_id
            WHERE website_product.delete_date IS null AND website_product.seller_id IS NOT {user_id} AND website_product.product_type_id = {category_id}
            ORDER BY website_product.product_type_id
        """)
    context = {"products": product_by_category, "product_category": product_category_name}
    return render(request, 'product_by_category.html', context)