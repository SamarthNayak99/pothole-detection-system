# 🛠️ TECHNICAL DEEP DIVE & ARCHITECTURE EXPLANATION

## 1. TECHNOLOGY STACK (The "What")

We used a modern, hybrid stack designed for speed (`FastAPI`) and mobile accessibility (`HTML5/PWA features`).

### **A. Core Stack**
1.  **Programming Language:** 
    - **Python 3.10+** (Backend logic, AI processing).
    - **JavaScript (ES6+)** (Frontend interactivity, Camera handling, API calls).
2.  **Web Framework:** **FastAPI** (Python).
    - *Why?* It's one of the fastest Python frameworks, supports asynchronous operations (`async/await`), and auto-generates API docs.
3.  **Frontend Interface:** **HTML5 + CSS3 (Web Responsiveness)**.
    - *Why?* Allows the app to run on any mobile browser (Chrome/Safari) without installing an APK/IPA.
4.  **Database:** **CSV (Comma Separated Values)**.
    - *Why?* Lightweight, easy to read, and sufficient for storing structured data (ID, Location, Time) without the overhead of SQL/NoSQL servers.

### **B. AI & Computer Vision Stack**
1.  **YOLOv8 (`ultralytics`)**: The "brain" of the detected.
    - We use the **YOLOv8 (You Only Look Once)** model for object detection.
    - It analyzes frames in milliseconds to find "pothole" patterns.
2.  **OpenCV (`cv2`)**: Used for image manipulation (saving, resizing, drawing bounding boxes).
3.  **Pillow (`PIL`)**: Used for handling image file formats.

### **C. Mapping & Geospatial Stack**
1.  **Leaflet.js**: The core mapping library.
    - *Why?* Lightweight alternative to Google Maps API (free & open source).
2.  **OpenStreetMap (OSM)**: The map tile provider.
    - Provides the actual visual map data.
3.  **Leaflet.markercluster**: A plugin to group nearby potholes into "clusters" to prevent map clutter.

---

## 2. API ENDPOINTS & COMMUNICATION (The "How")

The Mobile App communicates with the backend via **HTTP REST APIs**. Here is the complete list of "conversations" they have:

### **A. `/detect` (POST Request)**
-   **Who calls it?** The Mobile Detection Page (every ~500ms).
-   **What is sent?** A snapshot (image frame) from the camera + Current GPS Coordinates.
-   **What happens?**
    1.  Backend receives the image.
    2.  YOLO AI analyzes it.
    3.  If a pothole is found (>40% confidence):
        -   Saves image to disk.
        -   Appends data to `potholes.csv`.
        -   Triggers email alert.
-   **Response:** Returns `{"detected": true, "confidence": 0.85, "bbox": [...]}`.

### **B. `/potholes` (GET Request)**
-   **Who calls it?** History Page & Map Page.
-   **What happens?** Reads the `potholes.csv` file and converts it into a JSON list.
-   **Response:** A list of all detected potholes: `[{id: 1, lat: 12.91, lng: 77.49...}, ...]`.

### **C. `/potholes/{id}` (DELETE Request)**
-   **Who calls it?** Delete button on History/Map.
-   **What happens?** 
    1.  Finds the row in CSV with that ID.
    2.  Removes the row.
    3.  Deletes the corresponding image file.
-   **Response:** `{"message": "Pothole #123 deleted"}`.

### **D. `/detected_potholes/{filename}` (Static File Serving)**
-   **Who calls it?** Any page displaying an image.
-   **What happens?** Serves the actual `.jpg` file from the server's hard drive to the browser.

---

## 3. EMAIL ALERT SYSTEM (The "Notifier")

One of the most critical features is the automatic reporting to authorities.

### **How it Works (Pin-to-Pin)**
When `main.py` confirms a pothole detection via the `/detect` endpoint, it triggers the `send_email_alert()` function (running in a background thread to avoid slowing down the app).

### **Technical Implementation**
1.  **Protocol:** SMTP (Simple Mail Transfer Protocol) via `smtplib`.
2.  **Provider:** Gmail (`smtp.gmail.com` port 587).
3.  **Authentication:** Uses Environment Variables (`EMAIL_SENDER`, `EMAIL_PASSWORD`) for security.

