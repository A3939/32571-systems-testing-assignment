"use strict";

document.querySelectorAll("[data-print]").forEach(button => {
  button.addEventListener("click", () => window.print());
});

const filters = document.querySelector("#filters");
if (filters) {
  const query = document.querySelector("#query");
  const status = document.querySelector("#status");
  const group = document.querySelector("#group");
  const cards = [...document.querySelectorAll("[data-scenario]")];
  const parameters = new URLSearchParams(window.location.search);
  query.value = parameters.get("q") || "";
  for (const [name, select] of [["status", status], ["group", group]]) {
    const value = parameters.get(name);
    if ([...select.options].some(option => option.value === value)) {
      select.value = value;
    }
  }

  function searchable(value) {
    return value.toLowerCase().replace(/[\s·_-]+/g, "");
  }

  function filter() {
    const search = searchable(query.value.trim());
    let count = 0;
    for (const card of cards) {
      const matches = searchable(card.textContent).includes(search)
        && (!status.value || card.dataset.status === status.value)
        && (!group.value || card.dataset.group === group.value);
      card.hidden = !matches;
      if (matches) count += 1;
    }
    document.querySelector("#visible").textContent = `${count} of ${cards.length} scenarios shown`;
    document.querySelector("#empty").hidden = count !== 0 || cards.length === 0;
  }

  filters.addEventListener("input", filter);
  filters.addEventListener("submit", event => event.preventDefault());
  filters.addEventListener("reset", () => requestAnimationFrame(filter));
  filter();
}

const imageDialog = document.querySelector("#image-dialog");
if (imageDialog) {
  const fullImage = document.querySelector("#full-image");
  document.querySelectorAll("[data-zoom]").forEach(button => {
    button.addEventListener("click", () => {
      const image = button.querySelector("img");
      fullImage.src = image.src;
      fullImage.alt = image.alt;
      document.querySelector("#image-title").textContent = image.alt;
      imageDialog.showModal();
    });
  });
  document.querySelector("#close-image").addEventListener("click", () => imageDialog.close());
  imageDialog.addEventListener("click", event => {
    if (event.target === imageDialog) {
      const bounds = imageDialog.getBoundingClientRect();
      if (event.clientX < bounds.left || event.clientX > bounds.right
          || event.clientY < bounds.top || event.clientY > bounds.bottom) {
        imageDialog.close();
      }
    }
  });
}
