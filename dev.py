"""
Development server with hot-reload.
Watches for file changes and automatically rebuilds the site.
"""

import os
import sys
import time
import subprocess
import threading
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler


class DevServer:
    """Development server with auto-rebuild on file changes"""

    def __init__(self, port=8000):
        self.port = port
        self.watched_dirs = ['content', 'templates', 'assets', 'static', 'config.toml', 'build.py']
        self.last_modified = {}
        self.building = False
        self.server = None

    def get_file_mtimes(self):
        """Get modification times for all watched files"""
        mtimes = {}

        for path_str in self.watched_dirs:
            path = Path(path_str)

            if path.is_file():
                mtimes[str(path)] = path.stat().st_mtime
            elif path.is_dir():
                for file in path.rglob('*'):
                    if file.is_file():
                        mtimes[str(file)] = file.stat().st_mtime

        return mtimes

    def has_changes(self):
        """Check if any watched files have changed"""
        current_mtimes = self.get_file_mtimes()

        # First run - initialize
        if not self.last_modified:
            self.last_modified = current_mtimes
            return False

        # Check for changes
        if current_mtimes != self.last_modified:
            # Find what changed
            changed_files = []
            for file, mtime in current_mtimes.items():
                if file not in self.last_modified or self.last_modified[file] != mtime:
                    changed_files.append(file)

            # Check for deleted files
            for file in self.last_modified:
                if file not in current_mtimes:
                    changed_files.append(f"{file} (deleted)")

            if changed_files:
                print(f"\n📝 Changes detected:")
                for f in changed_files[:5]:  # Show max 5 files
                    print(f"   - {f}")
                if len(changed_files) > 5:
                    print(f"   ... and {len(changed_files) - 5} more")

            self.last_modified = current_mtimes
            return True

        return False

    def build(self):
        """Run the build script"""
        if self.building:
            return

        self.building = True
        try:
            print("\n🔨 Building site...")
            result = subprocess.run(
                [sys.executable, 'build.py'],
                capture_output=True,
                text=True
            )

            if result.returncode == 0:
                print("✅ Build successful!")
                # Print last line of output (usually "Build complete!")
                if result.stdout:
                    last_line = result.stdout.strip().split('\n')[-1]
                    if last_line:
                        print(f"   {last_line}")
            else:
                print("❌ Build failed!")
                if result.stderr:
                    print(result.stderr)
                if result.stdout:
                    print(result.stdout)
        except Exception as e:
            print(f"❌ Build error: {e}")
        finally:
            self.building = False

    def watch(self):
        """Watch for file changes and rebuild"""
        print("\n👀 Watching for changes...")
        print(f"   Watching: {', '.join(self.watched_dirs)}")

        while True:
            try:
                if self.has_changes():
                    self.build()
                time.sleep(0.5)  # Check every 500ms
            except KeyboardInterrupt:
                break

    def start_http_server(self):
        """Start HTTP server in public directory"""
        os.chdir('public')

        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                # Only log errors
                if args[1][0] != '2':  # Not 2xx status
                    super().log_message(format, *args)

        self.server = HTTPServer(('', self.port), QuietHandler)
        print(f"\n🌐 Server running at http://localhost:{self.port}")
        print("   Press Ctrl+C to stop")

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server.shutdown()

    def run(self):
        """Run the development server"""
        print("🚀 Starting development server...\n")

        # Initial build
        self.build()

        # Start file watcher in background thread
        watcher_thread = threading.Thread(target=self.watch, daemon=True)
        watcher_thread.start()

        # Start HTTP server in main thread
        self.start_http_server()


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Development server with hot-reload')
    parser.add_argument('-p', '--port', type=int, default=8000,
                       help='Port to run server on (default: 8000)')
    args = parser.parse_args()

    server = DevServer(port=args.port)
    server.run()


if __name__ == '__main__':
    main()
