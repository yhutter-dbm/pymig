import os
import json


class GalleryHelper():

    @staticmethod
    def save_to_disk(base_path, gallery, images, logger):
        # No point in creating the folder if it already exists...
        gallery_path = base_path + gallery.name + "/"
        if not os.path.isdir(gallery_path):
            os.makedirs(gallery_path)
            logger.info("Gallery structure was created")
        else:
            logger.warning("Gallery path already exists...")

        # Copy over the images, see: https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
        for image in images:
            image.save(gallery_path + image.filename)

    @staticmethod
    def save_to_json(file_name, galleries, logger):

        # Convert galleries to dictionary array in order to serialize easily as JSON
        converted_galleries = []
        for gallery in galleries:
            converted_galleries.append(gallery.to_dictionary_data_structure())

        # See: https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
        with open(file_name, 'w', encoding="utf-8") as save_file:
            json.dump(converted_galleries, save_file)

    @staticmethod
    def load_from_json(file_name, logger):
        # Check if json file actually exists otherwise return empty array
        if os.path.isfile(file_name):
            with open(file_name, "r", encoding="utf-8") as save_file:
                result = json.load(save_file)
                logger.info("Loaded the following data: ", result)
                return result
        return []
