(() => {
  const TOKEN_KEY = "hotel_admin_token";
  const USER_KEY = "hotel_admin_user";
  const API_BASE_KEY = "hotel_api_base";

  const token = localStorage.getItem(TOKEN_KEY);
  const apiBase = (localStorage.getItem(API_BASE_KEY) || "http://localhost:8000").replace(/\/$/, "");

  if (!token) {
    window.location.href = "login.html";
    return;
  }

  let apiOrigin = "";
  try {
    apiOrigin = new URL(apiBase).origin;
  } catch {
    apiOrigin = "http://localhost:8000";
  }

  const dashboardMessage = document.getElementById("dashboard-message");
  const roomForm = document.getElementById("room-form");
  const galleryForm = document.getElementById("gallery-form");

  function showMessage(kind, text) {
    dashboardMessage.classList.remove("d-none", "alert-success", "alert-danger");
    dashboardMessage.classList.add(kind === "error" ? "alert-danger" : "alert-success");
    dashboardMessage.textContent = text;
  }

  function clearMessage() {
    dashboardMessage.classList.add("d-none");
  }

  function toDisplayImage(src) {
    if (!src) {
      return "";
    }
    if (src.startsWith("http://") || src.startsWith("https://")) {
      return src;
    }
    if (src.startsWith("/")) {
      return `${apiOrigin}${src}`;
    }
    return `${apiOrigin}/media/${src.replace(/^\/+/, "")}`;
  }

  async function api(path, options = {}) {
    const headers = new Headers(options.headers || {});
    if (!headers.has("Authorization")) {
      headers.set("Authorization", `Bearer ${token}`);
    }

    const isFormData = options.body instanceof FormData;
    if (!isFormData && !headers.has("Content-Type") && options.body) {
      headers.set("Content-Type", "application/json");
    }

    const response = await fetch(`${apiBase}${path}`, { ...options, headers });

    if (response.status === 401 || response.status === 403) {
      localStorage.removeItem(TOKEN_KEY);
      window.location.href = "login.html";
      throw new Error("Session expired. Please login again.");
    }

    if (response.status === 204) {
      return null;
    }

    const data = await response.json().catch(() => ({}));
    if (!response.ok) {
      throw new Error(data.detail || data.message || `Request failed (${response.status})`);
    }
    return data;
  }

  function setAdminUserLabel() {
    const label = document.getElementById("admin-user-label");
    const userRaw = localStorage.getItem(USER_KEY);
    if (!userRaw) {
      return;
    }

    try {
      const user = JSON.parse(userRaw);
      label.textContent = `${user.name || "Admin"} (${user.email || ""})`;
    } catch {
      label.textContent = "Admin";
    }
  }

  function bindTopActions() {
    document.getElementById("logout-btn").addEventListener("click", () => {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
      window.location.href = "login.html";
    });
  }

  async function loadStats() {
    const data = await api("/api/admin/stats");
    document.getElementById("stat-users").textContent = data.total_users ?? 0;
    document.getElementById("stat-rooms").textContent = data.total_rooms ?? 0;
    document.getElementById("stat-bookings").textContent = data.total_bookings ?? 0;
    document.getElementById("stat-income").textContent = `$${Number(data.total_income || 0).toFixed(2)}`;
  }

  function resetRoomForm() {
    document.getElementById("room-id").value = "";
    document.getElementById("room-title").value = "";
    document.getElementById("room-description").value = "";
    document.getElementById("room-price").value = "";
    document.getElementById("room-type").value = "";
    document.getElementById("room-wifi").value = "yes";
    document.getElementById("room-image-url").value = "";
    document.getElementById("room-image-file").value = "";
  }

  function roomFormData() {
    const data = new FormData();
    data.append("room_title", document.getElementById("room-title").value.trim());
    data.append("description", document.getElementById("room-description").value.trim());
    data.append("price", document.getElementById("room-price").value.trim());
    data.append("room_type", document.getElementById("room-type").value.trim());
    data.append("wifi", document.getElementById("room-wifi").value);

    const urlVal = document.getElementById("room-image-url").value.trim();
    const fileInput = document.getElementById("room-image-file");

    if (urlVal) {
      data.append("image_url", urlVal);
    }
    if (fileInput.files[0]) {
      data.append("image_file", fileInput.files[0]);
    }

    return data;
  }

  async function loadRooms() {
    const tableBody = document.querySelector("#rooms-table tbody");
    const data = await api("/api/admin/rooms");

    tableBody.innerHTML = "";
    for (const room of data.rooms || []) {
      const tr = document.createElement("tr");
      const image = toDisplayImage(room.image || room.image_raw || "");
      tr.innerHTML = `
        <td>${room.id}</td>
        <td>${room.room_title || ""}</td>
        <td>${room.price || ""}</td>
        <td>${room.room_type || ""}</td>
        <td>${image ? `<img src="${image}" alt="room" class="room-thumb">` : "-"}</td>
        <td>
          <button class="btn btn-sm btn-outline-primary mr-1" data-action="edit-room" data-id="${room.id}">Edit</button>
          <button class="btn btn-sm btn-outline-danger" data-action="delete-room" data-id="${room.id}">Delete</button>
        </td>
      `;
      tr.dataset.room = JSON.stringify(room);
      tableBody.appendChild(tr);
    }
  }

  async function loadGallery() {
    const grid = document.getElementById("gallery-grid");
    const data = await api("/api/admin/gallery");

    grid.innerHTML = "";
    for (const item of data.gallery || []) {
      const image = toDisplayImage(item.image || item.image_raw || "");
      const card = document.createElement("article");
      card.className = "gallery-item";
      card.innerHTML = `
        ${image ? `<img src="${image}" alt="gallery-${item.id}">` : "<div class='p-2 text-muted small'>No image</div>"}
        <div class="meta d-flex justify-content-between align-items-center">
          <small class="text-muted">#${item.id}</small>
          <button class="btn btn-sm btn-outline-danger" data-action="delete-gallery" data-id="${item.id}">Delete</button>
        </div>
      `;
      grid.appendChild(card);
    }
  }

  async function loadBookings() {
    const tableBody = document.querySelector("#bookings-table tbody");
    const data = await api("/api/admin/bookings");

    tableBody.innerHTML = "";
    const statuses = ["waiting", "approved", "rejected", "canceled", "paid"];

    for (const booking of data.bookings || []) {
      const row = document.createElement("tr");
      const currentStatus = String(booking.status || "waiting").toLowerCase();
      const statusOptions = statuses
        .map((value) => `<option value="${value}" ${value === currentStatus ? "selected" : ""}>${value}</option>`)
        .join("");

      row.innerHTML = `
        <td>${booking.id}</td>
        <td>
          <strong>${booking.name || ""}</strong>
          <div class="small text-muted">${booking.email || ""}</div>
        </td>
        <td>${booking.room_title || booking.room_id || ""}</td>
        <td>${booking.start_date || ""} - ${booking.end_date || ""}</td>
        <td>
          <select class="form-control form-control-sm" data-role="status-select" data-id="${booking.id}">
            ${statusOptions}
          </select>
        </td>
        <td>${booking.total_price ?? ""}</td>
        <td>
          <button class="btn btn-sm btn-outline-primary mr-1" data-action="update-booking" data-id="${booking.id}">Save</button>
          <button class="btn btn-sm btn-outline-danger" data-action="delete-booking" data-id="${booking.id}">Delete</button>
        </td>
      `;
      tableBody.appendChild(row);
    }
  }

  async function loadUsers() {
    const tableBody = document.querySelector("#users-table tbody");
    const data = await api("/api/admin/users");

    tableBody.innerHTML = "";
    for (const user of data.users || []) {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${user.id}</td>
        <td>${user.name || ""}</td>
        <td>${user.email || ""}</td>
        <td>${user.phone || ""}</td>
        <td><span class="badge badge-secondary">${user.usertype || "user"}</span></td>
      `;
      tableBody.appendChild(row);
    }
  }

  function bindRoomActions() {
    roomForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      clearMessage();

      const roomId = document.getElementById("room-id").value;
      const payload = roomFormData();

      try {
        if (!document.getElementById("room-title").value.trim()) {
          throw new Error("Room title is required.");
        }

        if (roomId) {
          await api(`/api/admin/rooms/${roomId}`, { method: "PUT", body: payload });
          showMessage("success", "Room updated.");
        } else {
          await api("/api/admin/rooms", { method: "POST", body: payload });
          showMessage("success", "Room created.");
        }

        resetRoomForm();
        await Promise.all([loadRooms(), loadStats()]);
      } catch (error) {
        showMessage("error", error.message || "Unable to save room.");
      }
    });

    document.getElementById("room-form-reset").addEventListener("click", resetRoomForm);

    document.getElementById("refresh-rooms").addEventListener("click", async () => {
      try {
        clearMessage();
        await loadRooms();
      } catch (error) {
        showMessage("error", error.message);
      }
    });

    document.querySelector("#rooms-table tbody").addEventListener("click", async (event) => {
      const btn = event.target.closest("button[data-action]");
      if (!btn) {
        return;
      }

      const action = btn.dataset.action;
      const id = btn.dataset.id;

      try {
        if (action === "delete-room") {
          if (!window.confirm("Delete this room?")) {
            return;
          }
          await api(`/api/admin/rooms/${id}`, { method: "DELETE" });
          showMessage("success", "Room deleted.");
          await Promise.all([loadRooms(), loadStats()]);
        }

        if (action === "edit-room") {
          const row = btn.closest("tr");
          const room = JSON.parse(row.dataset.room || "{}");
          document.getElementById("room-id").value = room.id || "";
          document.getElementById("room-title").value = room.room_title || "";
          document.getElementById("room-description").value = room.description || "";
          document.getElementById("room-price").value = room.price || "";
          document.getElementById("room-type").value = room.room_type || "";
          document.getElementById("room-wifi").value = room.wifi || "yes";
          document.getElementById("room-image-url").value = room.image_raw || "";
          document.getElementById("room-image-file").value = "";
          window.scrollTo({ top: 0, behavior: "smooth" });
        }
      } catch (error) {
        showMessage("error", error.message || "Room action failed.");
      }
    });
  }

  function bindGalleryActions() {
    galleryForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      clearMessage();

      const urlVal = document.getElementById("gallery-image-url").value.trim();
      const fileInput = document.getElementById("gallery-image-file");

      if (!urlVal && !fileInput.files[0]) {
        showMessage("error", "Provide an image URL or choose an image file.");
        return;
      }

      const formData = new FormData();
      if (urlVal) {
        formData.append("image_url", urlVal);
      }
      if (fileInput.files[0]) {
        formData.append("image_file", fileInput.files[0]);
      }

      try {
        await api("/api/admin/gallery", { method: "POST", body: formData });
        showMessage("success", "Gallery item added.");
        galleryForm.reset();
        await loadGallery();
      } catch (error) {
        showMessage("error", error.message || "Unable to add gallery image.");
      }
    });

    document.getElementById("refresh-gallery").addEventListener("click", async () => {
      try {
        clearMessage();
        await loadGallery();
      } catch (error) {
        showMessage("error", error.message);
      }
    });

    document.getElementById("gallery-grid").addEventListener("click", async (event) => {
      const btn = event.target.closest("button[data-action='delete-gallery']");
      if (!btn) {
        return;
      }

      const id = btn.dataset.id;
      if (!window.confirm("Delete this gallery image?")) {
        return;
      }

      try {
        await api(`/api/admin/gallery/${id}`, { method: "DELETE" });
        showMessage("success", "Gallery image deleted.");
        await loadGallery();
      } catch (error) {
        showMessage("error", error.message || "Unable to delete gallery image.");
      }
    });
  }

  function bindBookingActions() {
    document.getElementById("refresh-bookings").addEventListener("click", async () => {
      try {
        clearMessage();
        await loadBookings();
      } catch (error) {
        showMessage("error", error.message);
      }
    });

    document.querySelector("#bookings-table tbody").addEventListener("click", async (event) => {
      const btn = event.target.closest("button[data-action]");
      if (!btn) {
        return;
      }

      const bookingId = btn.dataset.id;
      const action = btn.dataset.action;

      try {
        if (action === "delete-booking") {
          if (!window.confirm("Delete this booking?")) {
            return;
          }
          await api(`/api/admin/bookings/${bookingId}`, { method: "DELETE" });
          showMessage("success", "Booking deleted.");
          await Promise.all([loadBookings(), loadStats()]);
          return;
        }

        if (action === "update-booking") {
          const select = document.querySelector(`select[data-role='status-select'][data-id='${bookingId}']`);
          await api(`/api/admin/bookings/${bookingId}/status`, {
            method: "PATCH",
            body: JSON.stringify({ status: select.value }),
          });
          showMessage("success", "Booking status updated.");
          await Promise.all([loadBookings(), loadStats()]);
        }
      } catch (error) {
        showMessage("error", error.message || "Booking action failed.");
      }
    });
  }

  function bindUserActions() {
    document.getElementById("refresh-users").addEventListener("click", async () => {
      try {
        clearMessage();
        await loadUsers();
      } catch (error) {
        showMessage("error", error.message);
      }
    });
  }

  async function bootstrap() {
    setAdminUserLabel();
    bindTopActions();
    bindRoomActions();
    bindGalleryActions();
    bindBookingActions();
    bindUserActions();

    try {
      await Promise.all([loadStats(), loadRooms(), loadGallery(), loadBookings(), loadUsers()]);
    } catch (error) {
      showMessage("error", error.message || "Unable to load dashboard.");
    }
  }

  bootstrap();
})();
