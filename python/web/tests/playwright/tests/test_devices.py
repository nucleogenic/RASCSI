import pytest
from playwright.sync_api import Playwright, BrowserContext, Page, sync_playwright, expect

from models.index import Index
from models.index_device_management import IndexDeviceManagement
from models.index_file_management import IndexFileManagement

def test_reserve_and_release(page: Page) -> None:
    index = Index(page)
    devices = IndexDeviceManagement(page)
    files = IndexFileManagement(page)

    # Reserve (n.b. a device must not have previously been attached to this SCSI ID)
    devices.reserve(0, "Reserved ID #0")
    expect(page.locator("text=Reserved SCSI ID 0"))

    # Release
    devices.release(0)
    expect(page.locator("text=Released the reservation for SCSI ID 0"))


def test_attach_and_detach_image(page: Page) -> None:
    index = Index(page)
    devices = IndexDeviceManagement(page)
    files = IndexFileManagement(page)

    # Setup
    image_file_name = files.create_empty_disk_image()

    # Attach
    scsi_id = devices.attach_image(image_file_name)
    expect(page.locator(f"text=Attached {image_file_name} as Hard Disk to SCSI ID {scsi_id} LUN 0")).to_be_visible()

    # Detach
    devices.detach(scsi_id)
    expect(page.locator(f"text=Detached SCSI ID {scsi_id} LUN 0")).to_be_visible()

    # Cleanup
    files.delete(image_file_name)


@pytest.mark.skip(reason="Not implemented")
def test_attach_x68000_host_bridge(page: Page) -> None:
    pass


@pytest.mark.skip(reason="Not implemented")
def test_attach_daynaport_scsi_link(page: Page) -> None:
    pass


def test_attach_host_services(page: Page) -> None:
    index = Index(page)
    devices = IndexDeviceManagement(page)

    # Attach
    scsi_id = devices.attach_host_services()
    expect(page.locator(f"text=Attached Host Services to SCSI ID {scsi_id} LUN 0")).to_be_visible()

    # Cleanup
    devices.detach(scsi_id)


def test_attach_printer(page: Page) -> None:
    index = Index(page)
    devices = IndexDeviceManagement(page)

    # Attach
    scsi_id = devices.attach_printer()
    expect(page.locator(f"text=Attached Printer to SCSI ID {scsi_id} LUN 0")).to_be_visible()

    # Cleanup
    devices.detach(scsi_id)
