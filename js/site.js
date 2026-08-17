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
const heroSection = document.querySelector("[data-hero-section]");

if (revealBrandNav && revealBrandLink && heroSection) {
  let brandIsVisible = null;

  const updateBrandVisibility = () => {
    const heroHasPassed = heroSection.getBoundingClientRect().bottom <= 0;

    if (heroHasPassed === brandIsVisible) return;

    brandIsVisible = heroHasPassed;
    revealBrandLink.classList.toggle("is-visible", heroHasPassed);
    revealBrandLink.setAttribute("aria-hidden", String(!heroHasPassed));
    revealBrandLink.tabIndex = heroHasPassed ? 0 : -1;
  };

  updateBrandVisibility();
  window.addEventListener("scroll", updateBrandVisibility, { passive: true });
  window.addEventListener("resize", updateBrandVisibility);
}
