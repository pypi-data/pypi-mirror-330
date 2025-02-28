import logging
import os
import shlex
import shutil
import subprocess as sp
from importlib import resources
from pathlib import Path
from tempfile import mkdtemp

import pandas as pd
import tabulate

from menusadp import COLORS, CONFIG, CONFIGDIR, PANDOC_BIN
from menusadp import _get_src as _get_src_path
from menusadp.utils import shlex_split

logger = logging.getLogger("main")

BIO_LOGO = Path("fig") / "b.png"
TMP_PREFIX = "_adp_menus"
SECTION_RULER_WIDTH = "2pt"
SECTION_RULER_COLOR = "battleshipgrey"
SECTION_RULER = True

# PANDOC_BIN = CONFIG["MISC"]["pandoc_bin"]


def exe(cmd, wd):
    logger.debug(f"\ncd {wd} && {cmd}\n")
    cmd = shlex_split(cmd)
    logger.debug("Popen:")
    logger.debug(f"  * cmd: {cmd}")
    logger.debug(f"  * executable: {cmd[0]}")
    logger.debug(f"  * arguments: {cmd[1:]}")
    logger.debug(f"  * cwd: {wd}")
    child = sp.Popen(cmd, cwd=wd, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)
    output, err = child.communicate()
    rc = child.returncode
    return rc, output, err


def splitall(path):
    path = Path(path)
    return path.parent, path.stem, path.suffix


def _parse_wines(src, wrap):
    fpath, fname, ext = splitall(src)
    target = fpath / (fname + ".md")
    wines = pd.read_excel(src, None)
    df_wines = pd.concat(wines)
    # ========================================================================
    # remove cancelled rows
    cancelled = df_wines[df_wines["Prix"].astype(str).str.contains("!")]
    logger.info("cancel %d entries", len(cancelled))
    df_wines = df_wines[~df_wines["Prix"].astype(str).str.contains("!")]
    # ========================================================================
    df_wines = df_wines.reset_index(level=1, drop=True).set_index(
        pd.Index(range(len(df_wines))), append=True
    )
    df_wines.index.names = ["Origine", None]
    df_wines.reset_index(level=0, inplace=True)
    df_wines.Bio = df_wines.Bio.apply(lambda x: _conv_bool(x))
    df_wines.Cont = df_wines.Cont.fillna("75cl")
    # set Price at the end
    if "Prix" in df_wines.columns:
        df_wines.insert(len(df_wines.columns) - 1, "Prix", df_wines.pop("Prix"))
    if wrap:
        # ------------------------------------------------------------------------
        # "nom" and "apellation" width shouldn't exceed 80 characters
        MAX_TOTAL_WIDTH = 72  # characters
        widths = pd.concat(
            (df_wines["Nom"].str.len(), df_wines["Apellation"].str.len()), axis=1
        )
        widths["Total"] = widths.sum(axis=1)
        _df_KO = df_wines[widths["Total"] > MAX_TOTAL_WIDTH]
        df_wines.loc[:, "Nom"].update(
            _df_KO["Nom"].str.wrap(width=38, subsequent_indent=" ")
        )
        df_wines.loc[:, "Apellation"].update(
            _df_KO["Apellation"].str.wrap(width=38, subsequent_indent=" ")
        )
    return df_wines


def _build_options_menu(title, df, meta, keep_newpages=False):
    txt = title.format(**meta)
    txt += "\n" + len(title) * "-" + "\n"
    txt += '\n<div id="options_menu">\n'
    df = df.dropna(axis=1)
    # txt += '<div id="center">'
    for i, options in df.iterrows():
        options = options.tolist()
        if not keep_newpages:
            # remove user-defined newpages
            options = [o.replace("\n", "") for o in options]

        _opts = "\n\n*ou*\n\n".join(options)
        txt += _opts
        if i + 1 < len(df):
            txt += "\n\n—\n\n"
        else:
            txt += "\n\n"
    # -----------------------------------------------------------
    # add remarks
    rem = meta.get("Remarque")
    if rem:
        txt += build_remarks(rem)
    txt += "\n</div> <!-- /options_menu -->"
    txt += "\n\n"
    return txt


