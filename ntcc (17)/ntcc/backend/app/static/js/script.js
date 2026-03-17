// Mock data for the preview
const mockFoodItems = [
  {
    id: 1,
    name: "Fresh Bread",
    description: "10 loaves of fresh bread from our bakery",
    quantity: "10 loaves",
    expiration_date: "2023-12-25",
    location_name: "Downtown Bakery",
    latitude: 40.7128,
    longitude: -74.006,
    is_claimed: false,
    created_at: "2023-12-20 09:30",
  },
  {
    id: 2,
    name: "Organic Vegetables",
    description: "Assorted organic vegetables including carrots, potatoes, and broccoli",
    quantity: "5 kg",
    expiration_date: "2023-12-24",
    location_name: "Green Market",
    latitude: 40.72,
    longitude: -74.01,
    is_claimed: false,
    created_at: "2023-12-20 10:15",
  },
  {
    id: 3,
    name: "Canned Goods",
    description: "Various canned goods including beans, corn, and soup",
    quantity: "15 cans",
    expiration_date: "2024-06-30",
    location_name: "Community Pantry",
    latitude: 40.715,
    longitude: -74.005,
    is_claimed: false,
    created_at: "2023-12-19 14:45",
  },
  {
    id: 4,
    name: "Dairy Products",
    description: "Milk, cheese, and yogurt",
    quantity: "10 items",
    expiration_date: "2023-12-23",
    location_name: "Local Dairy",
    latitude: 40.718,
    longitude: -74.008,
    is_claimed: true,
    created_at: "2023-12-18 16:20",
  },
]

const mockNotifications = [
  {
    id: 1,
    message: "Your food item 'Fresh Bread' has been claimed by FoodBank123.",
    is_read: false,
    created_at: "2023-12-20 14:30",
  },
  {
    id: 2,
    message: "Your food item 'Organic Vegetables' is expiring in 2 days.",
    is_read: false,
    created_at: "2023-12-20 09:15",
  },
  {
    id: 3,
    message: "FoodBank123 has posted new food items near you.",
    is_read: true,
    created_at: "2023-12-19 11:45",
  },
]

// Global variables
let isLoggedIn = false
let userType = null
let map = null
let postMap = null
let markers = {}

// DOM Elements
const pages = document.querySelectorAll(".page")
const navLinks = document.querySelectorAll(".nav-link")
const authLink = document.getElementById("auth-link")
const joinBtn = document.getElementById("join-btn")
const loginBtn = document.getElementById("login-btn")
const registerLink = document.getElementById("register-link")
const loginLink = document.getElementById("login-link")
const loginForm = document.getElementById("login-form")
const registerForm = document.getElementById("register-form")
const postFoodBtn = document.getElementById("post-food-btn")
const postFoodForm = document.getElementById("post-food-form")
const flashMessages = document.getElementById("flash-messages")
const notificationBadge = document.getElementById("notification-badge")
const availableItemsSection = document.getElementById("available-items-section")

// Initialize the application
document.addEventListener("DOMContentLoaded", () => {
  // Set up navigation
  setupNavigation()

  // Set up auth forms
  setupAuthForms()

  // Set up post food form
  setupPostFoodForm()

  // Initialize maps
  initializeMaps()

  // Load initial data
  loadFoodItems()
  loadNotifications()

  // Set tomorrow as the default expiration date
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  const tomorrowFormatted = tomorrow.toISOString().split("T")[0]
  if (document.getElementById("food-expiration")) {
    document.getElementById("food-expiration").value = tomorrowFormatted
  }
})

// Set up navigation
function setupNavigation() {
  navLinks.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault()
      const targetPage = link.getAttribute("data-page")

      // Check if user is logged in for protected pages
      if ((targetPage === "dashboard" || targetPage === "notifications") && !isLoggedIn) {
        showPage("login")
        showFlashMessage("Please log in to access this page")
        return
      }

      showPage(targetPage)

      // Special handling for map page
      if (targetPage === "map" && map) {
        setTimeout(() => {
          map.invalidateSize()
        }, 100)
      }
    })
  })

  joinBtn.addEventListener("click", (e) => {
    e.preventDefault()
    showPage("register")
  })

  loginBtn.addEventListener("click", (e) => {
    e.preventDefault()
    showPage("login")
  })

  postFoodBtn.addEventListener("click", (e) => {
    e.preventDefault()
    showPage("post-food")
    setTimeout(() => {
      if (postMap) postMap.invalidateSize()
    }, 100)
  })
}

