import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error
import re
import logging
import os

# Configuration
HOST = '127.0.0.1'
PORT = 8080

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=None, **kwargs)

    def do_GET(self):
        self.handle_proxy_request("GET")

    def do_POST(self):
        self.handle_proxy_request("POST")

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
            
            # Forward headers, but strip Host to avoid confusion
            for header in self.headers:
                if header.lower() not in ['host', 'content-length', 'content-length']:
                    req.add_header(header, self.headers[header])
            
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
            except Exception as e:
                self.send_error(502, "Bad Gateway")
                return

            content_type = response.headers.get('Content-Type', '')
            content = response.read()

            if 'text/html' in content_type:
                content = self.rewrite_html(content, url)
            elif 'text/css' in content_type:
                content = self.rewrite_css(content, url)
            elif 'text/javascript' in content_type:
                content = self.rewrite_js(content, url)
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            
            # CRITICAL: Force these headers to allow embedding
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('X-Frame-Options', 'SAMEORIGIN') # Or 'DENY' if you prefer strict, but SAMEORIGIN is safer for iframe
            self.send_header('Content-Security-Policy', "frame-ancestors 'self' *;") # Allow ANYONE to embed us
            
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

        # 1. Remove X-Frame-Options meta tags
        html = re.sub(r'<meta[^>]*http-equiv=["\']?X-Frame-Options["\']?[^>]*>', '', html, flags=re.IGNORECASE)
        
        # 2. Remove CSP meta tags
        html = re.sub(r'<meta[^>]*http-equiv=["\']?Content-Security-Policy["\']?[^>]*>', '', html, flags=re.IGNORECASE)

        # 3. Rewrite relative URLs to point to our proxy
        # This ensures images, CSS, and JS also go through the proxy
        html = re.sub(r'(["\'])/([^"]+)', r'\1/http://127.0.0.1:8080/\2', html)
        html = re.sub(r'(["\'])//([^"]+)', r'\1http://127.0.0.1:8080/\2', html)
        
        # Fix specific YouTube iframe issues if present
        html = re.sub(r'(?i)allowfullscreen="false"', 'allowfullscreen="true"', html)

        return html.encode('utf-8')

    def rewrite_css(self, css_bytes, base_url):
        try:
            css = css_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return css_bytes
        # Rewrite relative URLs in CSS
        css = re.sub(r'url\(([^)]+)\)', lambda m: f"url('{base_url}{m.group(1)}')", css)
        return css.encode('utf-8')

    def rewrite_js(self, js_bytes, base_url):
        # Basic rewrite for JS, though less common to have assets here
        return js_bytes

if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), ProxyHandler) as httpd:
        print(f"Serving on http://{HOST}:{PORT}")
        httpd.serve_forever()