FONT_VARIANTS = {
    "normal": {"html": "normal"},
    "small-caps": {"html": "small-caps"},
}


def tcolor(txt, color):
    """
    >>> tcolor('test', 'adp')
    '<span style="color:#F7AE70">test</span>\\n'
    """
    html_color = COLORS[color]
    _txt = f'<span style="color:{html_color}">'
    _txt += txt
    _txt += "</span>\n"
    return _txt


def _conv_bool(x):
    """
    >>> _conv_bool('y')
    True
    >>> _conv_bool('toto')
    False
    """
    return x in ("1", 1, "y", "O")


def build_remarks(rem, prices=()):
    txt = ""
    remarks = [r.strip() for r in rem.split("\n")]
    # ====================================================================
    # HTML
    # ====================================================================
    txt += '<div id="remarks">'
    if prices:
        # menu Galerie
        for p in prices:
            txt += f"\n{p}\n"
        txt += "\n~\n"
    for remark in remarks:
        txt += f"\n{remark}\n"
    txt += "\n</div> <!-- /remarks -->\n"
    return txt


def _build_galerie(title, df, meta):
    txt = title.format(**meta)
    txt += "\n" + len(title) * "-" + "\n"
    txt += '\n<div id="options_menu">\n'

    prices = df.iloc[0].astype(str).str.replace("€", "", regex=False)

    df = df[1:]
    for i, options in df.iterrows():
        pg, gg = options.tolist()

        if isinstance(pg, str):
            txt += pg
        else:
            txt += tcolor(f"{gg}", "adp")
        if i < len(df):
            txt += "\n\n—\n\n"
        else:
            txt += "\n\n"
    # ------------------------------------------------------------------------
    # prices
    pr = "Petite Galerie {Petite Galerie}€ ".format(**prices.to_dict())
    pr += " | "
    pr += tcolor(
        " Grande Galerie {Grande Galerie}€\n\n".format(**prices.to_dict()), "adp"
    )
    # ------------------------------------------------------------------------
    # suppléments
    sup = meta.get("Suppléments")
    if isinstance(sup, str):
        txt += '<div id="additional">'
        sups = [r.strip() for r in sup.split("\n")]
        for sup in sups:
            txt += f"\n{sup}\n\n"
        txt += "</div>"
    # -----------------------------------------------------------
    # add remarks
    rem = meta.get("Remarque")
    if isinstance(rem, str):
        txt += build_remarks(rem, prices=(pr,))
    txt += "\n</div> <!-- /options_menu -->"
    txt += "\n\n"
    return txt


def _build_carte(title, df, meta):
    txt = title.format(**meta)
    txt += "\n" + len(title) * "-" + "\n"
    txt += '\n<div id="carte_items">\n'
    for i, row in df.iterrows():
        txt += '\n<div id="carte_item">\n'
        txt += row.Description + "\n\n"
        txt += str(row.Prix) + "€\n\n"

        txt += "\n</div> <!-- /carte_item -->"
    # -----------------------------------------------------------
    # add remarks
    rem = meta.get("Remarque")
    if isinstance(rem, str):
        txt += build_remarks(rem)
    txt += "\n</div> <!-- /carte_items -->"
    return txt


def _read_carte_tab(xls, tab, section=None):
    if section:
        df = xls[tab].ffill()
        df = df[df["Section"] == section]
    else:
        df = xls.get(tab)
    if "Prix" in df.columns:
        df.insert(len(df.columns) - 1, "Prix", df.pop("Prix"))
    return df


