const API_KEY = "YOUR_API_KEY"; // Replace with your actual key

async function loadViaProxy(event) {
    event.preventDefault();
    const url = event.target.getAttribute('href');
    const mainContent = document.querySelector('main');

    if (isProxyEnabled) {
        try {
            // Construct the proxy URL
            const proxyUrl = `https://api.scraperapi.com/?api_key=${API_KEY}&url=${encodeURIComponent(url)}`;

            // Redirect the browser to the proxy URL
            // This allows the proxy to handle the page rendering (including JS)
            window.location.href = proxyUrl;
        } catch (error) {
            mainContent.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        }
    } else {
        // If proxy is off, navigate directly
        window.location.href = url;
    }
}

// Handle Search Form Submission
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (isProxyEnabled) {
            e.preventDefault();
            const query = this.elements['q'].value;
            const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
            
            // Redirect to the search URL via proxy
            window.location.href = `https://api.scraperapi.com/?api_key=${API_KEY}&url=${encodeURIComponent(searchUrl)}`;
        }
    });
});

// Toggle Proxy Function
function toggleProxy() {
    isProxyEnabled = !isProxyEnabled;
    const btn = document.getElementById('proxyBtn');
    
    if (isProxyEnabled) {
        btn.innerText = "🌐 Proxy: ON";
        btn.style.background = "#e0ffe0";
    } else {
        btn.innerText = "🌐 Proxy: OFF";
        btn.style.background = "#f0f0f0";
    }
    
    // Reset the main content when toggling
    location.reload();
}
