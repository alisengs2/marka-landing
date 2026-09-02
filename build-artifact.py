#!/usr/bin/env python3
"""Generate the artifact bodies from the source pages.

index.html and about.html are the source of truth. Claude Artifacts wrap published
pages in their own <!doctype>/<head>/<body> and cannot load a local stylesheet, so
this strips the document skeleton, inlines styles.css, and rewrites the links
between pages to their published artifact URLs. Output lands in dist/.
"""
import base64
import mimetypes
import pathlib
import re

root = pathlib.Path(__file__).parent
PAGES = {"index.html": "artifact.html", "about.html": "about.html",
         "venue.html": "venue.html", "speakers.html": "speakers.html",
         "stepevi.html": "stepevi.html"}

# Published artifact URL for each source page; blank until the page has a URL.
ARTIFACT_URLS = {
    "index.html": "https://claude.ai/code/artifact/f086262d-3852-4be1-a791-7b11119a6f01",
    "about.html": "https://claude.ai/code/artifact/b29117f5-a500-4ea3-b1a7-145858d50401",
    "venue.html": "",
    "speakers.html": "",
    "stepevi.html": "",
}

shared_css = (root / "styles.css").read_text(encoding="utf-8")
out = root / "dist"
out.mkdir(exist_ok=True)

for src, dest in PAGES.items():
    page = (root / src).read_text(encoding="utf-8")
    head = re.search(r"<head>(.*?)</head>", page, re.S).group(1)
    body = re.search(r"<body>(.*?)</body>", page, re.S).group(1)

    # The host provides charset, viewport and a base reset; <title>, fonts and styles stay.
    head = re.sub(r'\s*<meta (charset|name="viewport"|name="description")[^>]*>', "", head)
    head = head.replace('<link rel="stylesheet" href="styles.css">',
                        "<style>\n" + shared_css.strip() + "\n</style>")

    doc = head.strip() + "\n\n" + body.strip() + "\n"

    # Artifacts cannot load local files, so images ship inside the page.
    def inline_image(match):
        path = root / match.group(1)
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        return 'src="data:%s;base64,%s"' % (mime, data)

    doc = re.sub(r'src="(assets/[^"]+)"', inline_image, doc)
    for page_name, url in ARTIFACT_URLS.items():
        if url:
            doc = doc.replace('href="%s#' % page_name, '%s#' % url.join(['href="', '']))
            doc = doc.replace('href="%s"' % page_name, 'href="%s"' % url)

    (out / dest).write_text(doc, encoding="utf-8")
    print("wrote dist/%s" % dest)
