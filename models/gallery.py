class Gallery():
	def __init__(self, name, tags, is_favourite, images, logger):
		self.name = name
		self.tags = tags
		self.is_favourite = is_favourite
		self.images = images
		self.logger = logger

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
		return result
	