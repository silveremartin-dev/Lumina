"""Utility script to launch the local Lumina interactive web studio."""

import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8080
ROOT_DIR = Path(__file__).resolve().parent.parent

class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

def main():
    url = f"http://localhost:{PORT}/index.html"
    print(f"\n==========================================")
    print(f"  🌟 Lumina Studio - Langue Logique")
    print(f"  Ouvrez : {url}")
    print(f"  Appuyez sur Ctrl+C pour arrêter le serveur.")
    print(f"==========================================\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass

    with socketserver.TCPServer(("127.0.0.1", PORT), QuietHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nArrêt du serveur Lumina Studio.")

if __name__ == "__main__":
    main()