def do_dump_menus(src, out, index_filename="index.html", A4=False):
    if A4:
        txt = r"""
---
papersize: a4
geometry: "left=2cm,right=2cm,top=2cm,bottom=3cm"
"""
    else:
        txt = r"""
---
geometry: "paperwidth=16.4cm,paperheight=32cm,hscale=0.9,vscale=0.85"
"""
    txt += r"""
index_filename: %s
toc-title: "Menus & Carte"
fontsize: 14pt
mainfontoptions:
- BoldFont=Font-Bold.otf
- ItalicFont=Font-Italic.otf
- BoldItalicFont=Font-BoldItalic.otf
subparagraph: yes
documentclass: extarticle
    """
    txt = txt % index_filename
    # ------------------------------------------------------------------------
    # txt += define_colors()
    txt += "\n---\n\n\n"
    chapters = {
        "Menus": {
            "Déjeuner": (_build_options_menu, "Menu Déjeuner {Prix:.0f}€", ""),
            "Goya": (_build_options_menu, "Menu Goya {Prix:.0f}€", r"\newpage"),
            "Galerie": (_build_galerie, "Menus Galerie", r"\newpage"),
        },
        "À la carte": {
            "Le début de la faim": (_build_carte, "Le début de la faim", ""),
            "Les poissons": (_build_carte, "Les poissons", r"\newpage"),
            "Les viandes": (_build_carte, "Les viandes", ""),
            "La fin de la faim": (
                _build_carte,
                "La fin de la faim",
                r"\newpage",
            ),
        },
    }
    carte = pd.read_excel(src, None)
    metas = carte["MenusMetadata"].set_index("Menu").T.to_dict()
    # ========================================================================
    # menus
    # ========================================================================
    txt += "\n\nMenus\n"
    txt += "=====\n\n"
    for tab, (build, title, sep) in chapters["Menus"].items():
        meta = metas.get(tab, {})
        df = _read_carte_tab(carte, tab)
        txt += build(title, df, meta)
        txt += sep + "\n\n"
    txt += "À la carte\n"
    txt += "==========\n\n"
    tab = "À la carte"
    for section, (build, title, sep) in chapters[tab].items():
        meta = metas.get(section, {})
        df = _read_carte_tab(carte, "À la carte", section=section)
        txt += build(title, df, meta)
        txt += sep + "\n\n"

    if not out:
        return txt
    path, fname, ext = splitall(out)
    target = os.path.join(path, out)
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(txt)
    return target


def bio(x):
    """
    subsitute `Bio` value with the appropriate logo
    >>> bio(None)
    ''
    >>> bio('1')
    '![](fig/b.png)'
    """
    if not x:
        return ""
    return "![](%s)" % BIO_LOGO


def titleize(txt, level=0):
    """
    >>> print(titleize('Hello World', 1))
    Hello World
    -----------
    <BLANKLINE>
    <BLANKLINE>
    """
    chars = "=-"
    return txt + "\n" + chars[level] * len(txt) + "\n\n"


def dress(txt, fix="**", token_id=None):
    """dress-up `txt` with `fix` (prefix and/or suffix):

    >>> dress('Hello\\nWorld', '~', None)
    '~Hello\\nWorld~'
    >>> dress('Hello\\nWorld', '~', -1)
    'Hello\\n~World~'
    """
    txt = str(txt).strip()
    if txt == "nan":
        return ""
    if token_id is None:
        # dress up everything
        return f"{fix}{txt}{fix}"
    # ------------------------------------------------------------------------
    # check tokens
    tokens = txt.split("\n")
    if len(tokens) > token_id:
        tokens[token_id] = fix + tokens[token_id].strip() + fix
    return "\n".join(tokens)


