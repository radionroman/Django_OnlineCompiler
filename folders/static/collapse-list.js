window.addEventListener("load", () => {
  for (let i of document.querySelectorAll(".collapse ul")) {
    let tog = document.createElement("div");
    tog.innerHTML = i.previousSibling.textContent;
    tog.className = "toggle";
    tog.onclick = () => tog.classList.toggle("show");
    i.parentElement.removeChild(i.previousSibling);
    i.parentElement.insertBefore(tog, i);
  }
});