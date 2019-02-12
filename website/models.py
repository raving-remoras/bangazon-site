from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    """Defines a model for a customer, including userId, address, and phone number

        Author: Brendan McCray
        Returns: __str__ userId, street_address, and phone_number

    """

    user = models.OneToOneField(User, on_delete=models.PROTECT)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    phone_number = models.IntegerField()
    delete_date = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"User: {self.user} Address:{self.street_address} Phone: {self.phone_number}"


class ProductType(models.Model):
    """ Defines a product type.

        Author: Sebastian Civarolo

    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    """Defines a Product

        Author: God
    """
    @property
    def get_purchased_count(self):
        """This method gets all completed orders for a specific product and calculates the number purchased

        Author: Kelly Morin, retooled by Rachel Daniel

        Returns:
            purchased_count
        """
        purchased_qty = OrderProduct.objects.raw(f"""
            SELECT * FROM website_orderproduct
            LEFT JOIN website_order ON website_order.id = website_orderproduct.order_id
            WHERE website_order.payment_type_id IS NOT null
            AND website_orderproduct.product_id = {self.id}
        """)

        purchased_count = 0
        for item in purchased_qty:
            if item.product_id == self.id:
                purchased_count += 1

        return purchased_count

    @property
    def get_available_count(self):
        """This method gets count of remaining product items based on total for sale and total purchased

        Author: Rachel Daniel

        Returns:
            available_count
        """
        purchased_count = self.get_purchased_count
        quantity = self.quantity
        available_count = quantity - purchased_count

        return available_count

    @property
    def get_cart_count(self):
        """This method gets all incomplete orders for a specific product and calculates the number currently in the carts of all users

        Author: Kelly Morin; retooled by Rachel Daniel

        Returns:
            cart_count
        """

        cart_qty = OrderProduct.objects.raw(f"""
            SELECT * FROM website_orderproduct
            LEFT JOIN website_order ON website_order.id = website_orderproduct.order_id
            WHERE website_order.payment_type_id IS null
            AND website_orderproduct.product_id = {self.id}
        """)

        cart_count = 0
        for item in cart_qty:
            if item.product_id == self.id:
                cart_count +=1

        return cart_count

    seller = models.ForeignKey(Customer, on_delete=models.PROTECT)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.PositiveIntegerField()
    quantity = models.IntegerField()
    delete_date = models.DateTimeField(default=None, null=True, blank=True)
    local_delivery = models.BooleanField(default=False)
    delivery_city = models.CharField(max_length=30, blank=True, null=True, default=None)
    delivery_state = models.CharField(max_length=2, blank=True, null=True, default=None)

    def __str__(self):
        return f"Title: {self.title} Description:{self.description} Price:{self.price} Qty:{self.quantity}"

class PaymentType(models.Model):
    """Defines a payment type.


        Author:Jase Hackman

        Returns: PaymentType Name
    """
    name = models.CharField(max_length = 50)
    account_number = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    delete_date = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    """ Defines an order

        Author: Rachel Daniel
        Methods: __str__ returns full name and completed (bool)
    """

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.PROTECT, default=None, null=True, blank=True)
    delete_date = models.DateTimeField(default=None, null=True, blank=True)

    def __str__(self):
        return f"Order: {self.id}, Customer Name: {self.customer.user.first_name} {self.customer.user.last_name}, Payment Type: {self.payment_type.name if self.payment_type else None}"

class OrderProduct(models.Model):
    """Defines the join table model for a product that is assigned to an order

        Author: Brendan McCray
        Returns: __str__ productId and orderId

    """
    # cascade used here because open orders are hard deleted, so we want to remove join tables also
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"Product: {self.product} Order:{self.order}"

