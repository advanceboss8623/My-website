// --- CONFIGURATION ---
// Change this to your desired proxy URL if you have one.
// Currently using a public CORS proxy for demonstration.
const PROXY_URL = "https://api.allorigins.win/raw?url=";

let isProxyEnabled = false;

// --- PROXY LOGIC ---

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
    
    // Optional: Clear main content when switching
    document.querySelector('main').innerHTML = `
        <div class="google-logo">
            <span class="blue">G</span><span class="red">o</span><span class="yellow">o</span><span class="blue">g</span><span class="green">l</span><span class="red">e</span>
        </div>
        <form class="search-box" action="https://www.google.com/search" method="GET">
            <span>⌕</span>
            <input name="q" placeholder="Search Google" autocomplete="off">
            <button type="submit">Search</button>
        </form>
        <div class="shortcuts">
            <a href="https://www.youtube.com" onclick="loadViaProxy(event)">▶ YouTube</a>
            <a href="https://www.wikipedia.org" onclick="loadViaProxy(event)">W Wikipedia</a>
            <a href="https://github.com" onclick="loadViaProxy(event)">◆ GitHub</a>
        </div>
    `;
}

async function loadViaProxy(event) {
    event.preventDefault();
    const url = event.target.getAttribute('href');
    const mainContent = document.querySelector('main');
    
    // Show loading state
    mainContent.innerHTML = "<p>Loading via proxy...</p>";

    if (isProxyEnabled) {
        try {
            // Fetch via CORS Proxy
            const response = await fetch(PROXY_URL + encodeURIComponent(url));
            if (!response.ok) throw new Error("Network response was not ok");
            
            const html = await response.text();
            
            // Extract body content to keep our layout intact
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const bodyContent = doc.body.innerHTML;
            
            mainContent.innerHTML = `
                <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
                    <h2>Proxy Loaded: ${url}</h2>
                    <div>${bodyContent}</div>
                    <button onclick="location.reload()" style="margin-top:20px;">Back</button>
                </div>
            `;
        } catch (error) {
            mainContent.innerHTML = `<p>Error loading proxy: ${error.message}</p>`;
        }
    } else {
        // Direct navigation if proxy is off
        window.location.href = url;
    }
}

// Optional: Intercept form submissions if you want to proxy searches too
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        if (isProxyEnabled && this.action.includes('google.com')) {
            e.preventDefault();
            const query = this.elements['q'].value;
            const searchUrl = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
            
            loadViaProxy({
                preventDefault: () => {},
                target: { getAttribute: (attr) => searchUrl }
            });
        }
    });
});
