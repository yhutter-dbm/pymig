import os

class Gallery():
    def __init__(self, logger, name="", tags=[], is_favourite=False, images=[], description=""):
        self.name = name
        self.tags = tags
        self.is_favourite = is_favourite
        self.images = images
        self.logger = logger
        self.description = description

    def set_file_paths(self, base_path, images):
        gallery_full_path = base_path + self.name + "/"
        for image in images:
            if image.filename:
                self.images.append(gallery_full_path + image.filename)

    def to_dictionary_data_structure(self):
        result = {}
        result["name"] = self.name
        result["tags"] = self.tags
        result["is_favourite"] = self.is_favourite
        result["images"] = self.images
        result["description"] = self.description
        return result

    def initialize_from_dictionary(self, dict):
        self.name = dict.get("name", "")
        self.is_favourite = dict.get("is_favourite", False)
        self.tags = dict.get("tags", [])
        self.images = dict.get("images", [])
        self.description = dict.get("description", "")

    def get_tags_str(self):
        result = ""
        if len(self.tags) > 0:
            for tag in self.tags:
                result = result + "#" + tag + " "
        return result

    def get_image_name(self, image):
        return image.split("/")[-1]

    def get_relative_image_path(self, image):
        os.path.join("./", image)

    def remove_images(self, images):
        for image in images:
            self.images.remove(image)
        return self.images

    def has_gallery_title(self, gallery_title):
        return self.name.lower().find(gallery_title) >= 0

    def has_tags(self, tags_to_include):
        for tag in self.tags:
            if tag in tags_to_include:
                return True
        return False
