#!/usr/bin/env python3
"""
Static site generator to replace Hugo.
Parses markdown files with YAML front matter and generates HTML pages, RSS feeds, and sitemap.
"""

import re
import shutil
import yaml
import markdown
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from xml.etree.ElementTree import Element, SubElement, tostring
from html import escape


# Template loader
class TemplateLoader:
    """Load and cache HTML templates"""
    _cache = {}

    @classmethod
    def load(cls, template_name):
        """Load a template file"""
        if template_name not in cls._cache:
            template_path = Path('templates') / template_name
            with open(template_path, 'r', encoding='utf-8') as f:
                cls._cache[template_name] = f.read()
        return cls._cache[template_name]


class Config:
    """Parse and hold configuration from config.toml"""

    def __init__(self, config_path='config.toml'):
        self.base_url = ""
        self.title = ""
        self.language = "en"
        self.author = ""
        self.description = ""
        self.keywords = ""
        self.navbar = ""
        self.info = ""
        self.avatar_url = ""
        self.favicon_svg = ""
        self.favicon_32 = ""
        self.since = 2023
        self.menu_items = []
        self.color_scheme = "auto"

        self._parse_toml(config_path)

    def _parse_toml(self, path):
        """Simple TOML parser for our specific config format"""
        with open(path, 'r') as f:
            content = f.read()

        # Parse basic settings
        self.base_url = self._extract_value(content, 'baseurl')
        self.title = self._extract_value(content, 'title')
        self.language = self._extract_value(content, 'languagecode', 'en')

        # Parse params section
        params_match = re.search(r'\[params\](.*?)(?=\n\[|\n\[\[|$)', content, re.DOTALL)
        if params_match:
            params = params_match.group(1)
            self.navbar = self._extract_value(params, 'navbar')
            self.author = self._extract_value(params, 'author')
            self.info = self._extract_multiline_value(params, 'info')
            self.description = self._extract_value(params, 'description')
            self.keywords = self._extract_value(params, 'keywords')
            self.avatar_url = self._extract_value(params, 'avatarurl')
            self.favicon_svg = self._extract_value(params, 'faviconSVG')
            self.favicon_32 = self._extract_value(params, 'favicon_32')
            self.color_scheme = self._extract_value(params, 'colorScheme', 'auto')
            since = self._extract_value(params, 'since')
            if since:
                self.since = int(since)

        # Parse menu items
        menu_pattern = r'\[\[menu\.main\]\]\s*name = "([^"]+)"\s*weight = (\d+)\s*url\s*=\s*"([^"]+)"'
        for match in re.finditer(menu_pattern, content):
            self.menu_items.append({
                'name': match.group(1),
                'weight': int(match.group(2)),
                'url': match.group(3)
            })
        self.menu_items.sort(key=lambda x: x['weight'])

    def _extract_value(self, text, key, default=''):
        """Extract a quoted value from TOML"""
        pattern = rf'{key}\s*=\s*"([^"]*)"'
        match = re.search(pattern, text)
        return match.group(1) if match else default

    def _extract_multiline_value(self, text, key):
        """Extract a multiline quoted value from TOML"""
        pattern = rf'{key}\s*=\s*"""(.*?)"""'
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1).strip() if match else ''


