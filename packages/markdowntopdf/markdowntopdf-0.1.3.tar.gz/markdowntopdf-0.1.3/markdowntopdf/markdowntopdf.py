# Based on https://gist.github.com/engineervix/2385a54a4019b3f4526e
import argparse
import markdown2
from importlib import resources
from pathlib import Path
from weasyprint import CSS, HTML


MARKDOWN2_EXTRAS = [
    "cuddled-lists",
    "fenced-code-blocks",
    "footnotes",
    "pyshell",
    "tables",
]


def get_styles(anchor):
    return {
        resource.name.removesuffix(".css"): resource
        for resource in resources.files(anchor).iterdir()
        if resource.is_file() and resource.name.endswith(".css")
    }


CODE_STYLES = get_styles("markdowntopdf.pygments-css")
MAIN_CSS = get_styles("markdowntopdf.css")


def default_template(body):
    return f"""<html>
<head>
</head>
<body>
{body}
</body>
</html>
"""


def html2pdf(html, styles, output):
    HTML(string=html).write_pdf(
        output,
        stylesheets=[CSS(string=css) for css in styles],
        presentational_hints=True,
    )


def md2html(md, extras=None, template_fn=None):
    if template_fn is None:
        template_fn = default_template
    return template_fn(markdown2.markdown(md, extras=extras))


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=Path, help="Markdown file to convert to PDF")
    return parser.parse_args(args)


def main(args):
    mddocument = parse_args(args).input_file
    mdtext = mddocument.read_text()

    styles = [CODE_STYLES["default"].read_text(), MAIN_CSS["default"].read_text()]

    # Add text wrap to pre blocks inside highlighted boxes
    styles.append(".codehilite pre { white-space: pre-wrap; }")
    styles.append(".codehilite pre { padding: 1em; }")

    mdhtml = md2html(mdtext, MARKDOWN2_EXTRAS)

    html2pdf(mdhtml, styles, mddocument.with_suffix(".pdf"))


def run():
    import sys

    exit(main(sys.argv[1:]))


if __name__ == "__main__":
    run()
