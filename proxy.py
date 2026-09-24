import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error
import re
import logging
import json

HOST = '127.0.0.1'
PORT = 8080

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=None, **kwargs)

    def do_GET(self):
        self.handle_proxy_request("GET")

    def handle_proxy_request(self, method):
        path = self.path
        if path.startswith('/'):
            path = path[1:]
        
        url = urllib.parse.unquote(path)
        if not url:
            url = "https://www.youtube.com"

        logging.info(f"Proxying: {method} {url}")

        try:
            req = urllib.request.Request(url, method=method)
            
            # Add headers from the client
            for header in self.headers:
                if header.lower() in ['host', 'content-length', 'origin']:
                    continue # Let the proxy decide these or omit them to avoid CORS issues
                
                req.add_header(header, self.headers[header])
            
            # Force User-Agent to look like a browser to bypass bot-detection
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else None
            if method == "POST" and post_data:
                req.data = post_data

            opener = urllib.request.build_opener()
            try:
                response = opener.open(req, timeout=15)
            except urllib.error.HTTPError as e:
                self.send_error(e.code, f"Proxy Error: {e.reason}")
                return

            content_type = response.headers.get('Content-Type', '')
            content = response.read()

            # Rewrite HTML/CSS to fix relative URLs
            if 'text/html' in content_type:
                content = self.rewrite_html(content, url)
            elif 'text/css' in content_type:
                content = self.rewrite_css(content, url)
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            
            # These headers force the browser to allow the content to be embedded
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('X-Frame-Options', 'SAMEORIGIN')
            self.send_header('Content-Security-Policy', "frame-ancestors 'self' *;")
            
            self.end_headers()
            self.wfile.write(content)

        except Exception as e:
            logging.error(f"General Error: {e}")
            self.send_error(500, f"Internal Server Error: {str(e)}")

    def rewrite_html(self, html_bytes, base_url):
        try:
            html = html_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return html_bytes

        # 1. Remove blocking meta tags
        html = re.sub(r'<meta[^>]*http-equiv=["\']?X-Frame-Options["\']?[^>]*>', '', html, flags=re.IGNORECASE)
        html = re.sub(r'<meta[^>]*http-equiv=["\']?Content-Security-Policy["\']?[^>]*>', '', html, flags=re.IGNORECASE)

        # 2. Rewrite relative URLs
        html = re.sub(r'(["\'])/([^"]+)', r'\1/http://127.0.0.1:8080/\2', html)
        html = re.sub(r'(["\'])//([^"]+)', r'\1http://127.0.0.1:8080/\2', html)

        # 3. FIX YOUTUBE EMBEDS - Force 'embed' format
        # Convert watch?v= to embed/
        html = re.sub(r'youtube\.com/(?:watch\?v=|embed/)([a-zA-Z0-9_-]+)', r'https://www.youtube.com/embed/\1', html)
        
        # Add the allow attribute to all iframes
        html = re.sub(r'<iframe([^>]*)>', r'<iframe\1 allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>', html, flags=re.IGNORECASE)

        return html.encode('utf-8')

    def rewrite_css(self, css_bytes, base_url):
        try:
            css = css_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return css_bytes
        css = re.sub(r'url\(([^)]+)\)', lambda m: f"url('{base_url}{m.group(1)}')", css)
        return css.encode('utf-8')

if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), ProxyHandler) as httpd:
        print(f"Serving on http://{HOST}:{PORT}")
        httpd.serve_forever()