class ContentFile:
    """Represents a markdown content file"""

    def __init__(self, path, base_dir='content'):
        self.path = Path(path)
        self.base_dir = Path(base_dir)
        self.front_matter = {}
        self.content = ''
        self.html_content = ''
        self.section = self._determine_section()
        self.url = self._generate_url()

        self._parse()

    def _determine_section(self):
        """Determine the section from the file path"""
        relative = self.path.relative_to(self.base_dir)
        parts = relative.parts
        if len(parts) > 1:
            return parts[0]
        return ''

    def _generate_url(self):
        """Generate the URL path for this content"""
        stem = self.path.stem
        if self.section:
            return f"/{self.section}/{stem}/"
        return f"/{stem}/"

    def _parse(self):
        """Parse the markdown file and extract front matter"""
        with open(self.path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML front matter
        pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)', re.DOTALL)
        match = pattern.match(content)

        if match:
            self.front_matter = yaml.safe_load(match.group(1)) or {}
            self.content = match.group(2)
        else:
            self.content = content

    def render(self):
        """Render markdown content to HTML"""
        # First process shortcodes
        processed = ShortcodeProcessor.process(self.content)

        # Then render markdown
        md = markdown.Markdown(extensions=[
            'fenced_code',
            'tables',
            'nl2br',
            'codehilite'
        ])
        self.html_content = md.convert(processed)

    @property
    def title(self):
        return self.front_matter.get('title', '')

    @property
    def date(self):
        d = self.front_matter.get('date')
        if isinstance(d, datetime):
            return d
        if d:
            # Handle both date and datetime objects from YAML
            try:
                if isinstance(d, str):
                    return datetime.fromisoformat(str(d))
                else:
                    # YAML date object - convert to datetime
                    return datetime.combine(d, datetime.min.time())
            except:
                pass
        return datetime.now()

    @property
    def description(self):
        return self.front_matter.get('description', '')

    @property
    def featured_image(self):
        return self.front_matter.get('featuredImage', '')

    @property
    def series(self):
        s = self.front_matter.get('series', [])
        return s if isinstance(s, list) else [s] if s else []

    @property
    def external_link(self):
        return self.front_matter.get('externalLink', '')

    @property
    def aliases(self):
        a = self.front_matter.get('aliases', [])
        return a if isinstance(a, list) else [a] if a else []


class ShortcodeProcessor:
    """Process Hugo shortcodes and convert them to HTML"""

    # Pattern to match Hugo shortcodes
    SHORTCODE_PATTERN = re.compile(
        r'{{<\s*(\w+)\s*(.*?)\s*>}}(.*?){{<\s*/\1\s*>}}',
        re.DOTALL
    )

    # Pattern for self-closing shortcodes
    SELF_CLOSING_PATTERN = re.compile(
        r'{{<\s*(\w+)\s*(.*?)\s*>}}',
        re.DOTALL
    )

    @classmethod
    def process(cls, content):
        """Process all shortcodes in content"""
        # First process paired shortcodes
        content = cls.SHORTCODE_PATTERN.sub(cls._replace_shortcode, content)
        # Then process self-closing ones
        content = cls.SELF_CLOSING_PATTERN.sub(cls._replace_self_closing, content)
        return content

    @classmethod
    def _replace_shortcode(cls, match):
        """Replace a matched shortcode with HTML"""
        name = match.group(1)
        args = match.group(2)
        inner = match.group(3)

        if name == 'notice':
            return cls._notice(args, inner)
        elif name == 'tabgroup':
            return cls._tabgroup(inner)
        elif name == 'tab':
            return cls._tab(args, inner)
        elif name == 'mermaid':
            return cls._mermaid(inner)
        elif name == 'raw':
            return inner

        return match.group(0)  # Return unchanged if unknown

    @classmethod
    def _replace_self_closing(cls, match):
        """Replace self-closing shortcodes"""
        name = match.group(1)
        args = match.group(2)

        if name == 'video':
            return cls._video(args)
        elif name == 'audio':
            return cls._audio(args)
        elif name == 'googledriveVideo':
            return cls._googledrive_video(args)

        return match.group(0)

    @classmethod
    def _parse_args(cls, args_str):
        """Parse shortcode arguments"""
        params = {}
        # Match key="value" or key=value
        for match in re.finditer(r'(\w+)=(?:"([^"]*)"|(\S+))', args_str):
            key = match.group(1)
            value = match.group(2) or match.group(3)
            params[key] = value
        # Also get positional arguments
        positional = re.findall(r'"([^"]+)"|\b(\w+)\b', args_str)
        positional = [p[0] or p[1] for p in positional if p[0] or p[1]]
        return params, positional

    @classmethod
    def _notice(cls, args, content):
        """Generate HTML for notice shortcode"""
        _, positional = cls._parse_args(args)
        notice_type = positional[0] if positional else 'note'
        return f'<div class="notice {notice_type}"><div class="notice-content">{content}</div></div>'

    @classmethod
    def _video(cls, args):
        """Generate HTML for video shortcode"""
        params, _ = cls._parse_args(args)
        url = params.get('url', '')
        width = params.get('width', '100%')
        height = params.get('height', '100%')
        return f'''<div style="display: flex; align-content: center;">
  <video style="margin:auto;" width="{width}" height="{height}" controls>
    <source src="{url}" type="video/mp4">
  </video>
</div>'''

    @classmethod
    def _audio(cls, args):
        """Generate HTML for audio shortcode"""
        params, _ = cls._parse_args(args)
        audio_file = params.get('audioFile', '')
        return f'<audio controls><source src="{audio_file}" type="audio/mpeg"></audio>'

    @classmethod
    def _tabgroup(cls, content):
        """Generate HTML for tabgroup shortcode"""
        return f'<div class="tabgroup">{content}</div>'

    @classmethod
    def _tab(cls, args, content):
        """Generate HTML for tab shortcode"""
        params, _ = cls._parse_args(args)
        name = params.get('name', 'Tab')
        return f'<div class="tab" data-name="{name}">{content}</div>'

    @classmethod
    def _mermaid(cls, content):
        """Generate HTML for mermaid shortcode"""
        return f'<div class="mermaid">{content}</div>'

    @classmethod
    def _googledrive_video(cls, args):
        """Generate HTML for googledriveVideo shortcode"""
        params, _ = cls._parse_args(args)
        url = params.get('url', '')
        return f'<iframe src="{url}" width="640" height="480" allow="autoplay"></iframe>'


