# MoodTune Backend

MoodTune is a backend project for managing user data and playlists, designed to power a Spotify-based recommendation system. This backend provides APIs for user management, playlist analysis, and integration with a machine learning model.

---

## **Getting Started**

Follow these steps to set up and run the project locally:

### **Prerequisites**

Make sure you have the following installed on your machine:
- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- A virtual environment tool (`venv` is included with Python).

---


### **1. Clone the Repository**

```bash
git clone https://github.com/yourusername/moodtune-backend.git
cd moodtune-backend
```


### **2.  Set Up the Virtual Environment**
Create and activate a virtual environment:
# Windows
```bash
python -m venv venv
venv\Scripts\activate
```

# macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```


### **3. Install Dependencies**
Install the required Python libraries:

```bash
pip install -r requirements.txt
```


### **4. Configure Environment Variables**
Create a .env file in the root directory and add the following:

```bash
FLASK_APP=run.py
FLASK_ENV=development
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>
DEBUG=True
```

Replace <username>, <password>, <host>, <port>, and <database> with your PostgreSQL credentials.


### **5. Initialize the Database**
Run the following command to create the necessary tables in your database:

```bash
python init_db.py
```


### **6. Run the Application**
Start the Flask development server:

```bash
python run.py
```

The server will be available at http://127.0.0.1:5000.

---


### **Endpoints Overview**

| Endpoint       | Method | Description                  |
|----------------|--------|------------------------------|
| `/users/`      | GET    | Fetch user-related information. |
| `/users/save`  | POST   | Save user data and tracks.   |


### **License**
This project is licensed under the MIT License. See the LICENSE file for details.
