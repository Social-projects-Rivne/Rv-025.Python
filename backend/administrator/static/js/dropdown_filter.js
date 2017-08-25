var dropdown = document.querySelector(".dropdown-filter");

dropdown.addEventListener("change", function (event) {
  window.location = window.location.pathname + event.target.value;
});
