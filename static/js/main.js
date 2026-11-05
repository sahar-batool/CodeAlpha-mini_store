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

  // Hide success/error messages after a few seconds
  document.querySelectorAll(".message").forEach((message) => {
    setTimeout(() => message.remove(), 5000);
  });
});