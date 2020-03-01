class SideNavHelper():

	"""
	This method resets the activate state of all side_nav_elements to False
	"""
	@staticmethod
	def reset_all_active_states(side_nav_elements):
		for side_nav_element in side_nav_elements:
			side_nav_element.reset()

		return side_nav_elements

	"""
	Sets the active element in the array active depending on the current path. The active element is determined by a matching title
	"""
	@staticmethod
	def set_active_side_nav_element(current_path, side_nav_elements):
		side_nav_elements = SideNavHelper.reset_all_active_states(side_nav_elements)
		# We set the element activate which has a matching key in the side nav elements
		for side_nav_element in side_nav_elements:
			side_nav_element.active = side_nav_element.title == current_path
		return side_nav_elements
