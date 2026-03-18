(() => {
  const TOKEN_KEY = "hotel_admin_token";
  const USER_KEY = "hotel_admin_user";
  const API_BASE_KEY = "hotel_api_base";

  const form = document.getElementById("admin-login-form");
  const message = document.getElementById("login-message");
  const baseInput = document.getElementById("api-base");

  const savedBase = localStorage.getItem(API_BASE_KEY);
  if (savedBase) {
    baseInput.value = savedBase;
  }

  function showMessage(kind, text) {
    message.classList.remove("d-none", "alert-success", "alert-danger");
    message.classList.add(kind === "error" ? "alert-danger" : "alert-success");
    message.textContent = text;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const apiBase = baseInput.value.trim().replace(/\/$/, "");
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!apiBase || !email || !password) {
      showMessage("error", "Please fill all fields.");
      return;
    }

    try {
      const response = await fetch(`${apiBase}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || "Login failed");
      }

      const role = String(data.user?.usertype || "").toLowerCase();
      if (role !== "admin") {
        throw new Error("Only admin users can access this panel.");
      }

      localStorage.setItem(TOKEN_KEY, data.access_token);
      localStorage.setItem(USER_KEY, JSON.stringify(data.user));
      localStorage.setItem(API_BASE_KEY, apiBase);

      window.location.href = "index.html";
    } catch (error) {
      showMessage("error", error.message || "Unable to sign in.");
    }
  });
})();
