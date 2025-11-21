# Lucrative-CareerHub
JobBuilding is a Django-based web application designed to manage job postings, job applications, and user interactions.   This project includes user-friendly interfaces, templates, static assets, and Django models that make it a fully functional job portal system.

## 🚀 Features

### ✔️ **Job Posting Management**
- Add new job listings  
- Update job details  
- Delete or manage existing job posts  

### ✔️ **User Job Application**
- Users can view all available jobs  
- Apply directly from the application page  

### ✔️ **Admin Panel**
- Django’s built-in admin for managing:  
  - Jobs  
  - Applicants  
  - Categories  
  - User accounts  

### ✔️ **Database**
- SQLite database (`db.sqlite3`)  
- Lightweight, fast, and ideal for academic projects  

### ✔️ **UI & Templates**
- Organized templates inside the `templates/` folder  
- Static files (CSS, JS, Images) are included  

---

## 🗂️ Project Structure

JobBuilding/
│── Job/ # Django project settings
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── init.py
│
│── JobApp/ # Main application
│ ├── admin.py
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ ├── templates/
│ ├── static/
│ └── migrations/
│
│── db.sqlite3 # Database (optional to upload)
│── manage.py # Django runner
│── requirements.txt # Required Python packages
│── run.bat # Windows Quick Run (optional)
│── docs/SCREENS.docx # Screenshots / documentation
└── README.md # Project documentation


---

## 🛠️ Tech Stack

| Component | Technology |
|----------|------------|
| **Backend** | Django (Python) |
| **Frontend** | HTML, CSS, JavaScript |
| **Database** | SQLite |
| **Runtime** | Python 3.x |
| **Server** | Django Development Server |

---

## 📦 Installation & Setup

Follow these steps to run the project on your local machine.

---

### **1️⃣ Create a Virtual Environment (Recommended)**

```bash
python -m venv venv
venv\Scripts\activate   # Windows
2️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
3️⃣ Run Database Migrations
bash
Copy code
python manage.py migrate
4️⃣ Start the Development Server
bash
Copy code
python manage.py runserver
