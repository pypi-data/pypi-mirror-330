import logging
import os
import shutil
from ftplib import FTP_TLS as FTP
from ftplib import error_perm
from tempfile import mkdtemp

from menusadp import CONFIG

logger = logging.getLogger("FTP")


def upload_this(ftp, path):
    """credit:
    https://stackoverflow.com/a/27299745/2069099
    """
    files = os.listdir(path)
    os.chdir(path)
    ftp_pwd = ftp.pwd()
    for f in files:
        if os.path.isfile(os.path.join(path, f)):
            logger.info("upload %s->%s/", os.path.join(path, f), ftp_pwd)
            with open(f, "rb") as fh:
                ftp.storbinary("STOR %s" % f, fh)
        elif os.path.isdir(os.path.join(path, f)):
            try:
                ftp.mkd(f)
            except error_perm:
                pass
            ftp.cwd(f)
            upload_this(ftp, os.path.join(path, f))
    ftp.cwd("..")
    os.chdir("..")


def upload(preview=True):
    _prefix = "preview_" if preview else ""
    src_dir = CONFIG["PATHS"][f"{_prefix}output_dir"]
    logger.info(f"uploading from {src_dir}")
    # --------------------------------------------------------------------
    # prepare temporary output dir
    # sources
    carte2file = {"wines": "carte_des_vins.html", "menus": "carte.html"}
    sources = [
        os.path.join(src_dir, "css"),
        os.path.join(src_dir, "fig"),
        os.path.join(src_dir, "index.html"),
        os.path.join(src_dir, carte2file["wines"]),
        os.path.join(src_dir, carte2file["menus"]),
    ]
    wdir = mkdtemp()
    # sp.Popen(shlex_split('/usr/bin/xdg-open "%s"' % wdir))
    for src in sources:
        if os.path.isfile(src):
            shutil.copy2(src, wdir)
        else:
            target = os.path.join(wdir, os.path.split(src)[-1])
            shutil.copytree(src, target)
    # ------------------------------------------------------------------------
    # FTP connection
    url = CONFIG["FTP"]["upload_url"]
    user = CONFIG["FTP"]["upload_username"]
    passwd = CONFIG["FTP"]["upload_password"]
    with FTP(url, user=user, passwd=passwd) as ftp:
        ftp.prot_p()  # switch to secure data connection
        if preview:
            try:
                ftp.mkd("preview")
            except error_perm:
                print("preview exists")
            ftp.cwd("preview")
        logger.warning("### uploading to %s" % ftp.pwd())
        upload_this(ftp, wdir)
    logger.info("----------------------------------------------------------")
    logger.info("upload finished")
    logger.info("----------------------------------------------------------")
