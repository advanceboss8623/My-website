function searchGoogle(event) {
    event.preventDefault();

    const search = document.getElementById("googleSearch").value.trim();

    if (!search) {
        return;
    }

    const url =
        "https://www.google.com/search?q=" +
        encodeURIComponent(search);

    window.location.href = url;
}


function go(event) {
    event.preventDefault();

    const input = document.getElementById("address").value.trim();

    if (!input) {
        return;
    }

    let url;

    // Open a website if it looks like a URL
    if (
        input.startsWith("http://") ||
        input.startsWith("https://")
    ) {
        url = input;
    }

    else if (
        input.includes(".") &&
        !input.includes(" ")
    ) {
        url = "https://" + input;
    }

    // Otherwise search Google
    else {
        url =
            "https://www.google.com/search?q=" +
            encodeURIComponent(input);
    }

    window.location.href = url;
}


function openSite(url) {
    window.location.href = url;
}


function goBack() {
    window.history.back();
}


function goForward() {
    window.history.forward();
}


function reloadPage() {
    window.location.reload();
}


function goHome() {
    window.location.href = window.location.pathname;
}


function newTab() {
    window.location.href = window.location.pathname;
}


function bookmarkPage() {
    alert("Bookmark saved!");
}


function toggleMenu() {
    const menu = document.getElementById("menu");

    menu.classList.toggle("show");
}


function toggleDarkMode() {
    document.body.classList.toggle("dark");

    const isDark =
        document.body.classList.contains("dark");

    localStorage.setItem("darkMode", isDark);
}


function showAbout() {
    alert(
        "My Chrome\n\n" +
        "A Chrome-style browser project."
    );
}


// Remember dark mode
window.addEventListener("load", function () {

    const darkMode =
        localStorage.getItem("darkMode");

    if (darkMode === "true") {
        document.body.classList.add("dark");
    }

});
