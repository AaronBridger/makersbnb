import os

from lib.database_connection import get_flask_database_connection
from lib.listing_repository import *
from lib.listing import *
from lib.user_repository import *
from lib.user import *
from flask import Flask, request, render_template, redirect

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==


@app.route('/add_listing', methods=['GET'])
def get_add_listing():
    return render_template('add_listing.html')

add_listing_branch
@app.route("/listings/new", methods=['POST'])
def post_new_listing():
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)

    name = request.form['name']
    description = request.form['description']
    price = request.form['price']
    user_id = request.form['user_id']
    listing = Listing(None, name, description, price, user_id)

    if not listing.is_valid():
        errors = listing.generate_errors()
        return render_template('templates/add_listing.html', errors=errors)
    
    repository.create(listing)
    return redirect(f"/index")

# get all listings on homepage
@app.route('/home', methods=['GET'])
def get_listings():
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)
    listings = repository.all()
    return render_template('home.html', listings=listings)

# add anchors to listings page
@app.route('/home/<int:listing_id>', methods=['GET'])
def show_listing(listing_id):
    connection = get_flask_database_connection(app)
    repository = ListingRepository(connection)

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5001)))
