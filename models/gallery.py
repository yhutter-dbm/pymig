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
            self.images.append(gallery_full_path + image.filename)
        self.logger.info("The current image paths  are ", self.images)

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
