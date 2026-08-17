document.querySelectorAll("[data-email-link]").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();

    const localPart = "ilagnahthsaniva".split("").reverse().join("");
    const domain = "moc.liamg".split("").reverse().join("");

    window.location.href = `mailto:${localPart}@${domain}`;
  });
});
