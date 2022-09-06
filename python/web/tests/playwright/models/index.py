import os
import pathlib
import shutil
import tempfile
import uuid

class Index:
    """ Page object modal for index page """

    def __init__(self, page):
        self.page = page
        self.page.goto("/")


    def reload(self):
        self.page.goto("/")


    # File management

    def create_empty_disk_image(self, image_type = "hds", size = "1"):
        image_file_name = str(uuid.uuid4())

        form = self.page.locator("form[action='/files/create']")
        print(form)
        form.locator("input[name='file_name']").fill(image_file_name)
        form.locator("select[name='type']").select_option(image_type)
        form.locator("input[name='size']").fill(size)
        form.locator("input[value='Create']").click()

        return f"{image_file_name}.{image_type}"


    def upload_file(self, source_file_path = None):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_name = str(uuid.uuid4()) + pathlib.PurePath(source_file_path).suffix
            file_path = f"{temp_dir}/{file_name}"
            shutil.copy2(source_file_path, f"{temp_dir}/{file_name}")

            with self.page.expect_file_chooser() as fc_info:
                self.page.click("text=Drop files here to upload")
                file_chooser = fc_info.value
                file_chooser.set_files(file_path)

            return file_name


    def download_url_to_images_dir(self, url):
        self.page.locator("table#download-to-image input[name='url']").fill(url)
        self.page.locator("table#download-to-image input[value='Download']").click()
        self.page.wait_for_url("/")


    def download_url_to_cdrom_image(self, url):
        form = self.page.locator("table#download-to-cdrom-image form")
        scsi_id = form.locator("select[name='scsi_id'] option:checked").text_content().strip()
        form.locator("input[name='url']").fill(url)
        form.locator("input >> text=Download and Mount CD-ROM image").click()
        self.page.wait_for_url("/")
        return scsi_id


    def rename_file(self, file_name, new_file_name):
        self.page.once("dialog", lambda dialog: dialog.accept(prompt_text=new_file_name))
        self.page.click(f"table#images >> text={file_name} >> .. >> input[value='Rename']")


    def copy_file(self, file_name, copied_file_name):
        self.page.once("dialog", lambda dialog: dialog.accept(prompt_text=copied_file_name))
        self.page.click(f"table#images >> text={file_name} >> .. >> input[value='Copy']")


    def delete_file(self, file_name):
        self.page.once("dialog", lambda dialog: dialog.accept())

        if file_name[-3:] == "zip":
            # Up an extra 2 levels due to the wrapping <details> + <summary> element
            self.page.click(f"table#images >> text={file_name} >> .. >> .. >> .. >> input >> text=Delete")
        else:
            self.page.click(f"table#images >> text={file_name} >> .. >> input >> text=Delete")


    def extract_archive(self, file_name):
        self.page.click(f"table#images >> text={file_name} >> .. >> .. >> .. >> input[value='Extract All']")


    # Device management

    def detach_all_devices(self):
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.click("text=Detach All Devices")


    def detach_device(self, scsi_id):
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.click(f"table#devices >> td:first-child >> text=\"{scsi_id}\" >> .. >> input[value='Detach']")


    def eject_device(self, scsi_id):
        self.page.once("dialog", lambda dialog: dialog.accept())
        self.page.click(f"table#devices >> td:first-child >> text=\"{scsi_id}\" >> .. >> input[value='Eject']")


    def reserve_device(self, scsi_id, msg):
        self.page.once("dialog", lambda dialog: dialog.accept(prompt_text=msg))
        self.page.click(f"table#devices >> td:first-child >> text=\"{scsi_id}\" >> .. >> input[value='Reserve']")


    def release_device(self, scsi_id):
        self.page.click(f"table#devices >> td:first-child >> text=\"{scsi_id}\" >> .. >> input[value='Release']")


    def attach_image(self, image_file_name):
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


    # Settings

    def set_log_level(self, level):
        form = self.page.locator("table#set-log-level form")
        form.locator("select").select_option(level)
        form.locator("text=Set Log Level").click()

    def set_language(self, language):
        form = self.page.locator("table#set-language form")
        form.locator("select").select_option(language)
        form.locator("input[type='submit']").click()
