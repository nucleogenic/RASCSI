class IndexDeviceManagement:
    """
    Page object model for device management
    """

    def __init__(self, page):
        self.page = page


    def detach_all(self):
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.click("text=Detach All Devices")


    def detach(self, scsi_id):
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.click(f"table#devices >> td:first-child >> text=\"{scsi_id}\" >> .. >> input[value='Detach']")


    def eject(self, scsi_id):
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.click(f"table#devices >> td:first-child >> text=\"{scsi_id}\" >> .. >> input[value='Eject']")


    def reserve(self, scsi_id, msg):
        self.page.once("dialog", lambda dialog: dialog.accept(prompt_text=msg))
        self.page.click(f"table#devices >> td:first-child >> text=\"{scsi_id}\" >> .. >> input[value='Reserve']")


    def release(self, scsi_id):
        self.page.click(f"table#devices >> td:first-child >> text=\"{scsi_id}\" >> .. >> input[value='Release']")


    def attach(self, image_file_name):
        form = self.page.locator(f"table#images >> text={image_file_name} >> .. >> form")
        scsi_id = form.locator("select[name='scsi_id'] option:checked").text_content().strip()
        form.locator("input[value='Attach']").click()
        return scsi_id


    def attach_x6800_host_bridge(self):
        # TODO: Requires network bridge to be setup
        pass


    def attach_daynaport_scsi_link(self):
        # TODO: Requires network bridge to be setup
        pass

    
    def attach_host_services(self):
        form = self.page.locator("table#attach-peripheral-devices >> text=Host Services >> .. >> .. >> form")
        scsi_id = form.locator("select[name='scsi_id'] option:checked").text_content().strip()
        form.locator("input[value='Attach']").click()
        return scsi_id


    def attach_printer(self):
        form = self.page.locator("table#attach-peripheral-devices >> text=Printer >> .. >> .. >> form")
        scsi_id = form.locator("select[name='scsi_id'] option:checked").text_content().strip()
        form.locator("input[value='Attach']").click()
        return scsi_id
