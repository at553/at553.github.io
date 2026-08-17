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
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let brandIsVisible = null;
  let updateFrame = null;

  const updateBrandOpacity = () => {
    const distancePastHero = Math.max(
      0,
      -heroSection.getBoundingClientRect().bottom,
    );
    const fadeDistance = Math.min(
      Math.max(window.innerHeight * 0.3, 200),
      320,
    );
    const fadeProgress = reducedMotion.matches
      ? Number(distancePastHero > 0)
      : Math.min(distancePastHero / fadeDistance, 1);
    const brandShouldBeVisible = fadeProgress > 0;

    revealBrandLink.style.setProperty("--brand-opacity", String(fadeProgress));

    if (brandShouldBeVisible === brandIsVisible) return;

    brandIsVisible = brandShouldBeVisible;
    revealBrandLink.classList.toggle("is-visible", brandShouldBeVisible);
    revealBrandLink.setAttribute("aria-hidden", String(!brandShouldBeVisible));
    revealBrandLink.tabIndex = brandShouldBeVisible ? 0 : -1;
  };

  const requestBrandUpdate = () => {
    if (updateFrame !== null) return;

    updateFrame = window.requestAnimationFrame(() => {
      updateFrame = null;
      updateBrandOpacity();
    });
  };

  updateBrandOpacity();
  window.addEventListener("scroll", requestBrandUpdate, { passive: true });
  window.addEventListener("resize", requestBrandUpdate);
  reducedMotion.addEventListener("change", requestBrandUpdate);
}
