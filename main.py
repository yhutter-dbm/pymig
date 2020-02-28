from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
from flask import make_response

app = Flask("Pymig")

# The app has a basic template called layout. I used https://hackersandslackers.com/flask-jinja-templates/ for inspiration.

# Global variables for UI
side_nav_elements = [
						{
						'title': 'My Galleries',
						'link': 'my_galleries',
						'active': False
						},
						{
						'title': 'Create',
						'link': 'create_new_gallery',
						'active': False
						},
						{
						'title': 'Search',
						'link': 'search',
						'active': False
						}]

current_path = "My Galleries"

def parse_tags_from_text(text):
	result =  []

	# Remove all unnecessary characters
	text = text.replace(',', '').replace('.', '').replace('\r\n', '').replace(' ', '')

	# We assume that a tag is beginning with #
	result = text.split('#')

	# Remove all empty entries from the list, see: https://www.geeksforgeeks.org/python-remove-empty-strings-from-list-of-strings/
	result = list(filter(None, result))
	return result

def reset_all_active_states(side_nav_elements):
	for element in side_nav_elements:
		element['active'] = False

	return side_nav_elements

def set_active_side_nav_element(current_path, side_nav_elements):
	side_nav_elements = reset_all_active_states(side_nav_elements)
	# We set the element activate which has a matching key in the side nav elements
	for element in side_nav_elements:
		if element['title'] == current_path:
			element['active'] = True
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
		new_gallery = {}
		new_gallery["name"] = request.form.get("gallery-name", '')
		new_gallery["tags"] = parse_tags_from_text(request.form.get("gallery-tags", ''))
		new_gallery["favourite"] = request.form.get("gallery-favourite", False)
		# See: https://pythonise.com/series/learning-flask/the-flask-request-object -> Multiple files section
		new_gallery["images"] = request.files.getlist("gallery-images")
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
