from __future__ import annotations

import logging
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

import mistune
from liquid import Environment, FileSystemLoader
from mistune.toc import add_toc_hook
from pygments import highlight
from pygments.formatters import html
from pygments.lexers import get_lexer_by_name
from slugify import slugify

from markupdown.util import resolve_base

from .files import MarkdownFile
from .transform import transform

logger = logging.getLogger(__name__)


class MarkupdownRenderer(mistune.HTMLRenderer):
    def __init__(self, md_file: MarkdownFile, base_dir: Path | str, **kwargs):
        super().__init__(**kwargs)
        self.md_file = md_file
        self.base_dir = Path(base_dir)

    def link(self, text, url, title=None):
        split_url = urlsplit(url)
        if not split_url.scheme:
            path = split_url.path
            path = self.md_file.resolve(self.base_dir, path)
            if path.name.endswith(".md"):
                path = MarkdownFile(self.base_dir / path).url_path(self.base_dir)
            split_url = (
                split_url.scheme,
                split_url.netloc,
                str(path),
                split_url.query,
                split_url.fragment,
            )
            url = urlunsplit(split_url)
        return super().link(text, url, title)

    def block_code(self, code, info=None):
        if info:
            lexer = get_lexer_by_name(info, stripall=True)
            formatter = html.HtmlFormatter(style="colorful")
            return highlight(code, lexer, formatter)
        return "<pre><code>" + mistune.escape(code) + "</code></pre>"


class TocHeadingGenerator:
    def __init__(self) -> None:
        self.heading_crumbs = []

    def __call__(self, token: dict[str, Any], _: int) -> str:
        header_text = token["text"]
        level = token["attrs"]["level"]
        while self.heading_crumbs and level <= self.heading_crumbs[-1][1]:
            self.heading_crumbs.pop()
        header_text = slugify(header_text)
        self.heading_crumbs.append((header_text, level))
        return "_".join(map(lambda x: x[0], self.heading_crumbs))


def render(
    glob_pattern: str,
    site: dict[str, object] = {},
    dest_dir: Path | str | None = None,
    template_dir: str | Path = "templates",
) -> None:
    """
    Render markdown files to HTML using liquid templates.

    For each markdown file:
    - Convert markdown content to HTML
    - Apply liquid template specified in frontmatter (or default.liquid)
    - Write rendered HTML to the same location with .html extension

    Args:
        glob_pattern: The glob pattern of the markdown files to render.
        site: Dictionary of site configuration. Defaults to {}.
        dest_dir: Directory to render to.
            Defaults to the base directory of the glob pattern.
        template_dir: Directory containing liquid templates.
            Defaults to "templates" in current directory.

    Raises:
        FileNotFoundError: If template directory doesn't exist
        ValueError: If no template is specified and no default.liquid exists
    """
    # Initialize Liquid environment
    template_dir = Path(template_dir).absolute()
    base_dir, _ = resolve_base(glob_pattern)

    if not template_dir.is_dir():
        raise FileNotFoundError(f"Template directory not found: {template_dir}")

    env_globals = {
        "base_dir": str(base_dir),
        "site": site,
    }

    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=False,
        globals=env_globals,
    )

    def _or_array(obj: Any) -> list:
        return [] if not obj else obj

    def _frontmatter(
        path: str | Path | list[str | Path],
    ) -> dict[str, object] | list[dict[str, object]]:
        """
        Takes a path relative to the site directory and returns the frontmatter dict.
        """
        if isinstance(path, str) or isinstance(path, Path):
            return MarkdownFile(base_dir / Path(path)).frontmatter()
        elif isinstance(path, list):
            frontmatters = []
            for p in path:
                frontmatters.append(_frontmatter(p))
            return frontmatters

        raise TypeError(f"path must be str, Path, or list, but got {type(path)}")

    def _render_redirects(md_file: MarkdownFile, base_dir: Path) -> None:
        if redirect_froms := md_file.frontmatter().get("redirects_from"):
            template = env.get_template("redirect.liquid")
            html_base_dir = Path(dest_dir) if dest_dir else base_dir
            redirect_to = Path("/") / md_file.url_path(base_dir)
            if isinstance(redirect_froms, str):
                redirect_froms = [redirect_froms]
            assert isinstance(redirect_froms, list)
            for redirect_from in redirect_froms:
                redirect_from = Path(redirect_from)
                if redirect_from.is_absolute():
                    redirect_from = Path(redirect_from).relative_to("/")
                redirect_from = html_base_dir / Path(redirect_from) / "index.html"
                redirect_from.parent.mkdir(parents=True, exist_ok=True)
                with open(redirect_from, "w", encoding="utf-8") as f:
                    f.write(
                        template.render(
                            site=site,
                            page={"redirect_to": redirect_to},
                        )
                    )
                logger.debug(f"Rendered redirect from: {redirect_from.absolute()}")

    env.add_filter("or_array", _or_array)
    env.add_filter("frontmatter", _frontmatter)

    def _render(md_file: MarkdownFile, base_dir: Path) -> None:
        html_base_dir = Path(dest_dir) if dest_dir else base_dir
        subpath = md_file.path.relative_to(base_dir).with_suffix(".html")
        if subpath.name != "index.html":
            subpath = subpath.with_suffix("") / "index.html"
        html_file_path = (html_base_dir / subpath).absolute()
        html_file_path.parent.mkdir(parents=True, exist_ok=True)
        format_markdown = mistune.create_markdown(
            escape=False,
            plugins=[
                "speedup",
                "strikethrough",
                "mark",
                "insert",
                "superscript",
                "subscript",
                "footnotes",
                "table",
                "url",
                "abbr",
                "def_list",
                "math",
                "ruby",
                "task_lists",
                "spoiler",
            ],
            renderer=MarkupdownRenderer(md_file, base_dir, escape=False),
        )
        add_toc_hook(format_markdown, heading_id=TocHeadingGenerator())
        html_content, _ = format_markdown.parse(md_file.content())
        html_content = str(html_content).strip()
        frontmatter = md_file.frontmatter()
        page_template = str(frontmatter.get("template", "default"))

        if not page_template.endswith(".liquid"):
            page_template += ".liquid"

        template = env.get_template(page_template)

        rendered = template.render(
            content=html_content,
            page=frontmatter,
        )

        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        _render_redirects(md_file, base_dir)

        logger.debug(
            f"Rendered {md_file.path.absolute()} to {html_file_path.absolute()}"
        )

    transform(glob_pattern, _render)
