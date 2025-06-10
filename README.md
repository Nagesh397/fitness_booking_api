# 🧘‍♀️ fitness_booking_api

A Django REST API for booking fitness classes. Clients can view, book, and manage class slots.  
Supports timezones, validation, and error handling. Built using Django and Django REST Framework with clean, modular code and sample seed data.

---

## 📚 Table of Contents

- [Features](#-features)
- [Setup Instructions](#-setup-instructions)
- [API Endpoints](#-api-endpoints)
- [Timezone Support](#-timezone-support)
- [Unit Tests](#-unit-tests)
- [License](#-license)
- [Author](#-author)

---

## 🚀 Features

- ✅ View available fitness classes
- ✅ Book slots in available classes
- ✅ Timezone support (IST by default)
- ✅ Overbooking prevention
- ✅ Input validation and structured error handling

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/fitness_booking_api.git
cd fitness_booking_api
```

### 2. Create and Activate a Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Or activate on macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is missing:

```bash
pip install django djangorestframework pytz
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Seed Sample Data (Optional)

You can create seed data using custom Django commands, fixtures, or scripts.

### 6. Start the Development Server

```bash
python manage.py runserver
```

Access your API at: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔌 API Endpoints

### 📋 List All Classes

**GET** `/classes/`

```bash
curl -X GET "http://localhost:8000/classes"
```

**Response** 
```json
[
{"id":3,"name":"Pilates","instructor":"Meena","datetime":"2025-06-11T09:00:00+05:30","available_slots":8},
{"id":4,"name":"HIIT","instructor":"Ravi","datetime":"2025-06-11T18:00:00+05:30","available_slots":8},
{"id":5,"name":"Strength Training","instructor":"Anita","datetime":"2025-06-12T07:30:00+05:30","available_slots":12}
]
```

---

### ➕ Book a Class Slot

**POST** `/bookings/`

#### cURL Example

```bash
curl -X POST "http://localhost:8000/book" \
  -H "Content-Type: application/json" \
  -d '{
    "class_id": 3,
    "client_name": "nagu",
    "client_email": "nagu@example.com"
}'

```
**Response**
```json
  {"id":4,"client_name":"nagu","client_email":"nagu@example.com","booked_at":"2025-06-10T06:23:06.939572Z","fitness_class":3}
```

---

### 📅 View Bookings made by a specific email address

**GET** `/bookings/`

```bash
curl -X GET "http://localhost:8000/bookings?email=nagu@example.com"
```
**Response**
```json
  [
  {"id":4,"client_name":"nagu","client_email":"nagu@example.com","booked_at":"2025-06-10T06:23:06.939572Z","fitness_class":3},
  {"id":5,"client_name":"nagu","client_email":"nagu@example.com","booked_at":"2025-06-10T06:33:13.100902Z","fitness_class":3}
]
```
---

## 🌐 Timezone Support

Class times are stored in **IST** (`Asia/Kolkata`). If needed, you can:

- Adjust on the frontend for the user’s local time.
- Extend the backend to accept user timezones and convert accordingly.

---


## 🧾 License

MIT License. See `LICENSE` file for details.

---

## 👨‍💻 Author

[Nagesh Acharya](https://github.com/Nagesh397)
