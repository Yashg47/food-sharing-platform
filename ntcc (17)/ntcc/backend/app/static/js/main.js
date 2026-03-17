// Main JavaScript file for FoodShare platform

document.addEventListener("DOMContentLoaded", () => {
    // Auto-dismiss flash messages after 5 seconds
    const flashMessages = document.querySelectorAll(".flash-message")
    if (flashMessages.length > 0) {
      setTimeout(() => {
        flashMessages.forEach((message) => {
          message.style.opacity = "0"
          setTimeout(() => {
            message.style.display = "none"
          }, 300)
        })
      }, 5000)
    }
  
    // Set min date for expiration date inputs to today
    const expirationDateInputs = document.querySelectorAll('input[type="date"]')
    if (expirationDateInputs.length > 0) {
      const today = new Date().toISOString().split("T")[0]
      expirationDateInputs.forEach((input) => {
        input.setAttribute("min", today)
      })
    }
  
    // Initialize any tooltips or popovers
    const tooltipElements = document.querySelectorAll("[data-tooltip]")
    tooltipElements.forEach((element) => {
      element.addEventListener("mouseenter", function () {
        const tooltip = document.createElement("div")
        tooltip.className = "tooltip"
        tooltip.textContent = this.getAttribute("data-tooltip")
        document.body.appendChild(tooltip)
  
        const rect = this.getBoundingClientRect()
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + "px"
        tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + "px"
        tooltip.style.opacity = "1"
  
        this.addEventListener(
          "mouseleave",
          () => {
            tooltip.remove()
          },
          { once: true },
        )
      })
    })
  })
  
  // Function to format dates in a user-friendly way
  function formatDate(dateString) {
    const date = new Date(dateString)
    return date.toLocaleDateString("en-US", {
      year: "numeric",
      month: "short",
      day: "numeric",
    })
  }
  
  // Function to calculate days remaining until expiration
  function daysUntilExpiration(expirationDate) {
    const today = new Date()
    today.setHours(0, 0, 0, 0)
  
    const expDate = new Date(expirationDate)
    expDate.setHours(0, 0, 0, 0)
  
    const diffTime = expDate - today
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
    return diffDays
  }
  
  document.body.addEventListener('click', function (e) {
  if (e.target.classList.contains('claim-btn')) {
    const foodId = e.target.dataset.id;

    const wantsDelivery = confirm("Do you want a delivery partner for this item?");

    fetch(`/claim/${foodId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ wants_delivery: wantsDelivery })
    })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        // Optionally remove the claimed item from UI
        const itemElement = document.querySelector(`.map-food-item[data-id="${foodId}"]`);
        if (itemElement) itemElement.remove();
      })
      .catch(err => {
        console.error("Claim failed:", err);
        alert("Something went wrong while claiming.");
      });
  }
});
let selectedFoodId = null;

document.body.addEventListener("click", function (e) {
  if (e.target.classList.contains("claim-btn")) {
    selectedFoodId = e.target.dataset.id;
    const modal = new bootstrap.Modal(document.getElementById("deliveryModal"));
    modal.show();
  }
});

document.getElementById("yes-delivery-btn").addEventListener("click", function () {
  claimFood(true);
});
document.getElementById("no-delivery-btn").addEventListener("click", function () {
  claimFood(false);
});

function claimFood(wantsDelivery) {
  if (!selectedFoodId) return;

  fetch(`/claim/${selectedFoodId}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ wants_delivery: wantsDelivery })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message);
      selectedFoodId = null;
      if (data.success) location.reload();
    })
    .catch(err => {
      alert("Something went wrong while claiming.");
      console.error(err);
    });
}
fetch(`/claim/${foodId}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        wants_delivery: confirm("Do you want a delivery partner for this item?")
    })
})
.then(response => response.json())
.then(data => {
    alert(data.message)
    if (data.success) {
        // Optional: remove from map/sidebar
    }
})
.catch(error => {
    console.error("Claim error:", error)
    alert("Something went wrong.")
})
fetch(`/claim/${foodId}`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ wants_delivery: true }),
})
.then(res => res.json())
.then(data => {
  if (data.success) {
    const delivery = data.delivery_partner;
    if (delivery) {
      document.getElementById("delivery-info").innerHTML = `
        <h4>Delivery Partner Assigned:</h4>
        <p><strong>Name:</strong> ${delivery.name}</p>
        <p><strong>Phone:</strong> ${delivery.phone}</p>
        <p><strong>Email:</strong> ${delivery.email}</p>
      `;
    } else {
      document.getElementById("delivery-info").innerText = "You chose not to use a delivery partner.";
    }
  } else {
    alert(data.message);
  }
});
fetch(`/claim/${foodId}`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ wants_delivery: true })  // or false
})
.then(response => response.json())
.then(data => {
  alert(data.message);
  if (data.delivery_partner) {
    alert(`📦 Delivery Partner Assigned:\nName: ${data.delivery_partner.name}\nPhone: ${data.delivery_partner.phone}`);
  }
});
fetch(`/claim/${foodId}`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ wants_delivery: true })  // or false
})
.then(response => response.json())
.then(data => {
  alert(data.message);
  if (data.delivery_partner) {
    alert(`📦 Delivery Partner Assigned:\nName: ${data.delivery_partner.name}\nPhone: ${data.delivery_partner.phone}`);
  }
});
let allFoodItems = [];

function applyFilters() {
    const locationFilter = document.getElementById("filter-location").value.toLowerCase();
    const expiryFilter = document.getElementById("filter-expiry").value;
    const keywordFilter = document.getElementById("filter-keyword").value.toLowerCase();

    // Clear existing markers and sidebar
    for (const id in markers) {
        map.removeLayer(markers[id]);
    }
    foodItemsList.innerHTML = '';

    const filtered = allFoodItems.filter(item => {
        const matchLocation = locationFilter ? item.location_name.toLowerCase().includes(locationFilter) : true;
        const matchExpiry = expiryFilter ? item.expiration_date >= expiryFilter : true;
        const matchKeyword =
            keywordFilter
                ? item.name.toLowerCase().includes(keywordFilter) ||
                  (item.description && item.description.toLowerCase().includes(keywordFilter))
                : true;

        return matchLocation && matchExpiry && matchKeyword;
    });

    if (filtered.length === 0) {
        foodItemsList.innerHTML = '<p>No matching food items.</p>';
        return;
    }

    const bounds = [];
    filtered.forEach(item => {
        const marker = L.marker([item.latitude, item.longitude]).addTo(map);
        markers[item.id] = marker;

        const popupContent = `
            <div class="map-popup">
                <h3>${item.name}</h3>
                <p><strong>Quantity:</strong> ${item.quantity}</p>
                <p><strong>Expires:</strong> ${item.expiration_date}</p>
                <p><strong>Location:</strong> ${item.location_name}</p>
                ${item.description ? `<p><strong>Description:</strong> ${item.description}</p>` : ''}
                <div class="map-popup-claim">
                    <label><input type="checkbox" id="delivery-${item.id}"> Request delivery?</label><br>
                    <button class="btn btn-primary btn-sm claim-btn" data-id="${item.id}">Claim This Item</button>
                </div>
            </div>
        `;
        marker.bindPopup(popupContent);
        bounds.push([item.latitude, item.longitude]);

        const sidebarItem = document.createElement('div');
        sidebarItem.className = 'map-food-item';
        sidebarItem.dataset.id = item.id;
        sidebarItem.innerHTML = `
            <h4>${item.name}</h4>
            <p><strong>Quantity:</strong> ${item.quantity}</p>
            <p><strong>Expires:</strong> ${item.expiration_date}</p>
        `;
        sidebarItem.addEventListener('click', () => {
            map.setView([item.latitude, item.longitude], 16);
            marker.openPopup();
        });

        foodItemsList.appendChild(sidebarItem);
    });

    if (bounds.length > 0) map.fitBounds(bounds);
}

function resetFilters() {
    document.getElementById("filter-location").value = '';
    document.getElementById("filter-expiry").value = '';
    document.getElementById("filter-keyword").value = '';
    applyFilters();
}
