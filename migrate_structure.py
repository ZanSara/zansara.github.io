#!/usr/bin/env python3
"""
Migration script to reorganize the blog structure:
- Merge content/ and static/ folders
- Rename markdown files to post.md
- Place images alongside markdown files
"""

import shutil
from pathlib import Path


def migrate_section(section_name):
    """Migrate a single section (posts, talks, etc.)"""
    content_section = Path('content') / section_name
    static_section = Path('static') / section_name

    if not content_section.exists():
        print(f"⚠️  {content_section} doesn't exist, skipping")
        return

    # Find all markdown files in the section (old structure)
    md_files = list(content_section.glob('*.md'))

    # Also find directories with post.md (new structure)
    post_dirs = [d for d in content_section.iterdir() if d.is_dir() and (d / 'post.md').exists()]

    print(f"\n📁 Migrating {section_name}/ ({len(md_files)} old files, {len(post_dirs)} directories)")

    for md_file in md_files:
        slug = md_file.stem  # e.g., "2025-05-21-vibecoding"

        # Create directory for this post
        post_dir = content_section / slug
        post_dir.mkdir(exist_ok=True)

        # Move markdown file and rename to post.md
        target_md = post_dir / 'post.md'
        if not target_md.exists():
            shutil.move(str(md_file), str(target_md))
            print(f"  ✓ {md_file.name} → {slug}/post.md")
        else:
            print(f"  ⚠️  {target_md} already exists, keeping original")

        # Move assets from static/ if they exist
        # Try both slug-based directory and just slug name for the file
        static_dir = static_section / slug
        if static_dir.exists() and static_dir.is_dir():
            for asset in static_dir.iterdir():
                if asset.is_file():
                    target_asset = post_dir / asset.name
                    if not target_asset.exists():
                        shutil.copy2(str(asset), str(target_asset))
                        print(f"    → copied {asset.name}")

            # Remove the now-empty static directory
            try:
                static_dir.rmdir()
                print(f"    → removed {static_dir}")
            except OSError:
                print(f"    ⚠️  {static_dir} not empty, keeping it")

        # Also check for direct files in static/ (for projects/publications)
        static_file_patterns = [f"{slug}.png", f"{slug}.jpg", f"{slug}.jpeg", f"{slug}.pdf", f"{slug}.svg"]
        for pattern in static_file_patterns:
            static_file = static_section / pattern
            if static_file.exists():
                target_asset = post_dir / pattern
                if not target_asset.exists():
                    shutil.copy2(str(static_file), str(target_asset))
                    print(f"    → copied {pattern}")

    # Also process already-migrated directories that need assets
    for post_dir in post_dirs:
        slug = post_dir.name
        if slug in [md.stem for md in md_files]:
            continue  # Already processed above

        print(f"  📦 {slug}/post.md (copying remaining assets)")

        # Copy assets from static/ directory
        static_dir = static_section / slug
        if static_dir.exists() and static_dir.is_dir():
            for asset in static_dir.iterdir():
                if asset.is_file():
                    target_asset = post_dir / asset.name
                    if not target_asset.exists():
                        shutil.copy2(str(asset), str(target_asset))
                        print(f"    → copied {asset.name}")

        # Also check for direct files in static/
        static_file_patterns = [f"{slug}.png", f"{slug}.jpg", f"{slug}.jpeg", f"{slug}.pdf", f"{slug}.svg"]
        for pattern in static_file_patterns:
            static_file = static_section / pattern
            if static_file.exists():
                target_asset = post_dir / pattern
                if not target_asset.exists():
                    shutil.copy2(str(static_file), str(target_asset))
                    print(f"    → copied {pattern}")


def main():
    """Main migration function"""
    print("="*60)
    print("Blog Structure Migration")
    print("="*60)

    # Migrate different sections
    sections = ['posts', 'talks', 'projects', 'publications']

    for section in sections:
        migrate_section(section)

    print("\n" + "="*60)
    print("Migration complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Review the changes")
    print("2. Remove empty static/ subdirectories if desired")
    print("3. Run 'python3 build.py' to test the new structure")


if __name__ == '__main__':
    main()
