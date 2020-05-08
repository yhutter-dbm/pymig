from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
from flask import redirect
import logging

from models.gallery import Gallery
from models.side_nav import SideNav
from helpers.side_nav_helper import SideNavHelper
from helpers.gallery_helper import GalleryHelper

# Setup application
app = Flask("Pymig")

# Debug flag for logging etc.
debug = True

# Only enable logger when not in debug mode...
app.logger.disabled = not debug

if debug:
    app.logger.setLevel(logging.DEBUG)

# The app has a basic template called layout. I used https://hackersandslackers.com/flask-jinja-templates/ for inspiration.

# Global variables for UI
# For more information about icons see: https://getuikit.com/docs/icon
side_nav_elements = [
    SideNav(
        title='My Galleries',
        link='my_galleries',
        active=False,
        icon="album"
    ),
    SideNav(
        title='Create',
        link='create_new_gallery',
        active=False,
        icon="pencil"
    ),
    SideNav(
        title='Search',
        link='search',
        active=False,
        icon="search"
    ),
    SideNav(
        title='Favourites',
        link='favourites',
        active=False,
        icon="heart"
    )
]

@app.route('/')
@app.route('/my_galleries/')
def my_galleries():
    current_path = "My Galleries"
    result = SideNavHelper.set_active_side_nav_element(
        current_path, side_nav_elements, app.logger)

    # Load from json...
    galleries = GalleryHelper.load_from_json(app.logger)
    return render_template("my_galleries.html",
                           side_nav_elements=result,
                           current_path=current_path,
                           galleries=galleries)


@app.route('/create_new_gallery/', methods=['GET', 'POST'])
def create_new_gallery():
    # Load from json...
    galleries = GalleryHelper.load_from_json(app.logger)
    current_path = "Create"

    result = SideNavHelper.set_active_side_nav_element(current_path, side_nav_elements, app.logger)


    # This happens when the user has entered all relevant data for a gallery
    if request.method == "POST":
        try:
            # Create from request object
            new_gallery = GalleryHelper.create_gallery_from_request(request, app.logger)

            # Add to existing galleries
            galleries.append(new_gallery)

            # Save as json file...
            GalleryHelper.save_to_json(galleries, app.logger)

            return redirect(url_for("my_galleries"))
        except Exception as error:
            return redirect(url_for("error", message=str(error), rescue_link=url_for('create_new_gallery')))

    return render_template("create_new_gallery.html",
                           side_nav_elements=result,
                           current_path=current_path,
                           requires_show_uploaded_files=True)


@app.route('/look_at_gallery/<gallery_name>')
def look_at_gallery(gallery_name=""):
    current_path = "My Galleries"
    result = SideNavHelper.set_active_side_nav_element(
        current_path, side_nav_elements, app.logger)

    galleries = GalleryHelper.load_from_json(app.logger)
    found_gallery = GalleryHelper.get_gallery_with_name(galleries, gallery_name, app.logger)
    return render_template("look_at_gallery.html",
                           side_nav_elements=result,
                           current_path=current_path,
                           gallery=found_gallery,
                           requires_init_masonry=True)

@app.route('/edit_gallery/<gallery_name>', methods=['POST', 'GET'])
def edit_gallery(gallery_name=""):
    current_path = "My Galleries"
    result = SideNavHelper.set_active_side_nav_element(
        current_path, side_nav_elements, app.logger)

    # Load from json...
    galleries = GalleryHelper.load_from_json(app.logger)
    # Find the gallery with the corresponding name
    found_gallery = GalleryHelper.get_gallery_with_name(galleries, gallery_name, app.logger)

    if request.method == "POST":
        try:
            updated_gallery = GalleryHelper.update_gallery_from_request(found_gallery, request, app.logger)

            # Remove the unedited one from galleries
            galleries.remove(found_gallery)

            # Add the newly edited one to galleries
            galleries.append(updated_gallery)

            # Save as json file...
            GalleryHelper.save_to_json(galleries, app.logger)
            return redirect(url_for("my_galleries"))
        except Exception as error:
            return redirect(url_for("error", message=str(error), rescue_link=url_for('edit_gallery', gallery_name=gallery_name)))



    return render_template("edit_gallery.html",
                           side_nav_elements=result,
                           current_path=current_path,
                           gallery=found_gallery,
                           requires_show_uploaded_files=True)

@app.route('/delete_gallery/<gallery_name>', methods=['POST', 'GET'])
def delete_gallery(gallery_name=""):
    current_path = "My Galleries"
    result = SideNavHelper.set_active_side_nav_element(current_path, side_nav_elements, app.logger)

    # Load from json...
    galleries = GalleryHelper.load_from_json(app.logger)
    # Find the gallery with the corresponding name
    found_gallery = GalleryHelper.get_gallery_with_name(galleries, gallery_name, app.logger)

    if request.method == "POST":

        try:
            # Delete from file system
            GalleryHelper.delete_gallery(found_gallery.name, app.logger)

            # Delete from global object
            galleries.remove(found_gallery)

            # Save as json file...
            GalleryHelper.save_to_json(galleries, app.logger)

            return redirect(url_for("my_galleries"))

        except Exception as error:
            return redirect(url_for("error", message=str(error), rescue_link=url_for('delete_gallery', gallery_name=gallery_name)))

    return render_template("confirm_delete_gallery.html",
                           side_nav_elements=result,
                           current_path=current_path,
                           gallery=found_gallery)


@app.route('/search/', methods=["GET", "POST"])
def search():
    current_path = "Search"
    result = SideNavHelper.set_active_side_nav_element(
        current_path, side_nav_elements, app.logger)

    # Load from json...
    galleries = GalleryHelper.load_from_json(app.logger)
    
    tags = []
    # Get all tags from the available galleries
    for gallery in galleries:
        tags = tags + gallery.tags

    # Remove duplicated tags
    tags = list(set(tags))

    # Sort alphabetically
    tags = sorted(tags)

    if request.method == "POST":
        # Search for the galleries with the data from the POST request
        search_title = request.form.get("search-title", "")
        tags_to_include = request.form.getlist("tag-to-include") or []

        found_galleries = GalleryHelper.filter_galleries(galleries, search_title, tags_to_include)
        return render_template("search_result.html",side_nav_elements=result,
                           current_path=current_path,
                           galleries=found_galleries)

    return render_template("search.html",
                           side_nav_elements=result,
                           current_path=current_path,
                           tags=tags)

@app.route('/favourites/')
def favourites():
    current_path = "Favourites"
    result = SideNavHelper.set_active_side_nav_element(
        current_path, side_nav_elements, app.logger)

    # Load from json...
    all_galleries = GalleryHelper.load_from_json(app.logger)

    # Filter out non favourite galleries
    galleries = []

    for gallery in all_galleries:
        print(gallery.is_favourite)
        if gallery.is_favourite == True:
            galleries.append(gallery)

    return render_template("favourite_galleries.html",
                           side_nav_elements=result,
                           current_path=current_path,
                           galleries=galleries)

@app.route('/error')
def error():
    current_path = ""

    # We extract the information directly from the request as encoding the rescue link in the route itself does not work
    # See: https://stackoverflow.com/questions/24892035/how-can-i-get-the-named-parameters-from-a-url-using-flask
    message = request.args.get("message", "")
    rescue_link = request.args.get("rescue_link", None)
    result = SideNavHelper.set_active_side_nav_element(current_path, side_nav_elements, app.logger)
    return render_template("error.html", side_nav_elements=result,
    current_path=current_path, message=message, rescue_link=rescue_link)

if __name__ == "__main__":
    app.run(debug=debug, port=5000)