// Set up authentication forms
function setupAuthForms() {
  registerLink.addEventListener("click", (e) => {
    e.preventDefault()
    showPage("register")
  })

  loginLink.addEventListener("click", (e) => {
    e.preventDefault()
    showPage("login")
  })

  loginForm.addEventListener("submit", (e) => {
    e.preventDefault()
    const username = document.getElementById("username").value
    const password = document.getElementById("password").value

    // Simulate login (in a real app, this would be an API call)
    if (username && password) {
      isLoggedIn = true
      userType = Math.random() > 0.5 ? "donor" : "recipient"
      updateAuthUI()
      showPage("dashboard")
      showFlashMessage("Login successful!")
    } else {
      showFlashMessage("Please enter both username and password")
    }
  })

  registerForm.addEventListener("submit", (e) => {
    e.preventDefault()
    const username = document.getElementById("reg-username").value
    const email = document.getElementById("reg-email").value
    const password = document.getElementById("reg-password").value
    const userTypeInputs = document.getElementsByName("user_type")
    let selectedUserType

    for (const input of userTypeInputs) {
      if (input.checked) {
        selectedUserType = input.value
        break
      }
    }

    // Simulate registration (in a real app, this would be an API call)
    if (username && email && password && selectedUserType) {
      isLoggedIn = true
      userType = selectedUserType
      updateAuthUI()
      showPage("dashboard")
      showFlashMessage("Registration successful!")
    } else {
      showFlashMessage("Please fill in all fields")
    }
  })
}

// Set up post food form
function setupPostFoodForm() {
  if (postFoodForm) {
    postFoodForm.addEventListener("submit", (e) => {
      e.preventDefault()

      const name = document.getElementById("food-name").value
      const description = document.getElementById("food-description").value
      const quantity = document.getElementById("food-quantity").value
      const expirationDate = document.getElementById("food-expiration").value
      const locationName = document.getElementById("food-location").value
      const latitude = document.getElementById("food-latitude").value
      const longitude = document.getElementById("food-longitude").value

      if (!name || !quantity || !expirationDate || !locationName || !latitude || !longitude) {
        showFlashMessage("Please fill in all required fields and pin a location on the map")
        return
      }

      // Simulate posting a food item (in a real app, this would be an API call)
      const newItem = {
        id: mockFoodItems.length + 1,
        name,
        description,
        quantity,
        expiration_date: expirationDate,
        location_name: locationName,
        latitude: Number.parseFloat(latitude),
        longitude: Number.parseFloat(longitude),
        is_claimed: false,
        created_at: new Date().toISOString().slice(0, 16).replace("T", " "),
      }

      mockFoodItems.unshift(newItem)

      // Reset form
      postFoodForm.reset()

      // Set tomorrow as the default expiration date again
      const tomorrow = new Date()
      tomorrow.setDate(tomorrow.getDate() + 1)
      const tomorrowFormatted = tomorrow.toISOString().split("T")[0]
      document.getElementById("food-expiration").value = tomorrowFormatted

      // Redirect to dashboard
      showPage("dashboard")
      showFlashMessage("Food item posted successfully!")

      // Reload food items
      loadFoodItems()
    })
  }
}

// Initialize maps
function initializeMaps() {
  // Initialize main map
  if (document.getElementById("map")) {
    map = L.map("map").setView([40.7128, -74.006], 13)
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map)
  }

  // Initialize post food map
  if (document.getElementById("post-map")) {
    postMap = L.map("post-map").setView([40.7128, -74.006], 13)
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(postMap)

    let postMarker

    // Handle map click to set location
    postMap.on("click", (e) => {
      const lat = e.latlng.lat
      const lng = e.latlng.lng

      document.getElementById("food-latitude").value = lat
      document.getElementById("food-longitude").value = lng

      if (postMarker) {
        postMarker.setLatLng([lat, lng])
      } else {
        postMarker = L.marker([lat, lng]).addTo(postMap)
      }
    })
  }
}

