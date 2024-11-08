from playwright.sync_api import Page, expect

# Tests for your routes go here

"""
We can render the home page
"""
# def test_get_home(page, test_web_address):
#     # We load a virtual browser and navigate to the /home page
#     page.goto(f"http://{test_web_address}/home")

#     # We look at the <p> tag
#     p_tag = page.locator("p")

#     # We assert that it has the text "This is the home."
#     expect(p_tag).to_have_text("This is the home.")

# Test title
def test_get_add_listing_page(page, test_web_address):
    page.goto(f"http://{test_web_address}/add_listing")
    expect(page).to_have_title("Makersbnb | Add a Listing")

# Test headings and form structure
def test_form_structure(page, test_web_address):
    page.goto(f"http://{test_web_address}/add_listing")

    expect(page.locator("h1")).to_have_text("Create a New Listing")
    expect(page.locator("h2").nth(0)).to_have_text("Listing Details")
    expect(page.locator("h2").nth(1)).to_have_text("Pricing Information")

# Test visibility of label and instructions
def test_labels_and_instructions(page, test_web_address):
    page.goto(f"http://{test_web_address}/add_listing")

    expect(page.locator("label[for='name']")).to_have_text("Listing Name")
    expect(page.locator("label[for='description']")).to_have_text("Description")
    expect(page.locator("label[for='price']")).to_have_text("Price per Night (GBP)")

    expect(page.locator("span.instructions").nth(0)).to_have_text("Enter a name that describes your listing, e.g., 'Rose Cottage'")
    expect(page.locator("span.instructions").nth(1)).to_have_text("Describe the features and atmosphere of your listing, e.g., 'A cozy cottage with a beautiful garden view.'")
    expect(page.locator("span.instructions").nth(2)).to_have_text("Specify the nightly rate for renting this listing.")

# Test submit button
def test_submit_button(page, test_web_address):
    page.goto(f"http://{test_web_address}/add_listing")
    submit_button = page.locator("input[type='submit']")

    expect(submit_button).to_be_visible()
    expect(submit_button).to_have_value("Add My Listing!")

def test_post_new_listing(page, test_web_address, db_connection):
    db_connection.seed('seeds/makersbnb.sql')
    page.goto(f"http://{test_web_address}/home")
    page.click("text=Add a property")
    # page.goto(f"http://{test_web_address}/add_listing") --> This was from before merge (i.e. no access to /home path)

    page.fill("input[name=name]", 'Test Listing')
    page.fill("input[name=description]", "Test description")
    page.fill("input[name=price]", "100")
    page.fill("input[name=user_id]", "1")
    page.click("input[type=submit]")
    
    expect(page.locator("h3").nth(3)).to_have_text("4: Test Listing")
    
    page.click("text=4: Test Listing")
    
    expect(page.locator("h2")).to_have_text("Test Listing")
    # expect(page.locator("h2")).to_have_text("Description: Test description")
    # expect(page.locator("p")).to_have_text("Price per night(GBP): £100")

def test_get_request_booking_page(page, test_web_address):
    id = 1
    page.goto(f"http://{test_web_address}/request_booking/{id}")
    h1_tag = page.locator("h1")
    # We assert that it has the text
    expect(h1_tag).to_have_text("Request a booking")

# checks for correct listing information - name, description, price
def test_get_listing_information(page, test_web_address):
    id = 3
    page.goto(f"http://{test_web_address}/request_booking/{id}")

    listing_name = page.locator("p").nth(0)
    description = page.locator("p").nth(1)
    price = page.locator("p").nth(2)

    expect(listing_name).to_have_text("Listing name: Seaside Serenity")
    expect(description).to_have_text("Description: A peaceful coastal retreat with stunning ocean views, a private balcony, and luxurious modern amenities.")
    expect(price).to_have_text("Price per night: £100")
    # complete when you know what home page looks like

# test for start and end date inputs
def test_start_and_end_dates(page, test_web_address):
    id = 2
    page.goto(f"http://{test_web_address}/request_booking/{id}")

    start_date_input = page.locator("input#start_date")
    end_date_input = page.locator("input#end_date")

    start_date_input.fill("2024-01-01")
    end_date_input.fill("2024-01-09")

    expect(start_date_input).to_have_value("2024-01-01")
    expect(end_date_input).to_have_value("2024-01-09")

    start_date_label = page.locator("label").nth(0)
    end_date_label = page.locator("label").nth(1)

    expect(start_date_label).to_have_text("Start Date")
    expect(end_date_label).to_have_text("End Date")

