class IndexSettings:
    """
    Page object model for settings
    """

    def __init__(self, page):
        self.page = page


    def set_log_level(self, level):
        form = self.page.locator("table#set-log-level form")
        form.locator("select").select_option(level)
        form.locator("text=Set Log Level").click()


    def set_language(self, language):
        form = self.page.locator("table#set-language form")
        form.locator("select").select_option(language)
        form.locator("input[type='submit']").click()
