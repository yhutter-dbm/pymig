from flask import Flask
from flask import render_template

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
						'title': 'Create a new Gallery',
						'link': 'create_new_gallery',
						'active': False
						},
						{
						'title': 'Search',
						'link': 'search',
						'active': False
						}]

current_path = "My Galleries"

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

@app.route('/create_new_gallery/')
def create_new_gallery():
	current_path = "Create a new Gallery"
	result = set_active_side_nav_element(current_path, side_nav_elements)
	return render_template("create_new_gallery.html", side_nav_elements=result, current_path=current_path)

@app.route('/search/')
def search():
	current_path = "Search"
	result = set_active_side_nav_element(current_path, side_nav_elements)
	return render_template("search.html", side_nav_elements=result, current_path=current_path)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