### **What is Sent?**
The email is a **MIME Multipart** message containing:
1.  **Subject:** `🚨 POTHOLE ALERT: Detected with 75.5% Confidence`
2.  **Body (HTML):** A formatted report including:
    -   **Pothole ID:** Unique identifier (e.g., #176).
    -   **Time:** Exact timestamp of detection.
    -   **Location Details:** Latitude/Longitude.
    -   **Action Button:** A clickable button "🗺️ View on Google Maps" that opens the location directly.
3.  **Attachment:** The actual `.jpg` image file of the pothole with the bounding box drawn by AI.

**Why this matters:** It automates the "reporting" step. Instead of a citizen finding a pothole and calling the city, the system **instantly** notifies the maintenance department with photo evidence and GPS coordinates.

---

## 4. MAPPING SYSTEM EXPLAINED (The "Where")

The Map functionality is a sophisticated combination of several layers. Here is the pin-to-pin explanation of how `map.html` works:

### **Step 1: The Canvas (Leaflet Map)**
We initialize a map centered on the user's location.
```javascript
const map = L.map('map').setView([lat, lng], 13);
```
We load "tiles" (the actual map images) from OpenStreetMap.

### **Step 2: The Data Layer (Markers)**
We fetch the list of 193+ potholes from the API. For each pothole, we create a **Marker**:
-   **Position:** Uses the stored Latitude/Longitude.
-   **Icon:** We use a Custom Icon (🕳️ emoji) to make it distinct.

### **Step 3: The Clustering (Intelligence)**
Instead of showing 193 overlapping pins (which looks like a mess), we use **MarkerClusterGroup**.
-   **Logic:** If 5 potholes are within 10 meters, show a single circle with the number "5".
-   **Interaction:** Clicking the circle zooms in and "spiders out" the individual pins.
-   **Why?** Essential for performance and usability on mobile.

### **Step 4: The Night Mode (Dark/Light Sync)**
This is a custom implementation we built.
-   Normal maps are bright white. In Dark Mode, this hurts the eyes.
-   **Our Trick:** We apply a CSS filter to the *entire map layer* when Dark Mode is on:
    ```css
    filter: invert(100%) hue-rotate(180deg) brightness(95%);
    ```
    -   `invert(100%)`: Turns white roads into black.
    -   `hue-rotate(180deg)`: Fixes the colors (so blue water doesn't turn orange).
    -   **Result:** A professional "Dark Mode" map without paying for expensive dark map tiles.

### **Step 5: Integration**
-   **Navigate:** We generate a link: `https://www.google.com/maps?q={lat},{lng}`. This hands off the navigation task to the native Google Maps app.

---

## 5. APP COMPONENT BREAKDOWN

### **Home Page**
-   **Role:** The "Launcher".
-   **Key Tech:** `localStorage` for Sync.
-   **Logic:** When you toggle Dark Mode here, it saves `theme='dark'` into the browser's storage. All other pages listen for this and adapt immediately.

### **Mobile Detection Page**
-   **Role:** The "Collector".
-   **Key API:** `navigator.mediaDevices` (Camera) & `navigator.geolocation` (GPS).
-   **Logic:** 
    -   It acts like a loop: **Capture Frame** -> **Send to API** -> **Draw Result**.
    -   It uses the **Web Audio API** to generate the "Beep" sound (no mp3 file needed, purely code-generated sound).
    -   It uses **Vibration API** (`navigator.vibrate(200)`) for haptic feedback.

### **History Page**
-   **Role:** The "Manager".
-   **Key Tech:** DOM Manipulation.
-   **Logic:** It fetches raw JSON data and dynamically builds HTML cards (`<div class="card">...</div>`) for every pothole.

---

## 6. SUMMARY OF INNOVATIONS

1.  **Browser-Based AI:** No app store installation needed. Works instantly via URL.
2.  **Hybrid Mapping:** Combines free OSM maps with custom CSS filters for a premium "Night Mode" experience.
3.  **Real-Time Sync:** Theme preferences and data equate instantly across the app.
4.  **Auto-Healing Data:** We built scripts to fix legacy data (image paths) so the system remains robust even as we upgrade it.
