#!/usr/bin/env python3
"""
Static site generator.
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


# Site configuration
BASE_URL = 'https://www.zansara.dev'
SITE_TITLE = 'Sara Zan'
LANGUAGE = 'en'
NAVBAR_TITLE = "Sara Zan's Blog"
AUTHOR = 'Sara Zan'
AUTHOR_INFO = """Experienced Python software engineer with extensive experience with NLP, LLMs GenAI and AI in general.
I worked on projects ranging from air-gapped [RAG pipelines](https://www.linkedin.com/posts/bnpparibascorporateandinstitutionalbanking_our-genai-assistant-is-now-available-to-everyone-activity-7370738071648067584-dzrh/)
to [voice AI recruiters](https://archive.today/IH48a),
open-source [LLM frameworks](https://github.com/deepset-ai/haystack),
[particle accelerators](/publications/thpv014/) software,
[IoT](/projects/zanzocam/) devices overwintering at several alpine huts,
and small [web apps](/projects/booking-system/).
Open-source [contributor](https://github.com/ZanSara) and former [CERN](https://home.cern/) employee."""
DESCRIPTION = "Sara Zan's Personal Blog"
KEYWORDS = 'blog,developer,personal,python,llm,nlp,swe,software-engineering,open-source,ai,genai'
AVATAR_URL = '/me/avatar.svg'
FAVICON_SVG = '/me/avatar.svg'
FAVICON_32 = '/me/avatar.png'
SINCE_YEAR = 2023
COLOR_SCHEME = 'auto'

MENU_ITEMS = [
    {'name': 'About', 'weight': 1, 'url': 'about'},
    {'name': 'Posts', 'weight': 2, 'url': 'posts/'},
    {'name': 'Projects', 'weight': 3, 'url': 'projects/'},
    {'name': 'Publications', 'weight': 5, 'url': 'publications/'},
    {'name': 'Talks', 'weight': 6, 'url': 'talks/'},
]


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
        md = markdown.Markdown(extensions=[
            'fenced_code',
            'tables',
            'nl2br',
            'codehilite'
        ])
        self.html_content = md.convert(self.content)

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


def base_template(content, title, meta_tags='', has_mermaid=False):
    """Generate the base HTML template"""
    mermaid_script = '''
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js" crossorigin="anonymous"></script>
  <script>
    mermaid.initialize({ startOnLoad: true });
  </script>''' if has_mermaid else ''

    template = TemplateLoader.load('base.html')
    return template.format(
        language=LANGUAGE,
        title=title,
        site_title=SITE_TITLE,
        author=AUTHOR,
        description=DESCRIPTION,
        keywords=KEYWORDS,
        meta_tags=meta_tags,
        base_url=BASE_URL,
        favicon_svg=FAVICON_SVG,
        favicon_32=FAVICON_32,
        color_scheme=COLOR_SCHEME,
        header=header_component(),
        content=content,
        footer=footer_component(),
        mermaid_script=mermaid_script
    )


def header_component():
    """Generate navigation header"""
    menu_html = '\n'.join([
        f'            <li class="navigation-item">\n              <a class="navigation-link" style="height: 30px;" href="/{item["url"]}">{item["name"]}</a>\n            </li>'
        for item in MENU_ITEMS
    ])

    template = TemplateLoader.load('header.html')
    return template.format(
        navbar=NAVBAR_TITLE,
        menu_items=menu_html
    )


def footer_component():
    """Generate footer"""
    year = datetime.now().year
    since_text = f'{SINCE_YEAR} -' if SINCE_YEAR < year else ''

    template = TemplateLoader.load('footer.html')
    return template.format(
        since_text=since_text,
        year=year
    )


def post_template(page):
    """Generate template for a post page"""
    featured_image = f'<img style="width:100%;" src="{page.featured_image}" alt="Featured image"/>' if page.featured_image else ''

    meta_tags = ''
    if page.featured_image:
        meta_tags = f'''<meta name="image" content="{page.featured_image}">
  <meta name="og:image" content="{page.featured_image}">
  <meta name="twitter:image" content="{BASE_URL}{page.featured_image}">'''

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

    has_mermaid = '<div class="mermaid">' in page.html_content
    return base_template(content_html, page.title, meta_tags, has_mermaid)


def list_template(section, pages):
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

    return base_template(content_html, section.capitalize())


def home_template(recent_posts):
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
        avatar_url=AVATAR_URL,
        description=DESCRIPTION,
        social_links=social_links,
        recent_posts=recent_html
    )

    return base_template(content_html, SITE_TITLE)


def series_template(series_name, pages):
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

    return base_template(content_html, f'Series: {series_name}')


class RSSGenerator:
    """Generate RSS feeds"""

    @staticmethod
    def generate(pages, output_path, section_name=''):
        """Generate an RSS feed"""
        rss = Element('rss', version='2.0')
        rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')

        channel = SubElement(rss, 'channel')

        # Channel metadata
        if section_name:
            title_text = f'{section_name.capitalize()} on {SITE_TITLE}'
            desc_text = f'Recent content in {section_name} on {SITE_TITLE}'
            link_text = f'{BASE_URL}/{section_name}/'
        else:
            title_text = SITE_TITLE
            desc_text = f'Recent content on {SITE_TITLE}'
            link_text = BASE_URL + '/'

        SubElement(channel, 'title').text = title_text
        SubElement(channel, 'link').text = link_text
        SubElement(channel, 'description').text = desc_text
        SubElement(channel, 'generator').text = 'Python Static Site Generator'
        SubElement(channel, 'language').text = LANGUAGE

        if pages:
            latest_date = max(p.date for p in pages)
            SubElement(channel, 'lastBuildDate').text = latest_date.strftime('%a, %d %b %Y %H:%M:%S %z')

        # Add items
        for page in sorted(pages, key=lambda x: x.date, reverse=True)[:20]:
            item = SubElement(channel, 'item')
            SubElement(item, 'title').text = page.title
            SubElement(item, 'link').text = BASE_URL + page.url
            SubElement(item, 'pubDate').text = page.date.strftime('%a, %d %b %Y %H:%M:%S +0000')
            SubElement(item, 'guid').text = BASE_URL + page.url
            SubElement(item, 'description').text = page.html_content

        # Write to file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
            f.write(tostring(rss, encoding='utf-8'))


class SitemapGenerator:
    """Generate sitemap.xml"""

    @staticmethod
    def generate(pages, output_path):
        """Generate sitemap"""
        urlset = Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')

        # Add homepage
        url = SubElement(urlset, 'url')
        SubElement(url, 'loc').text = BASE_URL + '/'
        SubElement(url, 'lastmod').text = datetime.now().strftime('%Y-%m-%d')

        # Add all pages
        for page in pages:
            url = SubElement(urlset, 'url')
            SubElement(url, 'loc').text = BASE_URL + page.url
            SubElement(url, 'lastmod').text = page.date.strftime('%Y-%m-%d')

        # Write to file
        with open(output_path, 'wb') as f:
            f.write(b'<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n')
            f.write(tostring(urlset, encoding='utf-8'))


class Builder:
    """Main builder class that orchestrates the build process"""

    def __init__(self):
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
            html = post_template(page)

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
            html = list_template(section, section_pages)
            output_path = self.public_dir / section / 'index.html'
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding='utf-8')

        # Generate homepage
        all_posts = [p for p in self.pages if p.section in ['posts', 'demos', 'talks']]
        all_posts.sort(key=lambda x: x.date, reverse=True)
        homepage_html = home_template(all_posts)
        (self.public_dir / 'index.html').write_text(homepage_html, encoding='utf-8')

        # Generate series pages
        by_series = defaultdict(list)
        for page in self.pages:
            for series in page.series:
                by_series[series].append(page)

        for series_name, series_pages in by_series.items():
            slug = series_name.lower().replace(' ', '-')
            html = series_template(series_name, series_pages)
            output_path = self.public_dir / 'series' / slug / 'index.html'
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding='utf-8')

        print(f'Generated {len(self.pages)} pages, {len(by_section)} section lists, homepage, and {len(by_series)} series pages')

    def generate_feeds(self):
        """Generate RSS feeds"""
        # Main feed
        all_pages = [p for p in self.pages if p.section in ['posts', 'talks', 'demos', 'projects', 'publications']]
        RSSGenerator.generate(all_pages, self.public_dir / 'index.xml')

        # Section feeds
        by_section = defaultdict(list)
        for page in self.pages:
            if page.section:
                by_section[page.section].append(page)

        for section, pages in by_section.items():
            RSSGenerator.generate(pages, self.public_dir / section / 'index.xml', section)

        print(f'Generated main RSS feed and {len(by_section)} section feeds')

    def generate_sitemap(self):
        """Generate sitemap.xml"""
        SitemapGenerator.generate(self.pages, self.public_dir / 'sitemap.xml')
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