def base_template(content, title, config, meta_tags='', has_mermaid=False):
    """Generate the base HTML template"""
    mermaid_script = '''
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js" crossorigin="anonymous"></script>
  <script>
    mermaid.initialize({ startOnLoad: true });
  </script>''' if has_mermaid else ''

    template = TemplateLoader.load('base.html')
    return template.format(
        language=config.language,
        title=title,
        site_title=config.title,
        author=config.author,
        description=config.description,
        keywords=config.keywords,
        meta_tags=meta_tags,
        base_url=config.base_url,
        favicon_svg=config.favicon_svg,
        favicon_32=config.favicon_32,
        color_scheme=config.color_scheme,
        header=header_partial(config),
        content=content,
        footer=footer_partial(config),
        mermaid_script=mermaid_script
    )


def header_partial(config):
    """Generate navigation header"""
    menu_html = '\n'.join([
        f'            <li class="navigation-item">\n              <a class="navigation-link" style="height: 30px;" href="/{item["url"]}">{item["name"]}</a>\n            </li>'
        for item in config.menu_items
    ])

    template = TemplateLoader.load('header.html')
    return template.format(
        navbar=config.navbar,
        menu_items=menu_html
    )


def footer_partial(config):
    """Generate footer"""
    year = datetime.now().year
    since_text = f'{config.since} -' if config.since < year else ''

    template = TemplateLoader.load('footer.html')
    return template.format(
        since_text=since_text,
        year=year
    )


def post_template(page, config):
    """Generate template for a post page"""
    featured_image = f'<img style="width:100%;" src="{page.featured_image}" alt="Featured image"/>' if page.featured_image else ''

    meta_tags = ''
    if page.featured_image:
        meta_tags = f'''<meta name="image" content="{page.featured_image}">
  <meta name="og:image" content="{page.featured_image}">
  <meta name="twitter:image" content="{config.base_url}{page.featured_image}">'''

    template = TemplateLoader.load('post.html')
    content_html = template.format(
        url=page.url,
        title=escape(page.title),
        description=escape(page.description),
        datetime=page.date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        date_formatted=page.date.strftime('%B %d, %Y'),
        featured_image=featured_image,
        html_content=page.html_content
    )

    has_mermaid = '{{< mermaid' in page.content or '<div class="mermaid">' in page.html_content
    return base_template(content_html, page.title, config, meta_tags, has_mermaid)


