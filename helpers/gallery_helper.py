import os
import json
import shutil
from models.gallery import Gallery
from helpers.string_helper import StringHelper


base_path = "./static/galleries/"
absolute_base_path = "/static/galleries/"
json_file_path = "./static/galleries.json"

class GalleryHelper():

    @staticmethod
    def save_images_to_disk(gallery, images, logger):
        # No point in creating the folder if it already exists...
        gallery_path = base_path + gallery.name + "/"
        if not os.path.isdir(gallery_path):
            os.makedirs(gallery_path)
            logger.info("Gallery structure was created")
        else:
            logger.warning("Gallery path already exists...")

        # Copy over the images, see: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
        for image in images:
            if image.filename:
                image.save(gallery_path + image.filename)

    @staticmethod
    def rename_gallery_folder(old_name, new_name):
        print("Calling rename gallery folder with", old_name, new_name)
        if os.path.isdir(old_name):
            print("Renaming folder", old_name, "to", new_name)
            os.rename(old_name, new_name)

    @staticmethod
    def remove_images_from_disk(images_to_delete, logger):
        # Only delete if the path actually exists
        for image_to_delete in images_to_delete:
            logger.info("Deleting ", image_to_delete)
            if os.path.exists(image_to_delete):
                os.remove(image_to_delete)
            else:
                raise Exception("The image " + image_to_delete + " could not be deleted...")

    @staticmethod
    def save_to_json(galleries, logger):

        # Convert galleries to dictionary array in order to serialize easily as JSON
        converted_galleries = []
        for gallery in galleries:
            converted_galleries.append(gallery.to_dictionary_data_structure())

        # See: https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
        with open(json_file_path, 'w', encoding="utf-8") as save_file:
            json.dump(converted_galleries, save_file)

    @staticmethod
    def load_from_json(logger):
        # Check if json file actually exists otherwise return empty array
        if os.path.isfile(json_file_path):
            with open(json_file_path, "r", encoding="utf-8") as save_file:
                result_dicts = json.load(save_file)
                result_galleries = []
                # Convert dictionary back to gallery object...
                for dict in result_dicts:
                    gallery = Gallery(logger)
                    gallery.initialize_from_dictionary(dict)
                    result_galleries.append(gallery)
                logger.info("Loaded the following data: ", result_galleries)
                return result_galleries
        return []

    @staticmethod
    def get_gallery_with_name(galleries, gallery_name, logger):
        for gallerie in galleries:
            if gallerie.name == gallery_name:
                return gallerie
        # At this point the gallery was not found
        return None

    @staticmethod
    def create_gallery_from_request(request, logger):
        # Extract the relevant information from the request
        new_gallery = Gallery(
            logger=logger,
            name=request.form.get("gallery-name", ''),
            tags=StringHelper.parse_tags_from_text(
                request.form.get("gallery-tags", ''), logger),
            is_favourite=request.form.get("gallery-favourite", False),
            # See: https://pythonise.com/series/learning-flask/the-flask-request-object -> Multiple files section
            images=[],
            description = request.form.get("gallery-description", "")
        )

        gallery_images = request.files.getlist("gallery-images")

        if len(gallery_images) > 0:
            new_gallery.set_file_paths(absolute_base_path, gallery_images)

            # Save to disk
            GalleryHelper.save_images_to_disk(
                new_gallery,
                request.files.getlist("gallery-images"), logger)

        return new_gallery

    @staticmethod
    def update_gallery_from_request(gallery, request, logger):
        old_name = gallery.name
        new_name = request.form.get("gallery-name", '')

        if new_name == "":
            raise Exception("Gallery name cannot be empty")

        # In case the name has changed we need to update the folder structure
        if old_name != new_name:
            GalleryHelper.rename_gallery_folder(base_path + old_name, base_path + new_name)
            gallery.rename(new_name)

        images_to_delete = request.form.getlist("image-to-delete")

        # The images have an absolute path -> /static/galleries/<gallery>/<image>
        # However in order to delete them successfully it should be relative -> ./static/galleries....
        sanitized_images_to_delete = StringHelper.replace_first_occurrence("/", "./", images_to_delete)

        GalleryHelper.remove_images_from_disk(sanitized_images_to_delete, logger)

        # Then create a new gallery from the request
        new_gallery = GalleryHelper.create_gallery_from_request(request, logger)

        existing_images = gallery.remove_images(images_to_delete)

        # Only add those images to the object which should not have been deleted
        new_gallery.images = new_gallery.images + existing_images

        return new_gallery
