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
DESCRIPTION = "Sara Zan's Blog"
KEYWORDS = 'blog,developer,personal,python,llm,nlp,swe,software-engineering,open-source,ai,genai'
AVATAR_URL = '/assets/avatar/avatar.svg'
FAVICON_SVG = '/assets/avatar/avatar.svg'
FAVICON_32 = '/assets/avatar/avatar.png'
SINCE_YEAR = 2023

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
        # If the file is named post.md, use the parent directory name as the slug
        if self.path.name == 'post.md':
            stem = self.path.parent.name
        else:
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

    def preprocess_html_tags_with_markdown(self, content):
        """
        Preprocess HTML tags to convert markdown content between tags when there are empty lines.

        Pattern: <tag>...\n\nmarkdown content\n\n</tag>
        The markdown content will be converted, but <tag>...markdown...</tag> will be left as-is.
        """
        # First pass: Handle content directly between opening and closing tags with empty lines
        # Pattern: <tag>\n\ncontent\n\n</tag>
        pattern1 = r'<(\w+)([^>]*)>\n\n(.*?)\n\n</\1>'

        def replace_direct_match(match):
            tag_name = match.group(1)
            tag_attrs = match.group(2)
            inner_content = match.group(3)

            # Create a temporary markdown renderer for the inner content
            # Don't use nl2br here as it interferes with HTML tags
            md = markdown.Markdown(extensions=[
                'fenced_code',
                'tables',
                'codehilite'
            ])
            # Convert the markdown content
            rendered_content = md.convert(inner_content)

            # Return the tag with rendered content
            return f'<{tag_name}{tag_attrs}>\n\n{rendered_content}\n\n</{tag_name}>'

        # Second pass: Handle content between </summary> and </details> specifically
        # Pattern: </summary>\n\ncontent (can include empty lines)\s*</details>
        # This handles cases like <details><summary>X</summary>\n\ncontent\n\n</details>
        # Use .+? to match content (one or more chars, non-greedy) and \s* for trailing whitespace
        pattern2 = r'</summary>\n\n(.+?)\s*</details>'

        def replace_summary_details_match(match):
            inner_content = match.group(1)

            # Create a temporary markdown renderer for the inner content
            # Don't use nl2br here as it interferes with HTML tags
            md = markdown.Markdown(extensions=[
                'fenced_code',
                'tables',
                'codehilite'
            ])
            # Convert the markdown content
            rendered_content = md.convert(inner_content)

            # Return with rendered content
            return f'</summary>\n\n{rendered_content}\n\n</details>'

        # Apply both patterns
        # Use DOTALL flag so . matches newlines within the content
        processed = re.sub(pattern1, replace_direct_match, content, flags=re.DOTALL)
        processed = re.sub(pattern2, replace_summary_details_match, processed, flags=re.DOTALL)

        return processed

    def add_invertible_class_to_images(self, html_content):
        """
        Add 'invertible' class to images whose filename ends with -inv

        For example: image-inv.png -> <img ... class="invertible">
        """
        def replace_img(match):
            img_tag = match.group(0)
            src = match.group(1)

            # Check if the filename (before extension) ends with -inv
            # Pattern: something-inv.ext
            if re.search(r'-inv\.[^/]*$', src):
                # Check if class attribute already exists
                if 'class=' in img_tag:
                    # Append to existing class attribute
                    img_tag = re.sub(
                        r'class="([^"]*)"',
                        r'class="\1 invertible"',
                        img_tag
                    )
                else:
                    # Add class attribute before the closing /> or >
                    # Handle both self-closing and regular tags
                    if img_tag.endswith('/>'):
                        img_tag = img_tag[:-2] + ' class="invertible" />'
                    else:
                        img_tag = img_tag[:-1] + ' class="invertible">'

            return img_tag

        # Match <img> tags and capture the src attribute
        pattern = r'<img[^>]+src="([^"]+)"[^>]*/?>'
        return re.sub(pattern, replace_img, html_content)

    def render(self):
        """Render markdown content to HTML"""
        # First preprocess HTML tags with markdown content
        preprocessed_content = self.preprocess_html_tags_with_markdown(self.content)

        md = markdown.Markdown(extensions=[
            'fenced_code',
            'tables',
            'nl2br',
            'codehilite'
        ])
        html_content = md.convert(preprocessed_content)

        # Add invertible class to images with -inv suffix
        self.html_content = self.add_invertible_class_to_images(html_content)

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
        return self.front_matter.get('featured-image', '')

    @property
    def series(self):
        s = self.front_matter.get('series', [])
        return s if isinstance(s, list) else [s] if s else []

    @property
    def external_link(self):
        return self.front_matter.get('external-link', '')

    @property
    def aliases(self):
        a = self.front_matter.get('aliases', [])
        return a if isinstance(a, list) else [a] if a else []

    @property
    def show_date(self):
        return bool(self.front_matter.get('show-date', True))

    @property
    def is_draft(self):
        return bool(self.front_matter.get('draft', False))

    def get_effective_url(self):
        """Get the effective URL - external link if set, otherwise internal URL"""
        return self.external_link if self.external_link else self.url


