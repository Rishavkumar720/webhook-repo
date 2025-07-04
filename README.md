# 🚀 Webhook Listener with Flask, MongoDB, and Dashboard

This repository (`webhook-repo`) contains the code for a **GitHub Webhook Listener** built using **Flask** and **MongoDB Atlas**. It captures events like `push` and `pull_request` from another GitHub repository (`action-repo`) and stores them in MongoDB. It also includes a simple **dashboard** to display the stored events.


webhook-repo/
│
├── app.py # Flask application
├── .env # Environment variables (MongoDB connection string)
├── templates/
│ └── dashboard.html # Simple dashboard UI
└── requirements.txt # Python dependencies

yaml
Copy
Edit

---

## 🌐 Features

- Receives **GitHub webhook** events (`push`, `pull_request`).
- Saves the event data in **MongoDB Atlas**.
- Provides a basic **web dashboard** to view received events.

---

## 🛠 Technologies Used

- Python 3.x
- Flask
- MongoDB Atlas (Cloud)
- Ngrok (for exposing localhost)
- HTML/CSS (for the dashboard)

---

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/YourUsername/webhook-repo.git
cd webhook-repo
2️⃣ Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
3️⃣ Create .env File
ini
Copy
Edit
MONGO_URI=mongodb+srv://<your-username>:<your-password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
Replace with your MongoDB Atlas connection string.

4️⃣ Run Flask Server
bash
Copy
Edit
python app.py
5️⃣ Start Ngrok (in a separate terminal)
bash
Copy
Edit
ngrok http 5000
Copy the Ngrok link (e.g., https://abcd1234.ngrok-free.app/webhook).

🔗 GitHub Webhook Setup (For action-repo)
Go to your action-repo → Settings → Webhooks → Add webhook.

Payload URL: https://<your-ngrok>.ngrok-free.app/webhook

Content type: application/json


