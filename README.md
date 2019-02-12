# Welcome to Bangazon

This web application is the source code for the Bangazon e-commerce web site. It is powered by Python and Django.

## Installation
- Create an empty directory to house your new project
- run `virtualenv env` to create a virtual environment within that directory
- run `source env/bin/activate` to initialize a virtual environment (`deactivate` to exit environment)
- run `git clone [repository id]`
- run `cd bangazon-workflow`
- run `pip install -r requirements.txt`

## Seed a Starter Database
- Run `python manage.py makemigrations website`
- Run `python manage.py migrate`
- If you want some data to play with, run `python manage.py loaddata db.json`
- Initialize the project using the command line by typing `python manage.py runserver` in the main directory.
- Access the application in a browser at `http://localhost:8000/website`.

## Products
- From the homepage, if you select <em>Shop</em> you will be taken to a list of all products
- If you select <em>View Details</em> on any product listing, you will then be taken to a view of all product details and be given the option to add the product to your cart.
- If you add a product to your cart and are logged in, you will be redirected to the view all products page with a success message to confirm that the product was added to your cart
- If you try to add a product to your cart and are not currently logged in, you will be redirected to the login page with a message encouraging you to login to proceed

## Sell a Product
- When a user is logged in, there is an affordance in the navbar to Add a Product.
- User can add the details for their product and add it to the market place.

## Payment Types
- From the User Settings page, Users can add payment types to their account so they can complete their order.
- Users can also delete payment types they no longer want to use at Bangazon.