def _prepare_output(tmp_dir, output_dir):
    """
    prepare output tree
    .
    └── <tmp_dir>  (pwd)
        └── out
            ├── fig
            └── html
            └── pdf
    """
    _fig_dir = os.path.join(tmp_dir, "fig")
    os.makedirs(_fig_dir, exist_ok=True)
    shutil.copy2(_get_src_path("b.png"), _fig_dir)
    shutil.copy2(_get_src_path("logo_carre.png"), _fig_dir)

    os.makedirs(os.path.join(tmp_dir, "html"), exist_ok=True)
    os.makedirs(os.path.join(tmp_dir, "pdf"), exist_ok=True)
    _css_dir = os.path.join(tmp_dir, "html", "css")
    _fig_dir = os.path.join(tmp_dir, "html", "fig")
    os.makedirs(_css_dir, exist_ok=True)
    shutil.copy2(_get_src_path("styling.css"), _css_dir)
    shutil.copy2(_get_src_path("default.html"), _css_dir)
    shutil.copy2(_get_src_path("b.png"), _fig_dir)
    # ------------------------------------------------------------------------
    # also copy css and figs to output_dir
    _fig_dir = os.path.join(output_dir, "fig")
    os.makedirs(_fig_dir, exist_ok=True)
    shutil.copy2(_get_src_path("b.png"), _fig_dir)
    shutil.copy2(_get_src_path("logo_carre.png"), _fig_dir)
    _css_dir = os.path.join(output_dir, "css")
    os.makedirs(_css_dir, exist_ok=True)
    shutil.copy2(_get_src_path("styling.css"), _css_dir)
    shutil.copy2(_get_src_path("index.html"), output_dir)


def define_colors():
    """append colors definition to pandoc yaml block"""
    txt = r"- \usepackage{color}" + "\n"
    txt += r"    - \AtBeginDocument{\colorlet{defaultcolor}{.}}"
    txt += "\n"
    # user defined colors
    for color, colord in COLORS.items():
        if color == "defaultcolor":
            continue
        colord = colord.strip("#")
        txt += rf"    - \definecolor{{{color}}}{{HTML}}{{{colord}}}" + "\n"
    return txt


def do_dump_wines(
    src,
    out=None,
    headers=(),
    break_on_chapter=True,
    index_filename="index.html",
    tablefmt="simple",
):
    """create markdown and resources files"""
    txt = r"""
---
index_filename: %s
papersize: a4
geometry: "left=2cm,right=2cm,top=3cm,bottom=3cm"
toc-title: "Carte des Vins"
fontsize: 10pt
mainfont: Font-Regular.otf
mainfontoptions:
- BoldFont=Font-Bold.otf
- ItalicFont=Font-Italic.otf
- BoldItalicFont=Font-BoldItalic.otf
subparagraph: yes
documentclass: article
    """
    txt = txt % index_filename

    txt += "\n---\n"
    current_origin = None
    if tablefmt == "simple":
        dfv = _parse_wines(src, wrap=False)  # should be True
    elif tablefmt == "grid":
        dfv = _parse_wines(src, wrap=False)
    else:
        dfv = _parse_wines(src, wrap=False)
    grps = dfv.groupby(["Origine", "Type"], sort=False)
    for i, ((origin, typ), df) in enumerate(grps):
        df = df.copy()  # avoid SettingwithCopyWarning
        if origin != current_origin:
            txt += "\n"

            if break_on_chapter:
                txt += "\\newpage\n"
            txt += titleize(origin, 0)
            current_origin = origin
        # --------------------------------------------------------------------
        # drop use less columns
        cols_to_drop = ["Origine", "Type"]
        # if no bio at all, drop column
        # if set(df.Bio) == {False}:
        #     cols_to_drop.append("Bio")
        # else:
        #     # subsitute with bio logo
        bio_str = df.Bio.apply(lambda x: bio(x))
        df = df.drop(columns=["Bio"])
        df["Bio"] = bio_str
        # if set(df.Cont) == {""}:
        #     cols_to_drop.append("Cont")
        df = df.drop(columns=cols_to_drop)
        # df = df.dropna(axis=1, how="all")
        if "Année" in df.columns:
            # Année is set to float when NaN are present
            df["Année"] = df["Année"].fillna("0")
            df["Année"] = df["Année"].astype(int).astype("str")
            df["Année"] = df["Année"].replace("0", "")
        # --------------------------------------------------------------------
        # no NaN...
        df = df.fillna("", axis=1)
        txt += titleize(typ, 1)
        # if origin == "Alsace":
        #     breakpoint()
        txt += tabulate.tabulate(
            df, headers=headers, showindex="never", tablefmt=tablefmt
        )

        txt += "\n\n"
    if not out:
        return txt
    path, fname, ext = splitall(out)
    target = os.path.join(path, out)
    with open(target, "w", encoding="utf-8") as fh:
        fh.write(txt)
        return target


