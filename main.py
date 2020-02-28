from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import make_response
from models.gallery import Gallery
from models.side_nav import SideNav
from helpers.string_helper import parse_tags_from_text

app = Flask("Pymig")

# The app has a basic template called layout. I used https://hackersandslackers.com/flask-jinja-templates/ for inspiration.

# Global variables for UI
side_nav_elements = [
						SideNav(
							title = 'My Galleries',
							link = 'my_galleries',
							active = False
						),
						SideNav(
							title = 'Create',
							link = 'create_new_gallery',
							active = False
						),
						SideNav(
							title = 'Search',
							link = 'search',
							active = False
						)
					]

current_path = "My Galleries"

def reset_all_active_states(side_nav_elements):
	for side_nav_element in side_nav_elements:
		side_nav_element.reset()

	return side_nav_elements

def set_active_side_nav_element(current_path, side_nav_elements):
	side_nav_elements = reset_all_active_states(side_nav_elements)
	# We set the element activate which has a matching key in the side nav elements
	for side_nav_element in side_nav_elements:
		if side_nav_element.title == current_path:
			side_nav_element.active = True
	return side_nav_elements

@app.route('/')
def home():
    return render_template("home.html", side_nav_elements=side_nav_elements)

@app.route('/my_galleries/')
def my_galleries():
	current_path = "My Galleries"
	result = set_active_side_nav_element(current_path, side_nav_elements)
	return render_template("my_galleries.html", side_nav_elements=result, current_path=current_path)

@app.route('/create_new_gallery/', methods=['GET', 'POST'])
def create_new_gallery():

	# This happens when the user has entered all relevant data for a gallery -> we show a confirmation page with the entered details
	if request.method == "POST":
		current_path = "Confirm your new Gallery"
		result = set_active_side_nav_element(current_path, side_nav_elements)
		# Extract the relevant information from the request
		new_gallery = Gallery(
			name = request.form.get("gallery-name", ''),
			tags = parse_tags_from_text(request.form.get("gallery-tags", '')),
			is_favourite = request.form.get("gallery-favourite", False),
			# See: https://pythonise.com/series/learning-flask/the-flask-request-object -> Multiple files section
			images = request.files.getlist("gallery-images")
		)
		return render_template("confirm_new_gallery.html", side_nav_elements=result, current_path=current_path, gallery=new_gallery)

	current_path = "Create"
	result = set_active_side_nav_element(current_path, side_nav_elements)

	return render_template("create_new_gallery.html", side_nav_elements=result, current_path=current_path)

@app.route('/gallery_created/')
def gallery_created():
	return "TODO: Write to JSON..."

@app.route('/search/')
def search():
	current_path = "Search"
	result = set_active_side_nav_element(current_path, side_nav_elements)
	return render_template("search.html", side_nav_elements=result, current_path=current_path)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