// Load food items
function loadFoodItems() {
  // Load posted items (for donors)
  const postedItemsContainer = document.getElementById("posted-items")
  if (postedItemsContainer) {
    if (isLoggedIn && userType === "donor") {
      postedItemsContainer.innerHTML = ""

      const donorItems = mockFoodItems.filter((item) => !item.is_claimed)

      if (donorItems.length === 0) {
        postedItemsContainer.innerHTML = '<p class="no-items">You haven\'t posted any food items yet.</p>'
      } else {
        donorItems.forEach((item) => {
          postedItemsContainer.innerHTML += createFoodItemCard(item, false)
        })
      }
    } else {
      postedItemsContainer.innerHTML = '<p class="no-items">You haven\'t posted any food items yet.</p>'
    }
  }

  // Load available items (for recipients)
  const availableItemsContainer = document.getElementById("available-items")
  if (availableItemsContainer) {
    if (isLoggedIn && userType === "recipient") {
      availableItemsContainer.innerHTML = ""

      const availableItems = mockFoodItems.filter((item) => !item.is_claimed)

      if (availableItems.length === 0) {
        availableItemsContainer.innerHTML = '<p class="no-items">No food items are currently available.</p>'
      } else {
        availableItems.forEach((item) => {
          availableItemsContainer.innerHTML += createFoodItemCard(item, true)
        })
      }

      // Add event listeners to claim buttons
      document.querySelectorAll(".claim-btn").forEach((button) => {
        button.addEventListener("click", function () {
          const foodId = Number.parseInt(this.getAttribute("data-id"))
          claimFoodItem(foodId)
        })
      })
    } else {
      availableItemsContainer.innerHTML = '<p class="no-items">No food items are currently available.</p>'
    }
  }

  // Show/hide sections based on user type
  if (availableItemsSection) {
    if (isLoggedIn && userType === "recipient") {
      availableItemsSection.style.display = "block"
    } else {
      availableItemsSection.style.display = "none"
    }
  }

  // Load map items
  const foodItemsList = document.getElementById("food-items-list")
  if (foodItemsList && map) {
    foodItemsList.innerHTML = ""

    // Clear existing markers
    for (const id in markers) {
      map.removeLayer(markers[id])
    }
    markers = {}

    const availableItems = mockFoodItems.filter((item) => !item.is_claimed)

    if (availableItems.length === 0) {
      foodItemsList.innerHTML = '<p class="no-items">No food items are currently available.</p>'
    } else {
      availableItems.forEach((item) => {
        // Create marker
        const marker = L.marker([item.latitude, item.longitude]).addTo(map)
        markers[item.id] = marker

        // Create popup content
        const popupContent = `
                    <div class="map-popup">
                        <h3>${item.name}</h3>
                        <p><strong>Quantity:</strong> ${item.quantity}</p>
                        <p><strong>Expires:</strong> ${item.expiration_date}</p>
                        <p><strong>Location:</strong> ${item.location_name}</p>
                        ${item.description ? `<p><strong>Description:</strong> ${item.description}</p>` : ""}
                        <div class="map-popup-claim">
                            <button class="btn btn-primary btn-sm popup-claim-btn" data-id="${item.id}">Claim This Item</button>
                        </div>
                    </div>
                `

        marker.bindPopup(popupContent)

        // Add event listener after popup is opened
        marker.on("popupopen", () => {
          document.querySelector(".popup-claim-btn").addEventListener("click", function () {
            const foodId = Number.parseInt(this.getAttribute("data-id"))
            if (isLoggedIn) {
              claimFoodItem(foodId)
            } else {
              showPage("login")
              showFlashMessage("Please log in to claim food items")
            }
          })
        })

        // Create sidebar item
        const sidebarItem = document.createElement("div")
        sidebarItem.className = "map-food-item"
        sidebarItem.setAttribute("data-id", item.id)
        sidebarItem.innerHTML = `
                    <h4>${item.name}</h4>
                    <p><strong>Quantity:</strong> ${item.quantity}</p>
                    <p><strong>Expires:</strong> ${item.expiration_date}</p>
                `

        // Click on sidebar item to focus on map marker
        sidebarItem.addEventListener("click", () => {
          map.setView([item.latitude, item.longitude], 16)
          markers[item.id].openPopup()
        })

        foodItemsList.appendChild(sidebarItem)
      })

      // If we have items, fit the map to show all markers
      if (availableItems.length > 0) {
        const bounds = []
        availableItems.forEach((item) => {
          bounds.push([item.latitude, item.longitude])
        })
        map.fitBounds(bounds)
      }
    }
  }
}

