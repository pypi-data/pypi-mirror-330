import hashlib
import os
import shlex
import shutil
from importlib import resources
from subprocess import check_output

import click


def echo_error(txt):
    return click.secho(txt, fg="red")


def echo_warning(txt):
    return click.secho(txt, fg="yellow")


def echo_info(txt):
    return click.secho(txt, fg="blue")


def shlex_split(txt):
    """redefine shlex.split taking care of OS

    >>> shlex_split("ls -la")
    ['ls', '-la']
    """
    return shlex.split(txt, posix=(os.name == "posix"))


def get_binary_info(prog):
    """return path to binary and version

    >>> get_binary_info("pandoc")
    ('...', 'pandoc ...')
    """
    _bin = shutil.which(prog)
    if not _bin:
        _bin = ""
        _ver = ""
    else:
        _ver = check_output(shlex_split("%s --version" % _bin)).decode().split("\n")[0]
    return _bin, _ver


def infos(config, configfile):
    """
    print some infos from config
    """
    print()
    click.secho("Files", bold=True, fg="white", bg="black")
    print("configuration file:", end="")
    echo_info(str(configfile))
    print("configuration dir:", end="")
    echo_info(f"file://{str(configfile.parent)}")
    paths = dict(config["PATHS"].items())
    print("home: ", end="")
    echo_info(f"file://{paths['home_dir']}")
    print("source: ", end="")
    echo_info(f"file://{paths['source_dir']}")
    print("output: ", end="")
    echo_info(f"file://{paths['output_dir']}")
    print()
    click.secho("Binaries", bold=True, fg="white", bg="black")
    for k, v in config["MISC"].items():
        if not k.endswith("_bin"):
            continue
        print(f"{k}:", end="")
        echo_info(v)
    print()
    click.secho("Uploading", bold=True, fg="white", bg="black")
    for k, v in config["FTP"].items():
        print(f"{k}:", end="")
        echo_info(v)
    print()


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def _booleanify(val):
    val = str(val)
    if val.lower()[0] in ("1yYoO"):
        return True
    return False


def _get_src_path(data=None, srcdir=None):
    """
    >>> _get_src_path('b.png')
    PosixPath('.../data/b.png')
    """
    if not srcdir:
        srcdir = resources.files("menusadp.data")
    else:
        # comming from partial
        pass
    if data:
        return srcdir / data
    return srcdir
