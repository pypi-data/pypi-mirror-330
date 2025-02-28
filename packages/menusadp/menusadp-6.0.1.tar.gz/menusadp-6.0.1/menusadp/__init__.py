# -*- coding: utf-8 -*-

"""Top-level package for menusADP."""
import getpass
import logging
import shutil
from configparser import ConfigParser, ExtendedInterpolation
from functools import partial
from importlib import resources
from logging.handlers import TimedRotatingFileHandler
from os.path import join as pjoin
from pathlib import Path

from appdirs import AppDirs

from menusadp.utils import (
    _get_src_path,
    echo_info,
    echo_warning,
    get_binary_info,
    infos,
)

__version__ = "6.0.1"
__appname__ = "menusadp"


CONFIG_VERSION = "3.0"

PANDOC_BIN, PANDOC_VERSION = get_binary_info("pandoc")
PDFLATEX_BIN, PDFLATEX_VERSION = get_binary_info("pdflatex")

user = getpass.getuser()
dirs = AppDirs(__appname__, user)
userdir = Path(dirs.user_data_dir)
CONFIGDIR = Path(dirs.user_config_dir)
CONFIGFILE = CONFIGDIR / "config.ini"

DEFAULT_CONFIG = dict(
    MISC={
        "config_version": CONFIG_VERSION,
        "pandoc_bin": PANDOC_BIN,
        "pdflatex_bin": PDFLATEX_BIN,
        "index_filename": "index.html",
    },
    PATHS={
        "home_dir": str(userdir),
        "default": CONFIGDIR / "static",
        "source_dir": pjoin("${home_dir}", "source"),
        "output_dir": pjoin("${home_dir}", "out"),
        "preview_output_dir": pjoin("${home_dir}", "out_preview"),
        "last_valid_data_dir": pjoin("${home_dir}", "last_valids"),
    },
    FILES={"wines_file": "vins.xlsx", "menus_file": "menus.xlsx"},
    LOGGING={
        "log_file": pjoin("${PATHS:home_dir}", "menusadp.log"),
        "console_log_level": "INFO",
        "file_log_level": "DEBUG",
    },
    FTP={
        "upload_url": "",
        "upload_username": "",
        "upload_password": "",
    },
    LAST_VALIDS={"wines": "", "menus": ""},
    LAST_VALIDS_PREVIEW={"wines": "", "menus": ""},
    ASK_MODE={
        "ask_for_prod": "1",
        "default_prod": "1",
        "ask_for_upload": "0",
        "default_upload": "1",
        "ask_for_force": "0",
        "default_force": "0",
    },
    COLORS={
        "defaultcolor": "#000000",
        "adp": "#F7AE70",
        "battleshipgrey": "#848482",
        "darkblue": "#000080",
        "darkgray": "#A9A9A9",
    },
)


def create_config_file():
    """create (overwrite if existing) configuration file,
    and return a `config` object
    """
    CONFIGDIR.mkdir(parents=True, exist_ok=True)
    config = ConfigParser(interpolation=ExtendedInterpolation(), allow_no_value=True)
    for chapter, content in DEFAULT_CONFIG.items():
        config[chapter] = content
    with open(CONFIGFILE, "w") as fh:
        config.write(fh)
        echo_warning('created config file "%s"' % CONFIGFILE)
    return config


def first_start():
    config = create_config_file()
    for _, path in config["PATHS"].items():
        Path(path).expanduser().mkdir(exist_ok=True, parents=True)
    # -------------------------------------------------------------------------
    # copy templates and default stuff
    for src in _get_src_path().glob("*"):
        if not src.is_file() or src.stem == "__init__":
            continue
        shutil.copy(src, config["PATHS"]["default"])
    return config


# ============================================================================
# manage configuration
# ============================================================================

if CONFIGFILE.exists():
    CONFIGDIR.mkdir(parents=True, exist_ok=True)
    # ------------------------------------------------------------------------
    # read existing config
    CONFIG = ConfigParser(interpolation=ExtendedInterpolation(), allow_no_value=True)
    CONFIG.read(CONFIGFILE)
    if float(CONFIG["MISC"].get("config_version", 0.0)) < float(CONFIG_VERSION):
        CONFIG = create_config_file()
else:
    # ------------------------------------------------------------------------
    # first start, create config and required folders
    CONFIG = first_start()

# =============================================================================
# override _get_src_path
# =============================================================================
_get_src = partial(_get_src_path, srcdir=CONFIGDIR / "static")


COLORS = dict(CONFIG["COLORS"].items())
PANDOC_BIN = CONFIG["MISC"]["pandoc_bin"]
PANDOC_VERSION = get_binary_info(PANDOC_BIN)

# ============================================================================
# create `logger`
# ============================================================================
logger = logging.getLogger("init")
logger.propagate = False
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
log_file = Path(CONFIG["LOGGING"]["log_file"])
log_dir = log_file.parent
if not log_dir.exists():
    log_dir.mkdir(parents=True)
print(f'check logs in "{log_file}"')
# fh = logging.FileHandler(log_file)
# -----------------------------------------------------------------------------
# file handler
fh = TimedRotatingFileHandler(log_file, when="W0", backupCount=2, encoding="utf-8")
fh_level = CONFIG["LOGGING"]["file_log_level"]
fh.setLevel(getattr(logging, fh_level))
# create console handler with a higher log level
ch = logging.StreamHandler()
ch_level = CONFIG["LOGGING"]["console_log_level"]
ch.setLevel(getattr(logging, ch_level))
# create formatter and add it to the handlers
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d,%H:%M:%S"
)
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)
# ----------------------------------------------------------------------------
# begin logging
logger.debug("\n")
logger.debug("================================")
logger.debug(f" # manusadp version {__version__}")
logger.debug(" # logger initialized")
logger.debug(f" # config file: {CONFIGFILE}")
logger.debug(f" # pandoc bin: {PANDOC_BIN}")
logger.debug(f" # pdflatex bin: {PDFLATEX_BIN}")

if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
    infos(CONFIG, CONFIGFILE=CONFIGFILE)
