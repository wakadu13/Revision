// Import de sets de QCM : glisser-déposer des fichiers .json sur la zone (ou
// clic pour les choisir). Le formulaire est envoyé dès que des fichiers sont
// choisis ; le serveur valide chaque set et affiche le résultat.
(function () {
  const form = document.querySelector("[data-quiz-import]");
  if (!form) return;
  const zone = form.querySelector("[data-dropzone]");
  const input = form.querySelector("[data-import-files]");

  function send(files) {
    const json = Array.from(files).filter((f) => f.name.toLowerCase().endsWith(".json"));
    if (!json.length) {
      alert("Seuls les fichiers .json sont acceptés.");
      return;
    }
    const transfer = new DataTransfer();
    json.forEach((f) => transfer.items.add(f));
    input.files = transfer.files;
    zone.classList.add("is-sending");
    zone.querySelector("b").textContent = "Import de " + json.length + " fichier" + (json.length > 1 ? "s" : "") + "…";
    form.submit();
  }

  input.addEventListener("change", () => { if (input.files.length) send(input.files); });

  ["dragenter", "dragover"].forEach((type) => zone.addEventListener(type, (e) => {
    e.preventDefault();
    zone.classList.add("is-over");
  }));
  ["dragleave", "drop"].forEach((type) => zone.addEventListener(type, () => zone.classList.remove("is-over")));
  zone.addEventListener("drop", (e) => {
    e.preventDefault();
    if (e.dataTransfer && e.dataTransfer.files.length) send(e.dataTransfer.files);
  });

  // Un fichier lâché à côté de la zone ne doit pas faire quitter la page.
  window.addEventListener("dragover", (e) => e.preventDefault());
  window.addEventListener("drop", (e) => e.preventDefault());
})();
