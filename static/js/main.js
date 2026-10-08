/**
 * DadBods Main JavaScript
 * Premium Interactive Features:
 * 1. Sticky Navigation & Scroll Progress Indicator
 * 2. Custom Desktop Cursor with Magnetic Hover State
 * 3. IntersectionObserver Scroll Reveal Animations
 * 4. Full-Featured Touch & Keyboard Lightbox
 * 5. Gentle Desktop Parallax
 * 6. Mobile Drawer Navigation
 */

document.addEventListener("DOMContentLoaded", () => {
  const isTouchDevice = () => window.matchMedia("(pointer: coarse)").matches || "ontouchstart" in window;

  /* ==========================================================================
     1. SCROLL PROGRESS BAR & STICKY NAVBAR
     ========================================================================== */
  const scrollProgressBar = document.getElementById("scrollProgressBar");
  const siteNav = document.querySelector(".site-nav");

  function handleScroll() {
    const scrollY = window.scrollY || window.pageYOffset;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;

    // Progress Bar
    if (scrollProgressBar && docHeight > 0) {
      const scrollPercent = Math.min(100, Math.max(0, (scrollY / docHeight) * 100));
      scrollProgressBar.style.width = `${scrollPercent}%`;
    }

    // Sticky Nav background change
    if (siteNav) {
      if (scrollY > 40) {
        siteNav.classList.add("scrolled");
      } else {
        siteNav.classList.remove("scrolled");
      }
    }

    // Gentle Parallax for Hero & Story Images on Desktop
    if (!isTouchDevice() && window.innerWidth >= 992) {
      const heroBg = document.getElementById("heroBgMedia");
      if (heroBg && scrollY < window.innerHeight) {
        heroBg.style.transform = `translate3d(0, ${scrollY * 0.22}px, 0)`;
      }

      // Parallax story images
      document.querySelectorAll(".parallax-target").forEach((img) => {
        const rect = img.getBoundingClientRect();
        if (rect.top < window.innerHeight && rect.bottom > 0) {
          const offset = (window.innerHeight - rect.top) * 0.06;
          img.style.transform = `translate3d(0, ${offset}px, 0)`;
        }
      });
    }
  }

  window.addEventListener("scroll", handleScroll, { passive: true });
  handleScroll(); // Initial run


  /* ==========================================================================
     3. INTERSECTION OBSERVER SCROLL REVEAL ANIMATIONS
     ========================================================================== */
  const revealElements = document.querySelectorAll(".reveal-on-scroll");
  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const delay = entry.target.getAttribute("data-delay") || 0;
            if (delay > 0) {
              setTimeout(() => {
                entry.target.classList.add("is-revealed");
              }, parseInt(delay, 10));
            } else {
              entry.target.classList.add("is-revealed");
            }
            observer.unobserve(entry.target);
          }
        });
      },
      {
        rootMargin: "0px 0px -60px 0px",
        threshold: 0.1,
      }
    );

    revealElements.forEach((el) => revealObserver.observe(el));
  } else {
    // Fallback for older browsers
    revealElements.forEach((el) => el.classList.add("is-revealed"));
  }

  /* ==========================================================================
     4. HERO SCROLL-TO-EXPLORE SMOOTH SCROLL
     ========================================================================== */
  const scrollIndicator = document.querySelector(".hero-scroll-indicator");
  scrollIndicator?.addEventListener("click", (e) => {
    e.preventDefault();
    const target = document.getElementById("statementSection");
    if (target) {
      target.scrollIntoView({ behavior: "smooth" });
    }
  });

  /* ==========================================================================
     5. ENHANCED FULL-FEATURED LIGHTBOX (NAV, KEYBOARD, SWIPE)
     ========================================================================== */
  const lightbox = document.getElementById("globalLightbox");
  const lightboxImg = document.getElementById("lightboxImg");
  const lightboxClose = document.getElementById("lightboxClose");
  const lightboxPrev = document.getElementById("lightboxPrev");
  const lightboxNext = document.getElementById("lightboxNext");
  const lightboxCounter = document.getElementById("lightboxCounter");

  const triggers = Array.from(document.querySelectorAll(".js-lightbox-trigger"));
  let currentIndex = 0;

  function openLightbox(index) {
    if (!lightbox || !lightboxImg || triggers.length === 0) return;
    currentIndex = (index + triggers.length) % triggers.length;
    const trigger = triggers[currentIndex];
    const src = trigger.getAttribute("data-img") || trigger.querySelector("img")?.src;

    if (src) {
      lightboxImg.src = src;
      lightbox.classList.add("active");
      document.body.style.overflow = "hidden";

      if (lightboxCounter) {
        lightboxCounter.textContent = `RESULT ${currentIndex + 1} / ${triggers.length}`;
      }
    }
  }

  function closeLightbox() {
    if (lightbox) {
      lightbox.classList.remove("active");
      document.body.style.overflow = "";
    }
  }

  function nextImage() {
    openLightbox(currentIndex + 1);
  }

  function prevImage() {
    openLightbox(currentIndex - 1);
  }

  triggers.forEach((trigger, idx) => {
    trigger.addEventListener("click", () => openLightbox(idx));
  });

  lightboxClose?.addEventListener("click", closeLightbox);
  lightboxNext?.addEventListener("click", nextImage);
  lightboxPrev?.addEventListener("click", prevImage);

  lightbox?.addEventListener("click", (e) => {
    if (e.target === lightbox) {
      closeLightbox();
    }
  });

  // Keyboard navigation
  document.addEventListener("keydown", (e) => {
    if (!lightbox?.classList.contains("active")) return;
    if (e.key === "Escape") closeLightbox();
    if (e.key === "ArrowRight") nextImage();
    if (e.key === "ArrowLeft") prevImage();
  });

  // Mobile Touch Swipe for Lightbox
  let touchStartX = 0;
  let touchEndX = 0;

  lightbox?.addEventListener(
    "touchstart",
    (e) => {
      touchStartX = e.changedTouches[0].screenX;
    },
    { passive: true }
  );

  lightbox?.addEventListener(
    "touchend",
    (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    },
    { passive: true }
  );

  function handleSwipe() {
    const swipeThreshold = 50;
    if (touchEndX < touchStartX - swipeThreshold) {
      nextImage(); // Swipe left -> Next
    }
    if (touchEndX > touchStartX + swipeThreshold) {
      prevImage(); // Swipe right -> Prev
    }
  }

  /* ==========================================================================
     6. MOBILE NAV DRAWER TOGGLE
     ========================================================================== */
  const navToggle = document.getElementById("navToggle");
  const mobileDrawer = document.getElementById("mobileDrawer");
  const mobileOverlay = document.getElementById("mobileOverlay");

  function toggleMobileNav() {
    const isOpen = mobileDrawer?.classList.contains("open");
    if (isOpen) {
      mobileDrawer?.classList.remove("open");
      mobileOverlay?.classList.remove("open");
      document.body.style.overflow = "";
    } else {
      mobileDrawer?.classList.add("open");
      mobileOverlay?.classList.add("open");
      document.body.style.overflow = "hidden";
    }
  }

  navToggle?.addEventListener("click", toggleMobileNav);
  mobileOverlay?.addEventListener("click", toggleMobileNav);

  document.querySelectorAll(".mobile-nav-links .nav-link").forEach((link) => {
    link.addEventListener("click", () => {
      mobileDrawer?.classList.remove("open");
      mobileOverlay?.classList.remove("open");
      document.body.style.overflow = "";
    });
  });
});
