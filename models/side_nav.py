class SideNav():
	def __init__(self, title, link, active):
		self.title = title
		self.link = link
		self.active = active

	def reset(self):
		self.active = False