def do_convert(mdfile, ext, toc, dest=None, debug=True):
    """convert odt menu to markdown"""
    logger.info(f"{mdfile} → {ext}")
    _args = ", ".join(["%s=%s" % (k, v) for k, v in locals().items()])
    logger.debug(f"convert( {_args} )")
    ext = ext.lstrip(".")
    fpath, fname, _ext = splitall(mdfile)
    fname = fname.strip(".")
    src_dir = os.path.join(fpath, ext)
    if not dest:
        target_dir = os.path.join(fpath, ext)
    else:
        target_dir = dest
    target = os.path.join(target_dir, fname + "." + ext)
    CMD = f"{PANDOC_BIN} --standalone -o {target} {mdfile}"
    # ------------------------------------------------------------------------
    # HTML output
    if ext == "html":
        _tpl = os.path.join(src_dir, "css", "default.html")
        CMD += " --to html5  --template=%s " % _tpl
        if toc:
            CMD += " --toc --toc-depth=1"
    rc, output, err = exe(CMD, wd=fpath)
    if rc != 0:
        logger.critical(f"convert returned code: {rc}")
    return target, rc, output, err


class Worker:
    """wrapper for upper functions"""

    def __init__(self, dest, open_tmp=True):
        # --------------------------------------------------------------------
        # temp working directory
        self.wdir = Path(mkdtemp(prefix=TMP_PREFIX))
        logger.info(f"working in {self.wdir}")
        _prepare_output(self.wdir, dest)
        if open_tmp and os.name == "posix":
            sp.Popen(shlex.split('/usr/bin/xdg-open "%s"' % self.wdir))
        # wines and carte file sources
        self.wines_src = None
        self.menus_src = None
        # wines nad carte markdown file
        self.wines_md = None
        self.menus_md = None
        # --------------------------------------------------------------------
        # output dir
        self.dest = dest
        logger.info(f"output to {self.dest}")

    def load_wines(self, src, break_on_chapter=True):
        self.wines_src = src
        self.wines_md = self.wdir / "carte_des_vins.md"
        do_dump_wines(
            src=self.wines_src,
            out=self.wines_md,
            break_on_chapter=break_on_chapter,
        )
        logger.info(f'"{self.wines_src}" → "{self.wines_md}"')

    def load_menus(self, src):
        self.menus_src = src
        for A4 in (True, False):
            if A4:
                self.menus_A4_md = self.wdir / "carte_A4.md"
                md_filepath = self.menus_A4_md
            else:
                self.menus_md = self.wdir / "carte.md"
                md_filepath = self.menus_md
            do_dump_menus(src=self.menus_src, out=md_filepath, A4=A4)
            logger.info(f'"{self.menus_src}" → "{md_filepath}"')

    def convert(self):
        status = {"wines": "OK", "menus": "OK"}
        toc = True
        for carte in ("wines", "menus", "menus_A4"):
            logger.debug(f"===== [processing {carte}_md] =====")
            carte_md = getattr(self, f"{carte}_md", None)
            if carte_md and carte_md.exists():
                for ext in ("html", "docx"):
                    if "A4" in carte and ext == "html":
                        logger.debug("do not create HTML for A4 carte")
                        continue
                    logger.debug(f"----- [{ext}] ----------")
                    target, rc, output, err = do_convert(
                        carte_md, ext, dest=self.dest, toc=toc
                    )
                    if rc != 0:
                        logger.error(err.decode())
                        status[carte] = False
            else:
                logger.warning(f'no "{carte}" to convert')
                status[carte] = False
        return status


if __name__ == "__main__":
    import doctest

    doctest.testmod(optionflags=doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE)
