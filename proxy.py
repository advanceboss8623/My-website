import sys
import threading
import urllib.request
import urllib.parse
import urllib.error
import http.server
import socketserver
import socket
import re
import logging

# Configuration
HOST = '127.0.0.1'
PORT = 8080
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'

# Set up logging
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Run the handler in the main thread to avoid socket issues
        super().__init__(*args, directory=None, **kwargs)

    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def handle_request(self, method):
        # Parse the incoming URL from the client
        # The client sends us the full URL they want to fetch, e.g., http://google.com/search?q=test
        # But since we are a proxy, the client sends /http://google.com/search?q=test
        # We strip the leading slash to get the actual URL
        
        path = self.path
        if path.startswith('/'):
            path = path[1:]
        
        url = urllib.parse.unquote(path)
        
        # If it's just /, default to Google
        if not url:
            url = "https://www.google.com"
            path = "https://www.google.com"

        logging.info(f"Proxying: {method} {url}")

        try:
            # Create a request object
            req = urllib.request.Request(url, method=method)
            
            # Forward headers from the client to the target server
            for header in self.headers:
                if header not in ['Host', 'Content-Length']:
                    req.add_header(header, self.headers[header])
            
            # Handle POST data
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length) if content_length > 0 else None
            
            if method == "POST" and post_data:
                req.data = post_data

            # Open the connection to the target site
            opener = urllib.request.build_opener()
            try:
                response = opener.open(req, timeout=10)
            except urllib.error.HTTPError as e:
                # If the target site returns an error (e.g., 404), forward it
                self.send_response(e.code)
                for header, value in e.headers.items():
                    self.send_header(header, value)
                self.end_headers()
                self.wfile.write(e.read())
                return
            except Exception as e:
                logging.error(f"Error fetching {url}: {e}")
                self.send_error(502, f"Bad Gateway: {str(e)}")
                return

            # Read the response content
            content_type = response.headers.get('Content-Type', '')
            content = response.read()

            # Rewrite URLs in the content if it's HTML
            if 'text/html' in content_type:
                content = self.rewrite_html(content, url)
            elif 'text/css' in content_type:
                content = self.rewrite_css(content, url)
            
            # Send the response back to the client
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', str(len(content)))
            # Add CORS headers to allow the iframe to load this content
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', '*')
            self.end_headers()
            self.wfile.write(content)

        except Exception as e:
            logging.error(f"General Error: {e}")
            self.send_error(500, f"Internal Server Error: {str(e)}")

    def rewrite_html(self, html_bytes, base_url):
        # Decode HTML
        try:
            html = html_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return html_bytes

        # Replace all links to point to our proxy
        # We replace http:// and https:// with /http:// and /https://
        # This ensures that when the browser clicks a link, it sends the request to our local server
        
        # Regex to find all URLs in href, src, action, etc.
        # This is a simplified regex. For production, use an HTML parser like BeautifulSoup.
        
        # Pattern to match URLs in common attributes
        pattern = re.compile(r'(href|src|action|srcset|data-src|background)="([^"]+)"')
        
        def replace_url(match):
            attr = match.group(1)
            url = match.group(2)
            
            # Skip empty URLs or internal anchors
            if not url or url.startswith('#') or url.startswith('javascript:') or url.startswith('mailto:'):
                return match.group(0)
            
            # If it's a relative URL, make it absolute
            if not url.startswith('http://') and not url.startswith('https://'):
                url = urllib.parse.urljoin(base_url, url)
            
            # Rewrite to go through our proxy
            return f'{attr}="/{url}"'

        # Apply regex replacement
        rewritten_html = pattern.sub(replace_url, html)
        
        # Also fix CSS background images if they are inline styles
        # This is a more complex case, but we can try a simple regex
        pattern_css = re.compile(r'background-image\s*:\s*url\(["\']?([^"\')]+)["\']?\)')
        rewritten_html = pattern_css.sub(lambda m: f'background-image: url("/{m.group(1)}")', rewritten_html)

        return rewritten_html.encode('utf-8')

    def rewrite_css(self, css_bytes, base_url):
        try:
            css = css_bytes.decode('utf-8')
        except UnicodeDecodeError:
            return css_bytes
        
        # Rewrite URLs in CSS
        pattern = re.compile(r'url\(["\']?([^"\')]+)["\']?\)')
        
        def replace_css_url(match):
            url = match.group(1)
            if not url:
                return match.group(0)
            if url.startswith('http'):
                return f'url("/{url}")'
            else:
                # Relative URL
                absolute_url = urllib.parse.urljoin(base_url, url)
                return f'url("/{absolute_url}")'
        
        rewritten_css = pattern.sub(replace_css_url, css)
        return rewritten_css.encode('utf-8')

    def log_message(self, format, *args):
        logging.info(format % args)

def start_server():
    # Use ThreadingHTTPServer to handle multiple requests
    with socketserver.ThreadingTCPServer((HOST, PORT), ProxyHandler) as httpd:
        logging.info(f"Proxy server running on http://{HOST}:{PORT}")
        logging.info("Open http://{HOST}:{PORT}/ in your browser")
        httpd.serve_forever()

if __name__ == "__main__":
    start_server()
