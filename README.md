# food-sharing-platform
# 🍱 FoodShare – Community Food Waste & Surplus Sharing Platform

🚀 A full-stack web application that connects food donors with NGOs and individuals to reduce food waste and support communities in need.

---

## 🌍 Problem Statement

Millions of tons of food are wasted daily while many people go hungry.

**FoodShare solves this by:**

* Connecting donors with nearby NGOs/recipients
* Enabling real-time food sharing
* Reducing food waste using technology

---

## ✨ Features

### 👤 Authentication

* User registration & login system
* Role-based access (Donor / Recipient)

### 🍲 Food Management

* Donors can post surplus food
* Add quantity, expiry, and location
* Track posted items

### 📍 Interactive Map

* View available food on map
* Locate nearby food items
* Click to claim food

### 📦 Claim System

* Recipients can claim food items
* Optional delivery request
* Real-time updates

### 📊 Dashboard

* Donor dashboard (posted items)
* Recipient dashboard (claimed items + map)

### 🔔 Notifications

* Real-time alerts
* Claim updates
* Expiry reminders

---

## 🛠️ Tech Stack

### 💻 Frontend

* HTML5, CSS3
* JavaScript
* Leaflet.js (Maps)

### ⚙️ Backend

* Flask (Python)
* Flask Blueprints
* REST APIs

### 🗄️ Database

* SQLite
* SQLAlchemy ORM
* Flask-Migrate (Alembic)

---

## 📂 Project Structure

```
ntcc/
 └── backend/
     └── app/
         ├── routes/
         ├── templates/
         ├── static/
         ├── models.py
         └── __init__.py
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/foodshare.git
cd foodshare/backend
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup database

```bash
flask --app manage.py db upgrade
```

### 5️⃣ Run the app

```bash
flask --app manage.py run
```

---

## 🚀 Usage

* Open: `http://127.0.0.1:5000`
* Register as donor or recipient
* Post or claim food items
* Explore map & dashboards

---

## 📸 Screenshots

*(Add screenshots here for better presentation)*

---

## 🔥 Future Improvements

* 📊 Analytics dashboard (charts)
* 🌐 Deployment (Render / AWS)
* 📱 Mobile responsiveness
* 🔔 Real-time WebSocket notifications
* 🤖 AI-based food demand prediction

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repo
2. Create a new branch
3. Commit changes
4. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Yash Gauri**
📧 [yashgauri47@gmail.com](mailto:yashgauri47@gmail.com)
🔗 LinkedIn: https://www.linkedin.com/in/yash-gauri-179b5b339

---

⭐ If you like this project, don’t forget to star the repo!