def list_template(section, pages, config):
    """Generate template for section list pages"""
    items_html = '\n'.join([
        f'''    <li>
      <span class="date">{p.date.strftime('%B %d, %Y')}</span>
      <a class="title" href="{p.url}">{escape(p.title)}</a>
    </li>'''
        for p in sorted(pages, key=lambda x: x.date, reverse=True)
    ])

    template = TemplateLoader.load('list.html')
    content_html = template.format(
        section_title=section.capitalize(),
        items=items_html
    )

    return base_template(content_html, section.capitalize(), config)


def home_template(config, recent_posts):
    """Generate homepage template"""
    recent_html = '\n'.join([
        f'''    <li>
      <span class="date">{p.date.strftime('%B %d, %Y')}</span>
      <a class="title" href="{p.url}">{escape(p.title)}</a>
    </li>'''
        for p in recent_posts[:5]
    ])

    # Load social links template
    social_links = TemplateLoader.load('social-links.html')

    template = TemplateLoader.load('home.html')
    content_html = template.format(
        avatar_url=config.avatar_url,
        description=config.description,
        social_links=social_links,
        recent_posts=recent_html
    )

    return base_template(content_html, config.title, config)


def series_template(series_name, pages, config):
    """Generate template for series pages"""
    items_html = '\n'.join([
        f'''    <li>
      <span class="date">{p.date.strftime('%B %d, %Y')}</span>
      <a class="title" href="{p.url}">{escape(p.title)}</a>
    </li>'''
        for p in sorted(pages, key=lambda x: x.date)
    ])

    template = TemplateLoader.load('series.html')
    content_html = template.format(
        series_name=series_name,
        items=items_html
    )

    return base_template(content_html, f'Series: {series_name}', config)


class RSSGenerator:
    """Generate RSS feeds"""

    @staticmethod
    def generate(pages, config, output_path, section_name=''):
        """Generate an RSS feed"""
        rss = Element('rss', version='2.0')
        rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')

        channel = SubElement(rss, 'channel')

        # Channel metadata
        if section_name:
            title_text = f'{section_name.capitalize()} on {config.title}'
            desc_text = f'Recent content in {section_name} on {config.title}'
            link_text = f'{config.base_url}/{section_name}/'
        else:
            title_text = config.title
            desc_text = f'Recent content on {config.title}'
            link_text = config.base_url + '/'

        SubElement(channel, 'title').text = title_text
        SubElement(channel, 'link').text = link_text
        SubElement(channel, 'description').text = desc_text
        SubElement(channel, 'generator').text = 'Python Static Site Generator'
        SubElement(channel, 'language').text = config.language

        if pages:
            latest_date = max(p.date for p in pages)
            SubElement(channel, 'lastBuildDate').text = latest_date.strftime('%a, %d %b %Y %H:%M:%S %z')

        # Add items
        for page in sorted(pages, key=lambda x: x.date, reverse=True)[:20]:
            item = SubElement(channel, 'item')
            SubElement(item, 'title').text = page.title
            SubElement(item, 'link').text = config.base_url + page.url
            SubElement(item, 'pubDate').text = page.date.strftime('%a, %d %b %Y %H:%M:%S +0000')
            SubElement(item, 'guid').text = config.base_url + page.url
            SubElement(item, 'description').text = page.html_content

        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
            f.write(tostring(rss, encoding='utf-8'))


