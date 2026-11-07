document.addEventListener("DOMContentLoaded", () => {
  const countEl = document.getElementById("cart-count");
  const toast = document.getElementById("toast");
  let toastTimer;

  function showToast(text) {
    toast.textContent = text;
    toast.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove("show"), 2500);
  }

  // Add to cart without reloading the page
  const form = document.querySelector(".add-form");
  if (form) {
    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const button = form.querySelector("button");
      button.disabled = true;

      try {
        const response = await fetch(form.action, {
          method: "POST",
          headers: { "X-Requested-With": "XMLHttpRequest" },
          body: new FormData(form),
        });
        if (!response.ok) throw new Error("Request failed");

        const data = await response.json();
        countEl.textContent = data.cart_count;
        showToast(data.message);
      } catch (error) {
        form.submit(); // fall back to a normal form post
      } finally {
        button.disabled = false;
      }
    });
  }
    // Mobile menu
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open);
      toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
  }

    // Hero: rotating category word
  const rotator = document.querySelector(".rotator");
  if (rotator) {
    const words = (rotator.dataset.words || "").split(",").map((w) => w.trim()).filter(Boolean);
    if (words.length > 1) {
      rotator.textContent = "";
      const spans = words.map((word, i) => {
        const span = document.createElement("span");
        span.textContent = word;
        if (i === 0) span.classList.add("is-active");
        rotator.appendChild(span);
        return span;
      });

      if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        let current = 0;
        setInterval(() => {
          const leaving = spans[current];
          current = (current + 1) % spans.length;
          leaving.classList.remove("is-active");
          leaving.classList.add("is-leaving");
          spans[current].classList.remove("is-leaving");
          spans[current].classList.add("is-active");
          setTimeout(() => leaving.classList.remove("is-leaving"), 700);
        }, 2400);
      }
    }
  }

    // Hero collage: each photo card cycles through its own products
  const heroCards = document.querySelectorAll(".hero-card[data-rotate]");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (heroCards.length && !reduceMotion) {
    const heroArt = document.querySelector(".hero-art");
    let paused = false;
    heroArt.addEventListener("mouseenter", () => (paused = true));
    heroArt.addEventListener("mouseleave", () => (paused = false));
    heroArt.addEventListener("focusin", () => (paused = true));
    heroArt.addEventListener("focusout", () => (paused = false));

    heroCards.forEach((card, index) => {
      const slides = card.querySelectorAll(".hero-slide");
      if (slides.length < 2) return;
      let current = 0;

      const show = (next) => {
        slides[current].classList.remove("is-active");
        slides[current].setAttribute("aria-hidden", "true");
        slides[current].tabIndex = -1;
        current = next;
        slides[current].classList.add("is-active");
        slides[current].removeAttribute("aria-hidden");
        slides[current].removeAttribute("tabindex");
      };

      // start after the entrance animation, and offset each card
      setTimeout(() => {
        setInterval(() => {
          if (paused || document.hidden) return;
          show((current + 1) % slides.length);
        }, 2000);
      }, 1800 + index * 650);
    });
  }

    // Quantity steppers (+ / -). Forms marked data-autosubmit save on every click.
  document.querySelectorAll("[data-qty]").forEach((box) => {
    const input = box.querySelector("input");
    box.querySelectorAll("[data-step]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const min = input.min === "" ? 0 : Number(input.min);
        const max = input.max === "" ? Infinity : Number(input.max);
        const next = (Number(input.value) || min) + Number(btn.dataset.step);
        const clamped = Math.min(max, Math.max(min, next));
        if (clamped === Number(input.value)) return;
        input.value = clamped;
        const form = input.closest("form[data-autosubmit]");
        if (form) form.requestSubmit();
      });
    });
  });

  // Hide success/error messages after a few seconds
  document.querySelectorAll(".message").forEach((message) => {
    setTimeout(() => message.remove(), 5000);
  });
});