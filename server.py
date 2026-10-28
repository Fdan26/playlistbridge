"""Run a local web server for Playlist Bridge (standard library only)."""
from functools import partial
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

HOST = '127.0.0.1'
PORT = 8000  # Must match the authorized JavaScript origin in Google Cloud.
PUBLIC_DIR = Path(__file__).resolve().parent / 'public'

handler = partial(SimpleHTTPRequestHandler, directory=str(PUBLIC_DIR))
print(f'Playlist Bridge: open http://localhost:{PORT}  (Ctrl+C to stop)')
try:
    ThreadingHTTPServer((HOST, PORT), handler).serve_forever()
except KeyboardInterrupt:
    print('\nStopped.')
