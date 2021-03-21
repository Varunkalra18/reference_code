# BOOKSTORE WEB APPLICATION
## ABOUT THE WEBSITE
This is my final project for Harvard CS50x course. It's a website named “BookStore Web Application” developed in order to give bookstores owner a chance to let their buisness introduce to the world. Admin can add a Book, delete a book and can ban a customer if they found guilty. The admin while adding a book to the application has to enter the price of the book, book count and discount percentage with it. If customer orders a book or buy a book the application than check all the necessary conditions such as if the book is in stock or if a user is logged in or not or may be if they dont have sufficient amount in their wallet, after all such validation final the order is placed and admin get the request for processing orders. After admin confirms the request the notification will be sent to customer and then admin can process the order.

The second user is 'Customer'. First of all customer have to register themselves on our application with their email address and password of their choice. They can check if a particular book is available on our store through search bar on our index page, they can buy a book , or they can Add a Book to the 'CART' for future use. or they has the feature to add a book to the 'WISHLIST'. The customer can later change their username and password. Every activity they perform will generate a notification and can be seen in "All Notification feature" 
There are different sections on the website. You can search a book or can view them by their category. The latest book that is added in any category can be seen in the Top section. If you want to fing a particular book, use the search function.

Now the database of BookStore web is filled with users which contains the details of users like their username, hashed password, flag for their authorisation of certain services provided by application, if flagged true that means user is banned to use the services of the bookstore, and the amount balance they hold in their Bookstore wallet. Another tables like books contains the list of book that were added to the Bookstore. cart has the list of product that a particular user added in their cart. Wishlist is same as cart, and notification has the list of activity performed by particular user.

## Description
Web application is based on Flask framework. I used cs50 python lib for working with database, it can be freely downloaded from github or replaced with something like SQLite.

## How to use
To run the web application use these commands:
Run the virtual enviroment with
$ source env/scripts/activate 
$ export FLASK_APP=application.py
$ flask run

## Requirements
python 3
flask
cs50
werkzeug