# tests if request booking button redirects to confirmation page with correct text
def test_requesting_a_booking_redirects(page, test_web_address):
    id = 2
    page.goto(f"http://{test_web_address}/request_booking/{id}")

    start_date_input = page.locator("input#start_date")
    end_date_input = page.locator("input#end_date")
    user_id_input = page.locator("input#user_id")

    start_date_input.fill("2024-01-01")
    end_date_input.fill("2024-01-09")
    user_id_input.fill(2)

    request_booking_button = page.locator("button")
    request_booking_button.click()

    booking_request_pending_h1 = page.locator("h1")
    booking_text_with_name = page.locator("p").nth(0)
    booking_dates = page.locator("p").nth(1)

    expect(booking_request_pending_h1).to_have_text("Booking Request Pending...")
    expect(booking_text_with_name).to_have_text("Your booking request for City Chic Loft is confirmed.")
    expect(booking_dates).to_have_text("Dates: 2024-01-01 to 2024-01-09")

# tests if go back to hompepage works on booking confirmation page
def test_go_back_homepage(page, test_web_address):
    id = 1
    page.goto(f"http://{test_web_address}/request_booking/{id}")

    start_date_input = page.locator("input#start_date")
    end_date_input = page.locator("input#end_date")

    start_date_input.fill("2024-01-01")
    end_date_input.fill("2024-01-09")

    request_booking_button = page.locator("button")
    request_booking_button.click()

    back_to_homepage_button = page.locator("button")
    back_to_homepage_button.click()
    assert page.url == f"http://{test_web_address}/home"

# test home listings
"""
GET /home
When: I open up the home
Then: I receive a list of all listings in the repository
"""
def test_get_listings(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/home")
    div_tags = page.locator("div")
    expect(div_tags).to_have_text([
        "1: Alpine Retreat Lodge",
        "2: City Chic Loft",
        "3: Seaside Serenity"
    ])

# test sign-up redirect 
"""
POST /sign_up
When: I enter an email, a  password and a username and click 'submit'
Then: I am redirtected to the home page.
"""
def test_post_user_sign_up_redirects_to_home(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/sign_up")

    page.fill("input[name=username]", 'doug_91')
    page.fill("input[name=email]", 'example@outlook.com')
    page.fill("input[name=password]", 'Password1!!')
    page.click("input[type=submit]")

    expect(page.locator("h1")).to_have_text("MakersBnB")

# test sign-up invalid password erroe message
"""
POST /sign_up
When: I enter an email, an INVALID password and a username and click 'submit'
Then: An error message is diaplayed at the top of the POST form page
"""
def test_post_user_sign_up_password_is_valid_too_short(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/sign_up")

    page.fill("input[name=username]", 'doug_91')
    page.fill("input[name=email]", 'example@outlook.com')
    page.fill("input[name=password]", 'hello')
    page.click("input[type=submit]")

    expect(page.locator(".errors-class")).to_have_text("* Your password must be at least 8 characters long")

def test_post_user_sign_up_password_is_valid_no_spec_char(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/sign_up")

    page.fill("input[name=username]", 'doug_91')
    page.fill("input[name=email]", 'example@outlook.com')
    page.fill("input[name=password]", 'Password')
    page.click("input[type=submit]")

    expect(page.locator(".errors-class")).to_have_text("* Your password must contain at least one of the following special character ('!', '@', '$', '%' or '&')")

def test_post_user_sign_up_password_is_valid_empty_input(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/sign_up")

    page.fill("input[name=username]", 'doug_91')
    page.fill("input[name=email]", 'example@outlook.com')
    page.fill("input[name=password]", '')
    page.click("input[type=submit]")

    expect(page.locator(".errors-class")).to_have_text("* Please add a valid password")


# test sign-up invalid email error message
"""
POST /sign_up
When: I enter an INVALID email, a password and a username and click 'submit'
Then: An error message is diaplayed at the top of the POST form page
"""
def test_post_user_sign_up_email_is_valid_empty_input(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/sign_up")

    page.fill("input[name=username]", 'doug_91')
    page.fill("input[name=email]", "")
    page.fill("input[name=password]", 'Password1!')
    page.click("input[type=submit]")

    expect(page.locator(".errors-class")).to_have_text("* Please add a valid email")

def test_post_user_sign_up_email_is_valid_no_at(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/sign_up")

    page.fill("input[name=username]", 'doug_91')
    page.fill("input[name=email]", "example.com")
    page.fill("input[name=password]", 'Password1!')
    page.click("input[type=submit]")

    expect(page.locator(".errors-class")).to_have_text("* Please add a valid email")

def test_post_user_sign_up_email_is_valid_no_at(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/sign_up")

    page.fill("input[name=username]", 'doug_91')
    page.fill("input[name=email]", "example@outlook")
    page.fill("input[name=password]", 'Password1!')
    page.click("input[type=submit]")

    expect(page.locator(".errors-class")).to_have_text("* Please add a valid email")

def test_post_user_sign_up_email_is_valid_email_already_exists(db_connection, page, test_web_address):
    db_connection.seed("seeds/makersbnb.sql")
    page.goto(f"http://{test_web_address}/sign_up")

    page.fill("input[name=username]", 'doug_91')
    page.fill("input[name=email]", "doug@email.com")
    page.fill("input[name=password]", 'Password1!')
    page.click("input[type=submit]")

    expect(page.locator(".errors-class")).to_have_text("* This email already exists. Please use a unique email")
