import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error
import re
import logging
import sys
import os

# Configuration
HOST = '127.0.0.1'
PORT = 8080

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve from the current directory so we can serve index.html
        super().__init__(*args, directory=os.getcwd(), **kwargs)

    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def handle_request(self, method):
        # 1. Check if this is a request for our local index.html or CSS/JS
        if self.path == '/' or self.path == '/index.html':
            super().do_GET()
            return
        
        # 2. Extract the target URL from the path
        # The client sends: /http://youtube.com
        path = self.path
        if path.startswith('/'):
            path = path[1:]
        
        url = urllib.parse.unquote(path)
        if not url:
            url = "https://www.youtube.com"

        logging.info(f"Proxying: {method} {url}")

        try:
            # Build request to target
            req = urllib.request.Request(url, method=method)
            
            # Forward headers (except host and content-length which we handle)
            for header in self.headers:
                if header.lower() not in ['host', 'content-length']:
                    req.add_header(header, self.headers[header])
            
            # Handle POST data
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else None
            
            if method == "POST" and post_data:
                req.data = post_data

            # Open connection
            opener = urllib.request.build_opener()
            try:
                response = opener.open(req, timeout=10)
            except urllib.error.HTTPError as e:
                logging.error(f"HTTP Error from {url}: {e.code}")
                self.send_error(e.code, f"Proxy Error: {e.reason}")
                return
            except Exception as e:
                logging.error(f"Failed to fetch {url}: {e}")
                self.send_error(502, "Bad Gateway")
                return

            content_type = response.headers.get('Content-Type', '')
            content = response.read()

            # 3. Process Content
            if 'text/html' in content_type:
                content = self.rewrite_html(content, url)
            elif 'text/css' in content_type:
                content = self.rewrite_css(content, url)
            elif 'text/javascript' in content_type:
                content = self.rewrite_js(content, url)
            
            # 4. Send Response
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            
            # CORS headers to allow iframe embedding
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            
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

        # Strip blocking headers from meta tags
        html = re.sub(r'<meta[^>]*http-equiv=["\']?X-Frame-Options["\']?[^>]*>', '', html, flags=re.IGNORECASE)
        html = re.sub(r'<meta[^>]*http-equiv=["\']?Content-Security-Policy["\']?[^>]*>', '', html, flags=re.IGNORECASE)

        # Rewrite URLs
        # Matches: href="...", src="...", action="...", etc.
        pattern = re.compile(r'(href|src|action|srcset|data-src|background|poster|srcdoc)="([^"]+)"')
        
        def replace_url(match):
            attr = match.group(1)
            url = match.group(2)
            
            # Skip anchors, javascript, mailto, data URIs
            if not url or url.startswith('#') or url.startswith('javascript:') or url.startswith('mailto:') or url.startswith('data:'):
                return match.group(0)
            
            # Make relative URLs absolute
            if not url.startswith('http://') and not url.startswith('https://'):
                url = urllib.parse.urljoin(base_url, url)
            
            # Rewrite to go through proxy
            return f'{attr}="/{url}"'

        html = pattern.sub(replace_url, html)
        
        # YouTube specific: Convert watch links to embed links for better iframe compatibility
        html = re.sub(r'youtube\.com/watch\?v=([^"&]+)', r'youtube.com/embed/\1', html)
        
        return html.encode('utf-8')

    def rewrite_css(self, css_bytes, base_url):
        try:
            css = css_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return css_bytes
        
        pattern = re.compile(r'url\(["\']?([^"\')]+)["\']?\)')
        
        def replace_css_url(match):
            url = match.group(1)
            if url and not url.startswith('http'):
                absolute_url = urllib.parse.urljoin(base_url, url)
                return f'url("/{absolute_url}")'
            elif url and url.startswith('http'):
                return f'url("/{url}")'
            return match.group(0)
        
        return pattern.sub(replace_css_url, css).encode('utf-8')

    def rewrite_js(self, js_bytes, base_url):
        try:
            js = js_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return js_bytes
        
        # Simple URL rewriting in JS
        pattern = re.compile(r'(url\(["\']?([^"\')]+)["\']?\))')
        
        def replace_js_url(match):
            url = match.group(2)
            if url and not url.startswith('http'):
                absolute_url = urllib.parse.urljoin(base_url, url)
                return f'url("/{absolute_url}")'
            return match.group(0)
        
        return pattern.sub(replace_js_url, js).encode('utf-8')

    def log_message(self, format, *args):
        logging.info(format % args)

def start_server():
    with socketserver.ThreadingTCPServer((HOST, PORT), ProxyHandler) as httpd:
        logging.info(f"Proxy server running on http://{HOST}:{PORT}")
        logging.info("Open http://{HOST}:{PORT} in your browser")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
