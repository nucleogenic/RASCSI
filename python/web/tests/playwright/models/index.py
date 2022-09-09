class Index:
    """
    Page object modal for index page
    """

    def __init__(self, page):
        self.page = page
        self.page.goto("/")


    def reload(self):
        self.page.goto("/")
