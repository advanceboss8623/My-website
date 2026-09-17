function go() {
  let input = document.getElementById("url").value;
  let page = document.getElementById("page");

  if (!input.startsWith("http://") &&
      !input.startsWith("https://")) {
    input = "https://www.google.com/search?q=" +
            encodeURIComponent(input);
  }

  page.src = input;
}
