function go() {
    const input = document.getElementById("url").value.trim();

    if (!input) {
        return;
    }

    // If it looks like a website address, open it.
    if (input.includes(".") && !input.includes(" ")) {
        let url = input;

        if (!url.startsWith("http://") && !url.startsWith("https://")) {
            url = "https://" + url;
        }

        window.location.href = url;
    } 
    
    // Otherwise, search Google.
    else {
        window.location.href =
            "https://www.google.com/search?q=" +
            encodeURIComponent(input);
    }
}