class SitemapGenerator:
    """Generate sitemap.xml"""

    @staticmethod
    def generate(pages, config, output_path):
        """Generate sitemap"""
        urlset = Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')

        # Add homepage
        url = SubElement(urlset, 'url')
        SubElement(url, 'loc').text = config.base_url + '/'
        SubElement(url, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')

        # Add all pages
        for page in pages:
            url = SubElement(urlset, 'url')
            SubElement(url, 'loc').text = config.base_url + page.url
            SubElement(url, 'lastmod').text = page.date.strftime('%Y-%m-%d')

        # Write to file
        with open(output_path, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
            f.write(tostring(urlset, encoding='utf-8'))


class Builder:
    """Main builder class that orchestrates the build process"""

    def __init__(self, config_path='config.toml'):
        self.config = Config(config_path)
        self.pages = []
        self.public_dir = Path('public')

    def collect_content(self):
        """Collect all markdown files from content directory"""
        content_dir = Path('content')
        for md_file in content_dir.rglob('*.md'):
            page = ContentFile(md_file)
            self.pages.append(page)

        print(f'Collected {len(self.pages)} content files')
        return self.pages

    def render_content(self):
        """Render all markdown content to HTML"""
        for page in self.pages:
            page.render()
        print(f'Rendered {len(self.pages)} pages')

    def generate_pages(self):
        """Generate all HTML pages"""
        # Group pages by section
        by_section = defaultdict(list)
        for page in self.pages:
            if page.section:
                by_section[page.section].append(page)

        # Generate individual pages
        for page in self.pages:
            if page.section:
                html = post_template(page, self.config)
            else:
                html = post_template(page, self.config)

            # Write to public directory
            output_path = self.public_dir / page.url.strip('/') / 'index.html'
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding='utf-8')

            # Handle aliases
            for alias in page.aliases:
                alias_path = self.public_dir / alias.strip('/') / 'index.html'
                alias_path.parent.mkdir(parents=True, exist_ok=True)
                alias_path.write_text(html, encoding='utf-8')

        # Generate section list pages
        for section, section_pages in by_section.items():
            html = list_template(section, section_pages, self.config)
            output_path = self.public_dir / section / 'index.html'
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding='utf-8')

        # Generate homepage
        all_posts = [p for p in self.pages if p.section in ['posts', 'demos', 'talks']]
        all_posts.sort(key=lambda x: x.date, reverse=True)
        homepage_html = home_template(self.config, all_posts)
        (self.public_dir / 'index.html').write_text(homepage_html, encoding='utf-8')

        # Generate series pages
        by_series = defaultdict(list)
        for page in self.pages:
            for series in page.series:
                by_series[series].append(page)

        for series_name, series_pages in by_series.items():
            slug = series_name.lower().replace(' ', '-')
            html = series_template(series_name, series_pages, self.config)
            output_path = self.public_dir / 'series' / slug / 'index.html'
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding='utf-8')

        print(f'Generated {len(self.pages)} pages, {len(by_section)} section lists, homepage, and {len(by_series)} series pages')

    def generate_feeds(self):
        """Generate RSS feeds"""
        # Main feed
        all_pages = [p for p in self.pages if p.section in ['posts', 'talks', 'demos', 'projects', 'publications']]
        RSSGenerator.generate(all_pages, self.config, self.public_dir / 'index.xml')

        # Section feeds
        by_section = defaultdict(list)
        for page in self.pages:
            if page.section:
                by_section[page.section].append(page)

        for section, pages in by_section.items():
            RSSGenerator.generate(pages, self.config, self.public_dir / section / 'index.xml', section)

        print(f'Generated main RSS feed and {len(by_section)} section feeds')

    def generate_sitemap(self):
        """Generate sitemap.xml"""
        SitemapGenerator.generate(self.pages, self.config, self.public_dir / 'sitemap.xml')
        print('Generated sitemap.xml')

    def copy_static_assets(self):
        """Copy static assets to public directory"""
        # Copy from static/
        if Path('static').exists():
            shutil.copytree('static', self.public_dir, dirs_exist_ok=True)
            print('Copied static/ assets')

        # Copy from assets/
        assets_dir = Path('assets')
        if assets_dir.exists():
            shutil.copytree(assets_dir, self.public_dir, dirs_exist_ok=True)
            print('Copied assets/ (CSS, JS, fonts)')

        # Copy robots.txt if exists
        if Path('static/robots.txt').exists():
            shutil.copy('static/robots.txt', self.public_dir / 'robots.txt')

    def clean(self):
        """Clean the public directory"""
        if self.public_dir.exists():
            shutil.rmtree(self.public_dir)
        self.public_dir.mkdir()
        print('Cleaned public directory')

    def build(self):
        """Main build process"""
        print('Starting build...')
        self.clean()
        self.collect_content()
        self.render_content()
        self.generate_pages()
        self.generate_feeds()
        self.generate_sitemap()
        self.copy_static_assets()
        print('Build complete!')


def main():
    """Main entry point"""
    builder = Builder()
    builder.build()


if __name__ == '__main__':
    main()
