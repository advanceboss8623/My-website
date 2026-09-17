function go() {
  let input = document.getElementById("url").value.trim();

  if (!input.startsWith("http://") &&
      !input.startsWith("https://")) {
    input = "https://www.google.com/search?q=" +
            encodeURIComponent(input);
  }

  window.location.href = input;
}
