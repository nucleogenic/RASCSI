import pytest
from playwright.sync_api import Playwright, BrowserContext, Page, sync_playwright, expect
import uuid

from models.index import Index
from models.index_file_management import IndexFileManagement
from models.index_device_management import IndexDeviceManagement

def test_upload(page: Page) -> None:
    index = Index(page)
    files = IndexFileManagement(page)

    # Upload
    file_name = files.upload("assets/test_image.hds")
    expect(page.locator(".dz-success-mark")).to_be_visible()
    index.reload()

    # Cleanup
    files.delete(file_name)


def test_rename(page: Page) -> None:
    index = Index(page)
    files = IndexFileManagement(page)

    # Setup
    file_name = files.create_empty_disk_image()
    new_file_name = f"{uuid.uuid4()}.tmp"

    # Rename
    files.rename(file_name, new_file_name)
    expect(page.locator(f"text=Image file renamed to: {new_file_name}")).to_be_visible()

    # Cleanup
    files.delete(new_file_name)


def test_copy(page: Page) -> None:
    index = Index(page)
    files = IndexFileManagement(page)

    # Setup
    file_name = files.create_empty_disk_image()
    copied_file_name = f"{uuid.uuid4()}.copy"

    # Copy
    files.copy(file_name, copied_file_name)
    expect(page.locator(f"text=Copy of image file saved as: {copied_file_name}")).to_be_visible()

    # Cleanup
    files.delete(file_name)
    files.delete(copied_file_name)


def test_extract(page: Page) -> None:
    index = Index(page)
    files = IndexFileManagement(page)

    # Setup
    archive_file_name = files.upload("assets/test_image.hds.zip")
    index.reload()

    # Extract
    files.extract(archive_file_name)
    expect(page.locator("text=Extracted 1 file(s)"))

    # Cleanup
    files.delete(archive_file_name)
    files.delete("test_image.hds")


def test_download_url_to_images_dir(page: Page, httpserver):
    index = Index(page)
    files = IndexFileManagement(page)

    # Setup
    image_file_name = str(uuid.uuid4())
    http_path = (f"/images/{image_file_name}")
    url = httpserver.url_for(http_path)

    with open("assets/test_image.hds", mode="rb") as file:
        test_image_data = file.read()

    httpserver.expect_request(http_path).respond_with_data(
        test_image_data,
        mimetype="application/octet-stream",
    )

    # Download from URL
    files.download_url_to_images_dir(url)
    expect(page.locator(f"text={image_file_name} downloaded to /home/pi/images")).to_be_visible()

    # Cleanup
    files.delete(image_file_name)


def test_download_to_cdrom_image(page: Page, httpserver):
    index = Index(page)
    files = IndexFileManagement(page)
    devices = IndexDeviceManagement(page)

    # Setup
    image_file_name = str(uuid.uuid4())
    http_path = (f"/images/{image_file_name}")
    url = httpserver.url_for(http_path)

    with open("assets/test_file.png", mode="rb") as file:
        test_image_data = file.read()

    httpserver.expect_request(http_path).respond_with_data(
        test_image_data,
        mimetype="application/octet-stream",
    )

    # Download from URL + create ISO + attach
    scsi_id = files.download_url_to_cdrom_image(url)
    expect(page.locator(f"text=Created CD-ROM ISO image with arguments \"-hfs\"")).to_be_visible()
    expect(page.locator(f"text=Saved image as: /home/pi/images/{image_file_name}.iso")).to_be_visible()

    # Cleanup
    devices.eject(scsi_id)
    devices.detach(scsi_id)
    files.delete(f"{image_file_name}.iso")
