#!/usr/bin/env python3
"""
File watcher that rebuilds the static site when changes are detected.
Uses debouncing to avoid rebuilding too frequently.
"""

import sys
import time
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import the builder from build.py
from build import Builder, TemplateLoader


class RebuildHandler(FileSystemEventHandler):
    """Handles file system events and triggers rebuilds with debouncing"""

    def __init__(self, builder, debounce_seconds=2.0):
        self.builder = builder
        self.debounce_seconds = debounce_seconds
        self.rebuild_timer = None
        self.rebuild_lock = threading.Lock()
        self.pending_changes = []

    def should_watch(self, event):
        """Determine if a file change should trigger a rebuild"""
        # Ignore changes in public/ directory
        if 'public' in Path(event.src_path).parts:
            return False

        # Ignore hidden files and directories
        if any(part.startswith('.') for part in Path(event.src_path).parts):
            return False

        # Ignore temporary files
        if event.src_path.endswith(('~', '.swp', '.tmp')):
            return False

        return True

    def schedule_rebuild(self):
        """Schedule a rebuild after debounce period"""
        with self.rebuild_lock:
            # Cancel existing timer if any
            if self.rebuild_timer:
                self.rebuild_timer.cancel()

            # Schedule new rebuild
            self.rebuild_timer = threading.Timer(
                self.debounce_seconds,
                self.rebuild
            )
            self.rebuild_timer.start()

    def rebuild(self):
        """Perform the rebuild"""
        print('\n' + '='*60)
        print('🔄 Rebuilding site...')
        print('='*60)

        try:
            # Clear template cache
            TemplateLoader._cache.clear()

            # Rebuild the site
            self.builder.build()

            print('='*60)
            print('✅ Rebuild complete!')
            print('='*60 + '\n')

        except Exception as e:
            print('='*60)
            print(f'❌ Build failed: {e}')
            print('='*60 + '\n')
            import traceback
            traceback.print_exc()

        # Clear pending changes
        with self.rebuild_lock:
            self.pending_changes.clear()

    def on_modified(self, event):
        if not event.is_directory and self.should_watch(event):
            print(f'📝 Modified: {event.src_path}')
            with self.rebuild_lock:
                self.pending_changes.append(('modified', event.src_path))
            self.schedule_rebuild()

    def on_created(self, event):
        if not event.is_directory and self.should_watch(event):
            print(f'📄 Created: {event.src_path}')
            with self.rebuild_lock:
                self.pending_changes.append(('created', event.src_path))
            self.schedule_rebuild()

    def on_deleted(self, event):
        if not event.is_directory and self.should_watch(event):
            print(f'🗑️  Deleted: {event.src_path}')
            with self.rebuild_lock:
                self.pending_changes.append(('deleted', event.src_path))
            self.schedule_rebuild()


def main():
    """Main entry point"""
    print('='*60)
    print('🚀 Starting file watcher with auto-rebuild')
    print('   Debounce: 2 seconds')
    print('='*60)

    # Create builder instance
    builder = Builder()

    # Initial build
    print('\n📦 Running initial build...\n')
    try:
        builder.build()
        print('\n✅ Initial build complete!')
    except Exception as e:
        print(f'\n❌ Initial build failed: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

    # Set up file watcher
    event_handler = RebuildHandler(builder, debounce_seconds=2.0)
    observer = Observer()

    # Watch these directories for changes
    watch_dirs = ['content', 'templates', 'static', 'assets']
    print('\n👀 Watching for changes:')
    for watch_dir in watch_dirs:
        if Path(watch_dir).exists():
            observer.schedule(event_handler, watch_dir, recursive=True)
            print(f'   • {watch_dir}/')

    # Also watch build.py itself
    observer.schedule(event_handler, '.', recursive=False)
    print('   • build.py')

    print('\nPress Ctrl+C to stop\n')
    print('='*60 + '\n')

    # Start observer
    observer.start()

    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n' + '='*60)
        print('👋 Stopping file watcher...')
        print('='*60)
        observer.stop()

    observer.join()


if __name__ == '__main__':
    main()
