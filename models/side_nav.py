class SideNav():
    def __init__(self, title, link, active, icon=""):
        self.title = title
        self.link = link
        self.active = active
        self.icon = icon

    def reset(self):
        self.active = False