def base_template(content, title, meta_tags='', has_mermaid=False):
    """Generate the base HTML template"""
    mermaid_script = ''
    if has_mermaid:
        mermaid_script = '''
            <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.0/dist/mermaid.min.js" crossorigin="anonymous"></script>
            <script>
                mermaid.initialize({ startOnLoad: true });
            </script>'''

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
        header=header_component(),
        content=content,
        footer=footer_component(),
        mermaid_script=mermaid_script
    )


def header_component():
    """Generate navigation header"""
    menu_item_template = TemplateLoader.load('menu-item.html')
    menu_html = '\n'.join([
        menu_item_template.format(url=item['url'], name=item['name'])
        for item in MENU_ITEMS
    ])

    template = TemplateLoader.load('header.html')
    return template.format(
        navbar_title=NAVBAR_TITLE,
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


def get_invertible_class_attr(image_path):
    """Check if image path ends with -inv and return class attribute string"""
    if image_path and re.search(r'-inv\.[^/]*$', image_path):
        return 'class="invertible"'
    return ''

def post_template(page):
    """Generate template for a post page"""
    featured_image = ''
    if page.featured_image:
        img_template = TemplateLoader.load('featured-image.html')
        class_attr = get_invertible_class_attr(page.featured_image)
        featured_image = img_template.format(src=page.featured_image, class_attr=class_attr)

    meta_tags = ''
    if page.featured_image:
        meta_template = TemplateLoader.load('meta-image.html')
        meta_tags = meta_template.format(
            image_url=page.featured_image,
            base_url=BASE_URL
        )

    if page.section in ["posts"]:
        template = TemplateLoader.load('post.html')
    else:
        template = TemplateLoader.load('page.html')

    desc_template = TemplateLoader.load('description.html')
    desc_line = desc_template.format(
        description=escape(page.description)
    )

    date_template = TemplateLoader.load('date.html')
    date_line = date_template.format(
        datetime=page.date.strftime('%Y-%m-%dT%H:%M:%SZ'),
        date_formatted=page.date.strftime('%B %d, %Y'),
    )
    content_html = template.format(
        url=page.url,
        title=escape(page.title),
        date=date_line,
        description=desc_line,
        featured_image=featured_image,
        html_content=page.html_content
    )

    has_mermaid = '<div class="mermaid">' in page.html_content
    return base_template(content_html, page.title, meta_tags, has_mermaid)


def list_template(section, pages):
    """Generate template for section list pages"""
    item_template = TemplateLoader.load('list-item.html')
    items_html = '\n'.join([
        item_template.format(
            featured_image=p.featured_image,
            description=p.description,
            date=p.date.strftime('%B %d, %Y'),
            url=p.get_effective_url(),
            title=escape(p.title),
            class_attr=get_invertible_class_attr(p.featured_image)
        )
        for p in sorted(pages, key=lambda x: x.date, reverse=True)
    ])

    template = TemplateLoader.load('list.html')
    content_html = template.format(
        section_title=section.capitalize(),
        items=items_html
    )

    return base_template(content_html, section.capitalize())


def home_template(recent_posts, recent_talks):
    """Generate homepage template"""
    item_template = TemplateLoader.load('list-item.html')
    recent_posts_html = '\n'.join([
        item_template.format(
            featured_image=p.featured_image,
            description=p.description,
            date=p.date.strftime('%B %d, %Y'),
            url=p.get_effective_url(),
            title=escape(p.title),
            class_attr=get_invertible_class_attr(p.featured_image)
        )
        for p in recent_posts[:4]
    ])
    recent_talks_html = '\n'.join([
        item_template.format(
            featured_image=p.featured_image,
            description=p.description,
            date=p.date.strftime('%B %d, %Y'),
            url=p.get_effective_url(),
            title=escape(p.title),
            class_attr=get_invertible_class_attr(p.featured_image)
        )
        for p in recent_talks[:4]
    ])

    # Load social links template
    social_links = TemplateLoader.load('social-links.html')

    template = TemplateLoader.load('home.html')
    content_html = template.format(
        avatar_url=AVATAR_URL,
        social_links=social_links,
        recent_posts=recent_posts_html,
        recent_talks=recent_talks_html
    )

    return base_template(content_html, "Home")


def series_template(series_name, pages):
    """Generate template for series pages"""
    item_template = TemplateLoader.load('list-item.html')
    items_html = '\n'.join([
        item_template.format(
            featured_image=p.featured_image,
            description=p.description,
            date=p.date.strftime('%B %d, %Y'),
            url=p.get_effective_url(),
            title=escape(p.title),
            class_attr=get_invertible_class_attr(p.featured_image)
        )
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
        SubElement(channel, 'generator').text = 'Custom Script'
        SubElement(channel, 'language').text = LANGUAGE

        if pages:
            latest_date = max(p.date for p in pages)
            SubElement(channel, 'lastBuildDate').text = latest_date.strftime('%a, %d %b %Y %H:%M:%S %z')

        # Add items
        for page in sorted(pages, key=lambda x: x.date, reverse=True)[:20]:
            item = SubElement(channel, 'item')
            SubElement(item, 'title').text = page.title
            effective_url = page.get_effective_url()
            # For external links, use them directly; for internal, prepend BASE_URL
            link_url = effective_url if page.external_link else BASE_URL + effective_url
            SubElement(item, 'link').text = link_url
            SubElement(item, 'pubDate').text = page.date.strftime('%a, %d %b %Y %H:%M:%S +0000')
            SubElement(item, 'guid').text = link_url
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

        # Add all pages (only internal pages, not external links)
        for page in pages:
            if not page.external_link:
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
        self.pages = []  # Clear pages list before collecting
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
        # Filter out drafts
        published_pages = [p for p in self.pages if not p.is_draft]
        draft_count = len(self.pages) - len(published_pages)

        # Separate pages with external links (no individual page generation)
        internal_pages = [p for p in published_pages if not p.external_link]
        external_link_count = len(published_pages) - len(internal_pages)

        # Group pages by section (include external links for listing)
        by_section = defaultdict(list)
        for page in published_pages:
            if page.section:
                by_section[page.section].append(page)

        # Generate individual pages (only for internal pages, not external links)
        for page in internal_pages:
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
        posts = sorted([p for p in published_pages if p.section == "posts"], key=lambda x: x.date, reverse=True)
        talks = sorted([p for p in published_pages if p.section == "talks"], key=lambda x: x.date, reverse=True)
        homepage_html = home_template(posts, talks)
        (self.public_dir / 'index.html').write_text(homepage_html, encoding='utf-8')

        # Generate series pages
        by_series = defaultdict(list)
        for page in published_pages:
            for series in page.series:
                by_series[series].append(page)

        for series_name, series_pages in by_series.items():
            slug = series_name.lower().replace(' ', '-')
            html = series_template(series_name, series_pages)
            output_path = self.public_dir / 'series' / slug / 'index.html'
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding='utf-8')

        print(f'Generated {len(internal_pages)} pages, {len(by_section)} section lists, homepage, and {len(by_series)} series pages')
        if draft_count > 0:
            print(f'Skipped {draft_count} draft pages')
        if external_link_count > 0:
            print(f'Skipped {external_link_count} pages with external links (included in listings)')

    def generate_feeds(self):
        """Generate RSS feeds"""
        # Filter out drafts
        published_pages = [p for p in self.pages if not p.is_draft]

        # Main feed
        all_pages = [p for p in published_pages if p.section in ['posts', 'talks', 'demos', 'projects', 'publications']]
        RSSGenerator.generate(all_pages, self.public_dir / 'index.xml')

        # Section feeds
        by_section = defaultdict(list)
        for page in published_pages:
            if page.section:
                by_section[page.section].append(page)

        for section, pages in by_section.items():
            RSSGenerator.generate(pages, self.public_dir / section / 'index.xml', section)

        print(f'Generated main RSS feed and {len(by_section)} section feeds')

    def generate_sitemap(self):
        """Generate sitemap.xml"""
        # Filter out drafts
        published_pages = [p for p in self.pages if not p.is_draft]
        SitemapGenerator.generate(published_pages, self.public_dir / 'sitemap.xml')
        print('Generated sitemap.xml')

    def generate_404_page(self):
        """Generate 404 error page"""
        template = TemplateLoader.load('404.html')
        html = base_template(template, '404 - Page Not Found')

        output_path = self.public_dir / '404.html'
        output_path.write_text(html, encoding='utf-8')
        print('Generated 404.html')

    def copy_static_assets(self):
        """Copy static assets to public directory"""
        # Create a set of published page paths for quick lookup
        published_paths = {p.path for p in self.pages if not p.is_draft}

        # Copy assets from content directories (images alongside post.md files)
        content_dir = Path('content')
        for section_dir in content_dir.iterdir():
            if not section_dir.is_dir():
                continue

            for item_dir in section_dir.iterdir():
                if not item_dir.is_dir():
                    continue

                # Check if this directory contains a post.md file
                post_md_path = item_dir / 'post.md'
                if post_md_path.exists():
                    # Skip if this is a draft post
                    if post_md_path not in published_paths:
                        continue

                    # Copy all non-.md files from this directory
                    dest_dir = self.public_dir / section_dir.name / item_dir.name
                    dest_dir.mkdir(parents=True, exist_ok=True)

                    for file in item_dir.iterdir():
                        if file.is_file() and not file.name.endswith('.md'):
                            shutil.copy2(file, dest_dir / file.name)

        print('Copied assets from content directories')

        # Copy from static/ if it still exists (for global assets)
        if Path('static').exists():
            shutil.copytree('static', self.public_dir, dirs_exist_ok=True)
            print('Copied static/ assets')

        # Copy robots.txt if exists
        robots_path = Path('static/robots.txt')
        if not robots_path.exists():
            robots_path = Path('content/robots.txt')
        if robots_path.exists():
            shutil.copy(robots_path, self.public_dir / 'robots.txt')

    def clean(self):
        """Clean the public directory"""
        if self.public_dir.exists():
            # Remove all contents without deleting the directory itself - the webserver is running there
            for item in self.public_dir.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
        else:
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
        self.generate_404_page()
        self.copy_static_assets()
        print('Build complete!')


def main():
    """Main entry point"""
    builder = Builder()
    builder.build()


if __name__ == '__main__':
    main()
