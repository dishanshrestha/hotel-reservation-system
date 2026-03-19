(() => {
  const API_BASE_KEY = "hotel_api_base";
  const META_API_BASE = document.querySelector('meta[name="api-base-url"]')?.getAttribute("content") || "";

  const grid = document.getElementById("rooms-grid");
  const bookingForm = document.getElementById("room-booking-form");
  const bookingMessage = document.getElementById("booking-message");
  const roomsFeedback = document.getElementById("rooms-feedback");
  const recommendationsSection = document.getElementById("recommendations-section");
  const recommendationsGrid = document.getElementById("recommendations-grid");
  const recommendationsMeta = document.getElementById("recommendations-meta");

  if (!grid || !bookingForm) {
    return;
  }

  const selectedRoomIdInput = document.getElementById("selected-room-id");
  const selectedRoomNameInput = document.getElementById("selected-room-name");
  const bookingNameInput = document.getElementById("booking-name");
  const bookingEmailInput = document.getElementById("booking-email");
  const bookingPhoneInput = document.getElementById("booking-phone");
  const bookingStartInput = document.getElementById("booking-start-date");
  const bookingEndInput = document.getElementById("booking-end-date");

  const roomPriceMap = new Map();

  function parseQueryDate(key) {
    const value = new URLSearchParams(window.location.search).get(key);
    if (!value) {
      return "";
    }
    return /^\d{4}-\d{2}-\d{2}$/.test(value) ? value : "";
  }

  function normalizeApiBase(url) {
    return String(url || "").trim().replace(/\/$/, "");
  }

  function resolveApiBase() {
    return normalizeApiBase(localStorage.getItem(API_BASE_KEY) || META_API_BASE || "http://localhost:8000");
  }

  function showMessage(target, kind, text, allowHtml = false) {
    if (!target) {
      return;
    }
    target.classList.remove("is-error", "is-success");
    if (text) {
      target.classList.add(kind === "error" ? "is-error" : "is-success");
      if (allowHtml) {
        target.innerHTML = text;
      } else {
        target.textContent = text;
      }
    } else {
      target.textContent = "";
    }
  }

  function apiOrigin(apiBase) {
    try {
      return new URL(apiBase).origin;
    } catch {
      return "http://localhost:8000";
    }
  }

  function displayImage(raw, apiBase) {
    if (!raw) {
      return "images/room1.jpg";
    }
    if (raw.startsWith("http://") || raw.startsWith("https://")) {
      return raw;
    }
    if (raw.startsWith("/")) {
      return `${apiOrigin(apiBase)}${raw}`;
    }
    return `${apiOrigin(apiBase)}/media/${raw.replace(/^\/+/, "")}`;
  }

  function selectRoom(roomId, roomTitle) {
    selectedRoomIdInput.value = String(roomId);
    selectedRoomNameInput.value = roomTitle;
    document.getElementById("room-booking-panel").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function normalizePrice(rawPrice) {
    const parsed = Number.parseFloat(String(rawPrice || "").replace(/[^0-9.]/g, ""));
    return Number.isFinite(parsed) ? parsed : null;
  }

  function calculateTotalPrice(roomId, startDate, endDate) {
    const pricePerNight = roomPriceMap.get(String(roomId));
    if (!pricePerNight) {
      return null;
    }

    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffMs = end.getTime() - start.getTime();
    const nights = Math.max(1, Math.ceil(diffMs / (1000 * 60 * 60 * 24)));
    return Number((nights * pricePerNight).toFixed(2));
  }

  function renderRecommendations(recommendations, apiBase) {
    if (!recommendationsSection || !recommendationsGrid || !recommendationsMeta) {
      return;
    }

    if (!Array.isArray(recommendations) || !recommendations.length) {
      recommendationsSection.classList.remove("is-visible");
      recommendationsGrid.innerHTML = "";
      recommendationsMeta.textContent = "";
      return;
    }

    recommendationsSection.classList.add("is-visible");
    recommendationsMeta.textContent = "Top matches are ranked by rating, price fit, room type, and wifi preference.";
    recommendationsGrid.innerHTML = "";

    for (const room of recommendations) {
      const roomId = String(room.id);
      const roomTitle = room.room_title || `Room ${room.id}`;
      const card = document.createElement("div");
      card.className = "col-md-4 col-sm-6";
      card.innerHTML = `
        <div class="room dynamic-room-card recommendation-card">
          <div class="room_img">
            <figure><img src="${displayImage(room.image || room.image_raw, apiBase)}" alt="${roomTitle}"></figure>
          </div>
          <div class="bed_room">
            <h3>${roomTitle}</h3>
            <p class="room-meta"><strong>Score:</strong> ${(Number(room.recommendation_score || 0) * 100).toFixed(1)}%</p>
            <p class="room-meta"><strong>Type:</strong> ${room.room_type || "Standard"}</p>
            <p class="room-meta"><strong>Price:</strong> ${room.price || "Contact us"}</p>
            <button type="button" class="book_btn room-select-btn" data-room-id="${roomId}" data-room-title="${roomTitle}">Choose Recommended Room</button>
          </div>
        </div>
      `;
      recommendationsGrid.appendChild(card);
    }
  }

  async function loadRecommendations() {
    const apiBase = resolveApiBase();
    const startDate = bookingStartInput.value;
    const endDate = bookingEndInput.value;

    if (!startDate || !endDate || endDate <= startDate) {
      renderRecommendations([], apiBase);
      return;
    }

    const params = new URLSearchParams({
      start_date: startDate,
      end_date: endDate,
      top_k: "3",
    });

    try {
      const response = await fetch(`${apiBase}/api/recommendations/rooms?${params.toString()}`);
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || "Failed to load recommendations");
      }
      renderRecommendations(data.recommendations || [], apiBase);
    } catch {
      renderRecommendations([], apiBase);
    }
  }

  async function loadRooms() {
    const apiBase = resolveApiBase();
    localStorage.setItem(API_BASE_KEY, apiBase);

    showMessage(roomsFeedback, "success", "");
    grid.innerHTML = '<div class="col-md-12"><p class="text-center py-4">Loading rooms...</p></div>';

    try {
      const response = await fetch(`${apiBase}/api/rooms`);
      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(data.detail || "Failed to load rooms");
      }

      const rooms = data.rooms || [];
      roomPriceMap.clear();

      if (!rooms.length) {
        grid.innerHTML = '<div class="col-md-12"><p class="text-center py-4">No rooms available right now.</p></div>';
        renderRecommendations([], apiBase);
        return;
      }

      grid.innerHTML = "";
      for (const room of rooms) {
        const roomId = String(room.id);
        const roomTitle = room.room_title || `Room ${room.id}`;
        const roomPrice = normalizePrice(room.price);
        if (roomPrice) {
          roomPriceMap.set(roomId, roomPrice);
        }

        const card = document.createElement("div");
        card.className = "col-md-4 col-sm-6";
        card.innerHTML = `
          <div class="room dynamic-room-card">
            <div class="room_img">
              <figure><img src="${displayImage(room.image || room.image_raw, apiBase)}" alt="${roomTitle}"></figure>
            </div>
            <div class="bed_room">
              <h3>${roomTitle}</h3>
              <p>${room.description || "Comfortable stay with modern amenities."}</p>
              <p class="room-meta"><strong>Type:</strong> ${room.room_type || "Standard"}</p>
              <p class="room-meta"><strong>Price:</strong> ${room.price || "Contact us"}</p>
              <button type="button" class="book_btn room-select-btn" data-room-id="${roomId}" data-room-title="${roomTitle}">Book This Room</button>
            </div>
          </div>
        `;
        grid.appendChild(card);
      }

      await loadRecommendations();
    } catch (error) {
      grid.innerHTML = "";
      showMessage(roomsFeedback, "error", error.message || "Unable to load rooms.");
    }
  }

  grid.addEventListener("click", (event) => {
    const button = event.target.closest(".room-select-btn");
    if (!button) {
      return;
    }
    selectRoom(button.dataset.roomId, button.dataset.roomTitle);
  });

  bookingMessage?.addEventListener("click", (event) => {
    const slotButton = event.target.closest(".slot-suggestion-btn");
    if (!slotButton) {
      return;
    }
    const startDate = slotButton.getAttribute("data-start") || "";
    const endDate = slotButton.getAttribute("data-end") || "";
    if (startDate && endDate) {
      bookingStartInput.value = startDate;
      bookingEndInput.value = endDate;
      loadRecommendations();
      showMessage(bookingMessage, "success", "Suggested dates applied. You can submit the booking now.");
    }
  });

  bookingStartInput.addEventListener("change", loadRecommendations);
  bookingEndInput.addEventListener("change", loadRecommendations);

  bookingForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const roomId = selectedRoomIdInput.value.trim();
    const roomTitle = selectedRoomNameInput.value.trim();
    const name = bookingNameInput.value.trim();
    const email = bookingEmailInput.value.trim();
    const phone = bookingPhoneInput.value.trim();
    const startDate = bookingStartInput.value;
    const endDate = bookingEndInput.value;
    const apiBase = resolveApiBase();

    if (!roomId || !roomTitle) {
      showMessage(bookingMessage, "error", "Please choose a room first.");
      return;
    }

    if (!name || !email || !startDate || !endDate) {
      showMessage(bookingMessage, "error", "Name, email, arrival, and departure are required.");
      return;
    }

    if (endDate <= startDate) {
      showMessage(bookingMessage, "error", "Departure date must be after arrival date.");
      return;
    }

    localStorage.setItem(API_BASE_KEY, apiBase);

    const payload = {
      room_id: Number(roomId),
      name,
      email,
      phone: phone || null,
      start_date: startDate,
      end_date: endDate,
      total_price: calculateTotalPrice(roomId, startDate, endDate),
    };

    showMessage(bookingMessage, "success", "Submitting your booking...");

    try {
      const response = await fetch(`${apiBase}/api/bookings`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await response.json().catch(() => ({}));
      if (!response.ok) {
        const detail = data.detail;
        if (response.status === 409 && detail && typeof detail === "object" && Array.isArray(detail.alternative_slots)) {
          const slotButtons = detail.alternative_slots
            .map(
              (slot) =>
                `<button type="button" class="slot-suggestion-btn" data-start="${slot.start_date}" data-end="${slot.end_date}">${slot.start_date} to ${slot.end_date} (${slot.nights} nights)</button>`
            )
            .join("");

          const message = `${detail.message || "Room is not available for these dates."}<br><br><strong>Try one of these:</strong><br><div class="slot-suggestion-list">${slotButtons}</div>`;
          showMessage(bookingMessage, "error", message, true);
          return;
        }

        if (typeof detail === "string") {
          throw new Error(detail);
        }
        throw new Error("Booking failed");
      }

      const emailStatus = data.email_confirmation_sent
        ? "A confirmation email has been sent."
        : "Booking saved. Email confirmation is pending server email configuration.";

      showMessage(bookingMessage, "success", `Booking confirmed for ${roomTitle}. ${emailStatus}`);
      bookingForm.reset();
      selectedRoomIdInput.value = "";
      selectedRoomNameInput.value = "";

      const arrival = parseQueryDate("arrival");
      const departure = parseQueryDate("departure");
      if (arrival) {
        bookingStartInput.value = arrival;
      }
      if (departure) {
        bookingEndInput.value = departure;
      }

      await loadRecommendations();
    } catch (error) {
      showMessage(bookingMessage, "error", error.message || "Unable to complete booking.");
    }
  });

  localStorage.setItem(API_BASE_KEY, resolveApiBase());

  const arrival = parseQueryDate("arrival");
  const departure = parseQueryDate("departure");
  if (arrival) {
    bookingStartInput.value = arrival;
  }
  if (departure) {
    bookingEndInput.value = departure;
  }

  loadRooms();
  loadRecommendations();
})();
