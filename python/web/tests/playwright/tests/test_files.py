import pytest
from playwright.sync_api import Playwright, BrowserContext, Page, sync_playwright, expect
import uuid

from models.index import Index

def test_upload(page: Page) -> None:
    index = Index(page)

    # Upload
    file_name = index.upload_file("assets/test_image.hds")
    expect(page.locator(".dz-success-mark")).to_be_visible()
    index.reload()

    # Cleanup
    index.delete_file(file_name)


def test_rename(page: Page) -> None:
    index = Index(page)

    # Setup
    file_name = index.create_empty_disk_image()
    new_file_name = f"{uuid.uuid4()}.tmp"

    # Rename
    index.rename_file(file_name, new_file_name)
    expect(page.locator(f"text=Image file renamed to: {new_file_name}")).to_be_visible()

    # Cleanup
    index.delete_file(new_file_name)


def test_copy(page: Page) -> None:
    index = Index(page)

    # Setup
    file_name = index.create_empty_disk_image()
    copied_file_name = f"{uuid.uuid4()}.copy"

    # Copy
    index.copy_file(file_name, copied_file_name)
    expect(page.locator(f"text=Copy of image file saved as: {copied_file_name}")).to_be_visible()

    # Cleanup
    index.delete_file(file_name)
    index.delete_file(copied_file_name)


def test_extract(page: Page) -> None:
    index = Index(page)

    # Setup
    archive_file_name = index.upload_file("assets/test_image.hds.zip")
    index.reload()

    # Extract
    index.extract_archive(archive_file_name)
    expect(page.locator("text=Extracted 1 file(s)"))

    # Cleanup
    index.delete_file(archive_file_name)
    index.delete_file("test_image.hds")


def test_download_url_to_images_dir(page: Page, httpserver):
    index = Index(page)

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
    index.download_url_to_images_dir(url)
    expect(page.locator(f"text={image_file_name} downloaded to /home/pi/images")).to_be_visible()

    # Cleanup
    index.delete_file(image_file_name)


def test_download_to_cdrom_image(page: Page, httpserver):
    index = Index(page)

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
    scsi_id = index.download_url_to_cdrom_image(url)
    expect(page.locator(f"text=Created CD-ROM ISO image with arguments \"-hfs\"")).to_be_visible()
    expect(page.locator(f"text=Saved image as: /home/pi/images/{image_file_name}.iso")).to_be_visible()

    # Cleanup
    index.eject_device(scsi_id)
    index.detach_device(scsi_id)
    index.delete_file(f"{image_file_name}.iso")