// Load notifications
function loadNotifications() {
  const notificationsList = document.getElementById("notifications-list")
  if (notificationsList) {
    notificationsList.innerHTML = ""

    if (mockNotifications.length === 0) {
      notificationsList.innerHTML = '<p class="no-items">You don\'t have any notifications.</p>'
    } else {
      mockNotifications.forEach((notification) => {
        notificationsList.innerHTML += `
                    <div class="notification-item ${notification.is_read ? "" : "unread"}">
                        <div class="notification-content">
                            <p>${notification.message}</p>
                            <span class="notification-time">${notification.created_at}</span>
                        </div>
                    </div>
                `
      })
    }
  }

  // Update notification badge
  const unreadCount = mockNotifications.filter((n) => !n.is_read).length
  notificationBadge.textContent = unreadCount > 0 ? unreadCount : ""
}

// Claim food item
function claimFoodItem(foodId) {
  if (!isLoggedIn) {
    showPage("login")
    showFlashMessage("Please log in to claim food items")
    return
  }

  // Find the food item
  const itemIndex = mockFoodItems.findIndex((item) => item.id === foodId)
  if (itemIndex !== -1) {
    // Mark as claimed
    mockFoodItems[itemIndex].is_claimed = true

    // Add notification for the donor
    const newNotification = {
      id: mockNotifications.length + 1,
      message: `Your food item '${mockFoodItems[itemIndex].name}' has been claimed.`,
      is_read: false,
      created_at: new Date().toISOString().slice(0, 16).replace("T", " "),
    }

    mockNotifications.unshift(newNotification)

    // Reload data
    loadFoodItems()
    loadNotifications()

    showFlashMessage("Food item claimed successfully!")
  }
}

// Create food item card
function createFoodItemCard(item, showClaimButton) {
  return `
        <div class="food-item-card ${item.is_claimed ? "claimed" : ""}">
            <div class="food-item-header">
                <h4>${item.name}</h4>
                <span class="status ${item.is_claimed ? "claimed" : "available"}">${item.is_claimed ? "Claimed" : "Available"}</span>
            </div>
            <div class="food-item-details">
                <p><strong>Quantity:</strong> ${item.quantity}</p>
                <p><strong>Location:</strong> ${item.location_name}</p>
                <p><strong>Expires:</strong> ${item.expiration_date}</p>
                ${item.description ? `<p><strong>Description:</strong> ${item.description}</p>` : ""}
                <p><strong>Posted:</strong> ${item.created_at}</p>
                ${showClaimButton && !item.is_claimed ? `<button class="btn btn-primary claim-btn" data-id="${item.id}">Claim This Item</button>` : ""}
            </div>
        </div>
    `
}

// Show page
function showPage(pageId) {
  pages.forEach((page) => {
    page.classList.remove("active")
  })

  const targetPage = document.getElementById(`${pageId}-page`)
  if (targetPage) {
    targetPage.classList.add("active")
  }
}

// Show flash message
function showFlashMessage(message) {
  const flashMessage = document.createElement("div")
  flashMessage.className = "flash-message"
  flashMessage.textContent = message

  flashMessages.appendChild(flashMessage)

  // Auto-dismiss after 5 seconds
  setTimeout(() => {
    flashMessage.style.opacity = "0"
    setTimeout(() => {
      flashMessage.remove()
    }, 300)
  }, 5000)
}

// Update auth UI
function updateAuthUI() {
  if (isLoggedIn) {
    authLink.textContent = "Logout"
    authLink.setAttribute("data-page", "home")
    authLink.addEventListener(
      "click",
      (e) => {
        e.preventDefault()
        isLoggedIn = false
        userType = null
        updateAuthUI()
        showPage("home")
        showFlashMessage("You have been logged out")
      },
      { once: true },
    )
  } else {
    authLink.textContent = "Login"
    authLink.setAttribute("data-page", "login")
  }
}
