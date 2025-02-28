import logging

from menusadp.upload import upload as do_upload

logger = logging.getLogger("cli")
import os
import shutil
from pathlib import Path

import click

from menusadp import (
    CONFIG,
    CONFIGFILE,
    PANDOC_BIN,
    PANDOC_VERSION,
    PDFLATEX_BIN,
    PDFLATEX_VERSION,
    __version__,
    create_config_file,
    infos,
)
from menusadp.main import Worker
from menusadp.utils import md5


@click.group
def cli():
    pass


@cli.command
def about():
    """misc. informations"""
    click.secho(f"menusadp version {__version__}", bold=True, fg="white", bg="black")
    click.secho(f"Pandoc version {PANDOC_VERSION}", bold=True, fg="white", bg="black")
    click.secho(f"Latex version {PDFLATEX_VERSION}", bold=True, fg="white", bg="black")
    infos(CONFIG, CONFIGFILE)


@cli.command
def check():
    """perform sanity checks and exit"""
    msg = ""
    msg += "Pandoc: %s (%s - %s) \n" % (
        os.path.isfile(PANDOC_BIN),
        PANDOC_BIN,
        PANDOC_VERSION,
    )
    msg += "pdflatex: %s (%s -%s)" % (
        os.path.isfile(PDFLATEX_BIN),
        PDFLATEX_BIN,
        PDFLATEX_VERSION,
    )
    print(msg)


@cli.command
def edit_config():
    """open configuration file for editing"""
    if os.getenv("EDITOR"):
        os.system("%s %s" % (os.getenv("EDITOR"), CONFIGFILE))
    else:
        # assume windows
        os.system(CONFIGFILE)


@cli.command
@click.option("-p", "--prod", is_flag=True, default=False, help="work on production")
@click.option(
    "-f", "--force", is_flag=True, default=False, help="force convert even if MD5 match"
)
@click.option("-u", "--upload", is_flag=True, default=False, help="upload HTML")
def convert(prod, force, upload):
    if prod:
        click.secho("working on production", fg="red")
        output_dir = Path(CONFIG["PATHS"]["output_dir"])
        valid_key = "LAST_VALIDS"
    else:
        output_dir = Path(CONFIG["PATHS"]["preview_output_dir"])
        valid_key = "LAST_VALIDS_PREVIEW"
    input_dir = Path(CONFIG["PATHS"]["source_dir"])
    click.secho(f"{input_dir=}")
    wfile = input_dir / "vins.xlsx"
    mfile = input_dir / "menus.xlsx"
    for src in (wfile, mfile):
        if src.exists():
            logger.debug(f'  working with "{src}"')
        else:
            msg = f'  can not find "{src}"'
            logger.error(msg)
            raise ValueError(msg)
    # ========================================================================
    # is there something to convert?
    # ========================================================================
    current_md5 = {"wines": md5(wfile), "menus": md5(mfile)}
    to_process = []
    for carte, act_md5 in current_md5.items():
        if force or CONFIG[valid_key][carte] != current_md5[carte]:
            to_process.append(carte)
    for carte in to_process:
        logger.warning(f"need to process {carte}")
    if not to_process:
        logger.info("----------------------------------------------------------")
        logger.info("nothing new, skip conversion")
        logger.info("----------------------------------------------------------")
        return
    # ========================================================================
    # create worker
    # ========================================================================
    worker = Worker(dest=output_dir)
    # ========================================================================
    # load and dump markdonw for required files
    # ========================================================================
    if "wines" in to_process:
        try:
            worker.load_wines(wfile)
        except Exception as exc:
            logger.exception(exc)
            logger.error(f"couldn`t load {wfile}")
            to_process.pop(to_process.index("wines"))
    if "menus" in to_process:
        try:
            worker.load_menus(mfile)
        except Exception as exc:
            logger.exception(exc)
            logger.error(f"couldn`t load {mfile}")
            to_process.pop(to_process.index("menus"))
    # ========================================================================
    # conversion
    # ========================================================================
    if to_process:
        to_process = worker.convert()  # {"wines": "OK", "menus": "OK"}
        if set(to_process.values()) == {False}:
            logger.info("----------------------------------------------------------")
            logger.info("nothing to process, skip conversion")
            logger.info("----------------------------------------------------------")
            return
    # ========================================================================
    # update md5stuff for PROD
    # ========================================================================
    if to_process["wines"]:
        shutil.copy2(wfile, CONFIG["PATHS"]["last_valid_data_dir"])
        CONFIG[valid_key]["wines"] = current_md5["wines"]
        logger.info(f"updated MD5 for wines: {current_md5['wines']}")
    if to_process["menus"]:
        shutil.copy2(mfile, CONFIG["PATHS"]["last_valid_data_dir"])
        CONFIG[valid_key]["menus"] = current_md5["menus"]
        logger.info(f"updated MD5 menus: {current_md5['menus']}")
    # -------------------------------------------------------------------------
    # update config file
    with open(CONFIGFILE, "w") as fh:
        CONFIG.write(fh)
    logger.info("----------------------------------------------------------")
    logger.info("conversion finished. check %s", output_dir)
    logger.info("----------------------------------------------------------")
    # ========================================================================
    # FTP upload
    # ========================================================================
    if not upload:
        return
    is_ok = True
    settings = dict(CONFIG["FTP"].items())
    for k, v in settings.items():
        if not v:
            logger.warning(f"FTP.{k} is blank")
            is_ok = False
    if not is_ok:
        logger.error("Please fill FTP section")
        return
    do_upload(preview=not prod)


@cli.command
@click.option("-p", "--prod", is_flag=True, default=False, help="work on production")
def upload(prod):
    is_ok = True
    settings = dict(CONFIG["FTP"].items())
    for k, v in settings.items():
        if not v:
            logger.warning(f"FTP.{k} is blank")
            is_ok = False
    if not is_ok:
        logger.error("Please fill FTP section")
        return
    do_upload(preview=not prod)
