import os
from flask import Flask, request, render_template, redirect, url_for
from lib.database_connection import get_flask_database_connection

from lib.booking import *
from lib.booking_repository import *

from lib.listing import Listing
from lib.listing_repository import ListingRepository
from datetime import datetime
from lib.user_repository import UserRepository
from lib.user import User

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==

# GET /home
# Returns the homepage
# Try it:
#   ; open http://localhost:5001/home
# @app.route('/home', methods=['GET'])
# def get_home():
#     return render_template('home.html')

@app.route('/add_listing', methods=['GET'])
def get_add_listing():
    return render_template('add_listing.html')

@app.route('/request_booking/<id>', methods=['GET'])
def get_request_booking(id):
    connection = get_flask_database_connection(app)
    listing_repository = ListingRepository(connection)

    listing = listing_repository.find(id)

    id = listing.id
    name = listing.name
    description = listing.description
    price = listing.price

    return render_template('request_booking.html', id=id, name=name, description=description, price=price)

@app.route('/request_booking/<id>', methods=['POST'])
def post_request_booking(id):
    connection = get_flask_database_connection(app)
    
    start_date = request.form.get("start_date")
    end_date = request.form.get("end_date")
    user_id = request.form.get("user_id")

    listing_repository = ListingRepository(connection)
    listing = listing_repository.find(id)

    id = listing.id
    name = listing.name
    description = listing.description
    price = listing.price

    booking = Booking(None, id, user_id, start_date, end_date, "pending")
    errors = booking.generate_errors()

    if not booking.is_valid():
        print(errors)
        return render_template('request_booking.html', id=id, name=name, description=description, price=price, errors=errors)

    booking_repository = BookingRepository(connection)
    booking_repository.create(booking)

    return redirect(url_for('request_booking_pending', id=id, start_date=start_date, end_date=end_date, errors=errors))

# pending booking page
@app.route('/request_booking_pending', methods=['GET'])
def request_booking_pending():
    id = request.args.get("id")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    connection = get_flask_database_connection(app)
    listing_repository = ListingRepository(connection)
    listing = listing_repository.find(id)
    listing_name = listing.name

    return render_template('request_booking_pending.html', start_date=start_date, end_date=end_date, name=listing_name)

# add_listing_branch
@app.route("/listings/new", methods=['POST'])
def post_new_listing():
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)

    name = request.form['name']
    description = request.form['description']
    price = int(request.form['price'])
    user_id = request.form['user_id']
    listing = Listing(None, name, description, price, user_id)

    if not listing.is_valid():
        errors = listing.generate_errors()
        print(errors)
        return render_template('add_listing.html', errors=errors)
    
    repository.create(listing)
    return redirect(f"/home")

# get all listings on homepage
@app.route('/home', methods=['GET'])
def get_listings():
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    listings = repository.all()
    print(listings)
    return render_template('home.html', listings=listings)

# add anchors to listings page
@app.route('/home/<int:listing_id>', methods=['GET'])
def show_listing(listing_id):
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    listing = repository.find(listing_id)
    return render_template('/show_listing.html', listing=listing)


# http://local:5001/sign_up
@app.route('/sign_up', methods=['GET'])
def get_sign_up_form():
    return render_template('sign_up.html')

@app.route('/sign_up', methods=['POST'])
def create_account():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    user = User(None, username, email, password)

    if not user.is_valid(app):
        errors = user.generate_errors(app)
        return render_template('sign_up.html', errors=errors)

    repository.create(user)
    return redirect(f"/home")

# invalid parameters
def has_invalid_user_parameters(form):
    return 'username' not in form or \
        'email' not in form or \
            'password' not in form            
            
@app.route('/landing')
def index():
    return render_template('landing.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_account():
    connection = get_flask_database_connection(app)
    repository = UserRepository(connection)

    email = request.form.get('email')
    password_value = request.form.get('password')
    
    user_check = repository.find_by_email(email)
    if user_check is None:
        return render_template('sign_up.html')

    if user_check.password != password_value:
        return render_template('login.html')
    return redirect(f"/home")



# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
