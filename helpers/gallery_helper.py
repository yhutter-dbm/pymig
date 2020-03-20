import os
import json
import shutil
from models.gallery import Gallery
from helpers.string_helper import StringHelper


base_path = "./static/galleries/"
absolute_base_path = "/static/galleries/"
json_file_path = "./static/galleries.json"

# We assume that the following characters are valid
# a-z / A-Z / 0-9, _, -, ' '
letters = list("abcdefghijklmnopqrstuvwxyz")
upper_case_letters = list("abcdefghijklmnopqrstuvwxyz".upper())
numbers = list("0123456789")
other_valid_characters = list("_- ")
valid_gallery_name_characters = letters + upper_case_letters + numbers + other_valid_characters
valid_image_name_characters = valid_gallery_name_characters # The same rule applies for images

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
        if os.path.isdir(old_name):
            os.rename(old_name, new_name)

    @staticmethod
    def remove_images_from_disk(images_to_delete, logger):
        # Only delete if the path actually exists
        for image_to_delete in images_to_delete:
            logger.info("Deleting ", image_to_delete)
            if os.path.exists(image_to_delete):
                os.remove(image_to_delete)

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
    def is_valid_gallery_name(gallery_name):
        gallery_name = gallery_name.strip()
        for character in gallery_name:
            if not character in valid_gallery_name_characters:
                return False
        return True

    @staticmethod
    def is_valid_image_name(image_name):
        image_name = image_name.strip()
        for character in image_name:
            if not character in valid_image_name_characters:
                return False
        return True

    @staticmethod
    def does_gallery_with_name_already_exist(gallery_name):
        gallery_path = base_path + gallery_name
        return os.path.exists(gallery_path)


    @staticmethod
    def create_gallery_from_request(request, logger, check_gallery_name = True):
        # Extract the relevant information from the request
        name = request.form.get("gallery-name", '')
        gallery_images = request.files.getlist("gallery-images")

        # Check if the name is valid
        if not GalleryHelper.is_valid_gallery_name(name):
            raise Exception("Invalid gallery name " + name + ". It should only contain numeric, alphanumeric, '_' , '-' or whitespaces")

        # Check if this gallery already exists
        if check_gallery_name and GalleryHelper.does_gallery_with_name_already_exist(name):
            raise Exception("The gallery name " + "'" + name + "'" + " does already exist")

        # Check if image names are valid
        for image in gallery_images:
            if not GalleryHelper.is_valid_image_name(image.filename):
                raise Exception("The image name " + "'" + image.filename + "'" + " contains invalid Characters. It should only contain numeric, alphanumeric, '_' , '-' or whitespaces")
        
        new_gallery = Gallery(
            logger=logger,
            name=name,
            tags=StringHelper.parse_tags_from_text(
                request.form.get("gallery-tags", ''), logger),
            is_favourite=request.form.get("gallery-favourite", False),
            # See: https://pythonise.com/series/learning-flask/the-flask-request-object -> Multiple files section
            images=[],
            description = request.form.get("gallery-description", "")
        )


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

        # Check if the name is valid
        if not GalleryHelper.is_valid_gallery_name(new_name):
            raise Exception("Invalid gallery name " + name + ". It should only contain numeric, alphanumeric, '_' , '-' or whitespaces")

        images_to_delete = request.form.getlist("image-to-delete")

        check_gallery_name = False

        # In case the name has changed we need to update the folder structure
        if old_name != new_name:
            # Only check gallery name in create from request if the name has actually changed...
            check_gallery_name = True

            # Check if this gallery already exists
            if GalleryHelper.does_gallery_with_name_already_exist(new_name):
                raise Exception("The gallery name " + "'" + new_name + "'" + " does already exist")

            # Rename the gallery folder
            GalleryHelper.rename_gallery_folder(base_path + old_name, base_path + new_name)

            # Rename the old gallery object so the paths are correctly updated
            gallery.name = new_name
            gallery.images = StringHelper.replace_first_occurrence(absolute_base_path + old_name, absolute_base_path + new_name, gallery.images)

            # Rename the images to delete because the still have the old name
            images_to_delete = StringHelper.replace_first_occurrence(absolute_base_path + old_name, absolute_base_path + new_name, images_to_delete)


        # The images have an absolute path -> /static/galleries/<gallery>/<image>
        # However in order to delete them successfully it should be relative -> ./static/galleries....
        sanitized_images_to_delete = StringHelper.replace_first_occurrence("/", "./", images_to_delete)

        GalleryHelper.remove_images_from_disk(sanitized_images_to_delete, logger)

        # Then create a new gallery from the request
        new_gallery = GalleryHelper.create_gallery_from_request(request, logger, check_gallery_name)

        existing_images = gallery.remove_images(images_to_delete)

        # Only add those images to the object which should not have been deleted
        new_gallery.images = new_gallery.images + existing_images

        # Make sure that the images are unique
        new_gallery.images = list(set(new_gallery.images))

        return new_gallery

    @staticmethod
    def delete_gallery(gallery_name, logger):
        gallery_path = base_path + gallery_name
        if os.path.exists(gallery_path):
            # See: https://linuxize.com/post/python-delete-files-and-directories/
            shutil.rmtree(gallery_path)

    @staticmethod
    def filter_galleries(galleries, gallery_title, tags_to_include):
        result = []

        gallery_title = gallery_title.strip()
        # Only include galleries where the gallery title matches or we have a matching tag
        for gallery in galleries:
            if gallery.has_gallery_title(gallery_title) or gallery.has_tags(tags_to_include):
                result.append(gallery)

        return result
