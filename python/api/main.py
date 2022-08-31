from fastapi import FastAPI, Request

from rascsi.socket_cmds import SocketCmds
from rascsi.ractl_cmds import RaCtlCmds
from rascsi.file_cmds import FileCmds
from rascsi.sys_cmds import SysCmds

from rascsi.common_settings import (
    CFG_DIR,
    CONFIG_FILE_SUFFIX,
    PROPERTIES_SUFFIX,
    ARCHIVE_FILE_SUFFIXES,
    RESERVATIONS,
)

sock_cmd = SocketCmds(host="192.168.1.32", port=6868)
ractl_cmd = RaCtlCmds(sock_cmd=sock_cmd, token="doge")
file_cmd = FileCmds(sock_cmd=sock_cmd, ractl=ractl_cmd, locale="en", token="doge")
sys_cmd = SysCmds()

app = FastAPI()


@app.get("/images")
async def read_images():
    return file_cmd.list_images()


@app.get("/server_info")
async def read_server_info():
    return ractl_cmd.get_server_info()


@app.get("/devices")
async def read_devices():
    return ractl_cmd.list_devices()


@app.post("/devices")
async def create_device(request: Request):
    data = await request.form()
    return data.keys()