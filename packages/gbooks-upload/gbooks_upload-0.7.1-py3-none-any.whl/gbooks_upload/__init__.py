#!/usr/bin/env python3
import json
import logging
import time
from json import JSONDecodeError
from mimetypes import add_type
from pathlib import Path
from typing import Callable, Optional

import httplib2
import rich_click as click
import uvloop
from click.exceptions import BadParameter
from click.globals import get_current_context
from googleapiclient.discovery import Resource, build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from rich import print
from rich.logging import RichHandler

from google_internal_apis import cli, get_client
from google_internal_apis.cli import asyncio, verbose_flag

from .const import COOKIE_TXT, PATH
from .drive import upload_with_drive
from .endpoints import LibraryService
from .scotty import steal_cookie, upload_with_scotty

__version__ = "0.7.1"

logging.basicConfig(handlers=[RichHandler(rich_tracebacks=True)])

add_type("application/epub+zip", ".epub")


def get_http():
    assert argparser
    args = argparser.parse_args(["--noauth_local_webserver"])
    storage = Storage(PATH / "credentials.json")
    credentials = storage.get()
    if credentials is None:
        flow = flow_from_clientsecrets(
            PATH / "client_secrets.json",
            scope=[
                "https://www.googleapis.com/auth/drive.file",
                "openid",
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/books",
            ],
        )
        credentials = run_flow(flags=args, flow=flow, storage=storage)
    http = credentials.authorize(httplib2.Http())
    if credentials.access_token_expired:
        credentials.refresh(http)
    return http


def get_volume(
    books: Resource, name: Optional[str] = None, volumeId: Optional[str] = None
):
    return next(
        volume
        for volume in books.volumes().useruploaded().list().execute()["items"]
        if (volume["volumeInfo"]["title"] == name or volume["id"] == volumeId)
    )


def paginate(method: Callable, *args, **kwargs):
    request = method(*args, **kwargs)
    start_index = 0
    while request:
        res = request.execute()
        if "items" not in res:
            break
        yield from res["items"]
        start_index += len(res["items"])
        request = method(*args, startIndex=start_index, **kwargs)


@click.group()
@click.version_option(__version__)
def main() -> None:
    pass


main.add_command(cli.rpc)


@main.command()
@verbose_flag
@asyncio
async def login():
    """
    Login to Google with GHunt
    """
    from ghunt.modules.login import check_and_login

    await check_and_login(None)


@main.command()
@click.argument(
    "files",
    required=True,
    nargs=-1,
    type=click.Path(exists=True, readable=True, path_type=Path, dir_okay=False),
)
@click.option("--use-drive", is_flag=True)
@click.option("--bookshelf", help="Add the uploaded books to this bookshelf")
@verbose_flag
def upload(files: list[str], use_drive: bool, bookshelf: str):
    """
    Upload files to Google Books
    """

    http = get_http()

    books = build("books", "v1", http=http)
    drive = build("drive", "v3", http=http)

    uploads = [
        upload_with_drive(drive, books, filename)
        if use_drive
        else upload_with_scotty(books, filename)
        for filename in files
    ]
    for upl in uploads:
        monitor(books, upl["volumeId"])

    if not bookshelf:
        return

    print(
        uvloop.run(
            add_multiple_to_shelf([upl["volumeId"] for upl in uploads], bookshelf)
        )
    )


async def add_multiple_to_shelf(book_ids: list[str], shelf_name: str):
    service = await get_client(LibraryService)

    tag_id = await get_shelf(service, shelf_name)

    return await service.add_tags(book_ids, tag_id)


def load_json(ctx, param, filename):
    try:
        with open(filename) as f:
            return json.load(f)
    except JSONDecodeError as e:
        raise BadParameter(e) from e


@main.command()
@click.argument(
    "filename",
    type=click.Path(exists=True, readable=True, path_type=Path, dir_okay=False),
    callback=load_json,
)
@verbose_flag
def steal(data: dict):
    """
    Steal the cookie from a Chrome net-export log
    """
    cookie = steal_cookie(data)
    if not cookie:
        raise Exception("Could not find cookie")
    PATH.mkdir(parents=True, exist_ok=True)
    COOKIE_TXT.write_text(cookie)


@main.group()
def shelves():
    "Commands to manage shelves"
    pass


async def get_shelf(service: LibraryService, shelf_name: str):
    tags = await service.list_tags()

    if shelf_name not in tags["tags"]:
        ctx = get_current_context()
        param = next(p for p in ctx.command.params if p.name == "bookshelf")
        raise BadParameter(f'Shelf with name "{shelf_name}" not found', param=param)

    return tags["tags"][shelf_name]


@shelves.command("add")
@click.argument("book_id")
@click.argument("bookshelf")
@verbose_flag
@asyncio
async def add_to_shelf(book_id: str, bookshelf: str):
    "add book to shelf"
    service = await get_client(LibraryService)

    tag_id = await get_shelf(service, bookshelf)

    print(await service.add_tags([book_id], tag_id))


@shelves.command("list")
@verbose_flag
@asyncio
async def list_shelves():
    "list shelves"
    service = await get_client(LibraryService)

    tags = await service.list_tags()

    for name in tags["tags"]:
        print(name)


@main.group()
def books():
    "Commands to manage books"
    pass


@books.command("list", help="list books")
def list_books():
    raise NotImplementedError()


@books.command("get")
@click.argument("book_id")
@verbose_flag
@asyncio
async def get_book(book_id: str):
    "get book info"
    service = await get_client(LibraryService)

    print(await service.get_library_document(book_id))


def monitor(books: Resource, volume_id: str) -> None:
    wait = 1.0

    while True:
        state = get_volume(books, volumeId=volume_id)["userInfo"][
            "userUploadedVolumeInfo"
        ]["processingState"]
        print(state)
        if state.startswith("COMPLETED_"):
            break
        time.sleep(wait)
        wait *= 1.5


if __name__ == "__main__":
    main()
