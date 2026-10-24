"""Utility script to launch the local Lumina interactive web studio."""

import http.server
import socket
import socketserver
import webbrowser
from pathlib import Path

DEFAULT_PORT = 8080
ROOT_DIR = Path(__file__).resolve().parent.parent


def find_available_port(start_port: int = DEFAULT_PORT, max_attempts: int = 20) -> int:
    """Finds an open TCP port starting from start_port."""
    for port in range(start_port, start_port + max_attempts):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT_DIR), **kwargs)

    def log_message(self, format: str, *args) -> None:
        pass


def main():
    port = find_available_port(DEFAULT_PORT)
    url = f"http://localhost:{port}/index.html"
    print(f"\n==========================================")
    print(f"  🌟 Lumina Studio - Langue Logique")
    print(f"  Ouvrez : {url}")
    print(f"  Appuyez sur Ctrl+C pour arrêter le serveur.")
    print(f"==========================================\n")
    try:
        webbrowser.open(url)
    except Exception:
        pass

    with socketserver.TCPServer(("127.0.0.1", port), QuietHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nArrêt du serveur Lumina Studio.")


if __name__ == "__main__":
    main()
