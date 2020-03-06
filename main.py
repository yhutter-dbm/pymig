from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import logging

from models.gallery import Gallery
from models.side_nav import SideNav
from helpers.string_helper import StringHelper
from helpers.side_nav_helper import SideNavHelper
from helpers.gallery_helper import GalleryHelper
app = Flask("Pymig")

# Debug flag for logging etc.
debug = True

# Only enable logger when not in debug mode...
app.logger.disabled = not debug

if debug:
    app.logger.setLevel(logging.DEBUG)

# The app has a basic template called layout. I used https://hackersandslackers.com/flask-jinja-templates/ for inspiration.


# Keep track of all galleries
galleries = []

# Global variables for UI
side_nav_elements = [
    SideNav(
        title='My Galleries',
        link='my_galleries',
        active=False
    ),
    SideNav(
        title='Create',
        link='create_new_gallery',
        active=False
    ),
    SideNav(
        title='Search',
        link='search',
        active=False
    )
]

current_path = "My Galleries"


# Variables for file handling
base_path = "./galleries/"
json_file_path = "./galleries.json"


@app.route('/')
@app.route('/my_galleries/')
def my_galleries():
    current_path = "My Galleries"
    result = SideNavHelper.set_active_side_nav_element(
        current_path, side_nav_elements, app.logger)

    # Load from json...
    galleries = GalleryHelper.load_from_json(json_file_path, app.logger)
    return render_template("my_galleries.html",
                           side_nav_elements=result,
                           current_path=current_path,
                           galleries=galleries)


@app.route('/create_new_gallery/', methods=['GET', 'POST'])
def create_new_gallery():

    # This happens when the user has entered all relevant data for a gallery
    if request.method == "POST":
        current_path = "Confirm your new Gallery"
        result = SideNavHelper.set_active_side_nav_element(
            current_path, side_nav_elements, app.logger)
        # Extract the relevant information from the request
        new_gallery = Gallery(
            name=request.form.get("gallery-name", ''),
            tags=StringHelper.parse_tags_from_text(
                request.form.get("gallery-tags", ''), app.logger),
            is_favourite=request.form.get("gallery-favourite", False),
            # See: https://pythonise.com/series/learning-flask/the-flask-request-object -> Multiple files section
            images=[],
            logger=app.logger
        )

        new_gallery.set_file_paths(
            base_path, request.files.getlist("gallery-images"))

        # Save to disk
        GalleryHelper.save_to_disk(
            base_path, new_gallery,
            request.files.getlist("gallery-images"), app.logger)

        # Add to existing galleries
        galleries.append(new_gallery)

        # Save as json file...
        GalleryHelper.save_to_json(json_file_path, galleries, app.logger)

        return redirect(url_for("my_galleries"))

    current_path = "Create"
    result = SideNavHelper.set_active_side_nav_element(
        current_path, side_nav_elements, app.logger)

    return render_template("create_new_gallery.html",
                           side_nav_elements=result,
                           current_path=current_path)


@app.route('/search/')
def search():
    current_path = "Search"
    result = SideNavHelper.set_active_side_nav_element(
        current_path, side_nav_elements, app.logger)
    return render_template("search.html",
                           side_nav_elements=result,
                           current_path=current_path)


if __name__ == "__main__":
    app.run(debug=debug, port=5000)
