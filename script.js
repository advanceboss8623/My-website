function openWebsite(event) {
    event.preventDefault();

    const input = document.getElementById("address").value.trim();

    if (!input) return;

    let url;

    if (input.includes(" ") || !input.includes(".")) {
        url = "https://www.google.com/search?q=" +
              encodeURIComponent(input);
    } else {
        url = input.startsWith("http://") || input.startsWith("https://")
            ? input
            : "https://" + input;
    }

    window.location.href = url;
}

function searchGoogle(event) {
    event.preventDefault();

    const search = document.getElementById("googleSearch").value.trim();

    if (!search) return;

    window.location.href =
        "https://www.google.com/search?q=" +
        encodeURIComponent(search);
}
