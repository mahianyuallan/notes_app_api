# 📒 Notes App API  

A simple **Notes API** built with **FastAPI**, implementing **JWT authentication** to allow users to register, log in, and manage their personal notes. Each user can only view and manage their own notes, ensuring secure multi-user functionality.

---

## 🚀 Features  

- **User Authentication**
  - Register new users
  - Secure login with JWT tokens
- **Notes Management**
  - Create a new note
  - Get all notes belonging to the authenticated user
  - Get a single note by ID
  - Update a note
- **Authorization**
  - Only authenticated users can access the API
  - Users can only manage their own notes

---

## 🛠️ Tech Stack  

- **Backend Framework:** FastAPI  
- **Database:** SQLite (with SQLAlchemy ORM)  
- **Authentication:** JWT (JSON Web Tokens) via `python-jose`  
- **Password Hashing:** Passlib (bcrypt)  
- **Environment Management:** python-dotenv  

---


