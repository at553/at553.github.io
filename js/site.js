document.querySelectorAll("[data-email-link]").forEach((link) => {
  link.addEventListener("click", (event) => {
    event.preventDefault();

    const localPart = "ilagnahthsaniva".split("").reverse().join("");
    const domain = "moc.liamg".split("").reverse().join("");

    window.location.href = `mailto:${localPart}@${domain}`;
  });
});

const revealBrandNav = document.querySelector("[data-reveal-brand]");
const revealBrandLink = revealBrandNav?.querySelector(".brand");
const heroName = document.querySelector("[data-hero-name]");

if (revealBrandNav && revealBrandLink && heroName) {
  let brandIsVisible = null;

  const updateBrandVisibility = () => {
    const nameHasPassed =
      heroName.getBoundingClientRect().bottom <=
      revealBrandNav.getBoundingClientRect().bottom;

    if (nameHasPassed === brandIsVisible) return;

    brandIsVisible = nameHasPassed;
    revealBrandLink.classList.toggle("is-visible", nameHasPassed);
    revealBrandLink.setAttribute("aria-hidden", String(!nameHasPassed));
    revealBrandLink.tabIndex = nameHasPassed ? 0 : -1;
  };

  updateBrandVisibility();
  window.addEventListener("scroll", updateBrandVisibility, { passive: true });
  window.addEventListener("resize", updateBrandVisibility);
}
