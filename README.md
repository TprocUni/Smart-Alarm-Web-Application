# Smart-Alarm-Web-Application
This Python Flask-based application acts as a smart alarm system that integrates weather updates, news notifications, and text-to-speech (TTS) functionality. It allows users to set alarms, receive timely updates, and interact with the system through a web interface.


### Key Features

#### 1. **Alarm Management**
- **Setting Alarms**:
  - Users can set alarms with labels, and optional weather/news notifications.
  - Alarms are stored persistently in a JSON database (`Announcements.json`).
- **Deleting Alarms**:
  - Users can remove alarms from the list, updating both the database and the user interface.

#### 2. **Notifications**
- **Automatic Notifications**:
  - Fetches and displays weather, COVID updates, and news articles.
  - Ensures no duplicate notifications are added to the interface.
- **User-Removable Notifications**:
  - Users can dismiss notifications, which are then removed from the active list.

#### 3. **Text-to-Speech (TTS)**
- **Announcement Playback**:
  - At the scheduled alarm time, the system uses TTS to announce the alarm label.
  - Optionally includes weather and news updates in the spoken announcement.

#### 4. **Data Handling**
- **API Integration**:
  - Fetches data from weather, news, and COVID APIs using custom functions.
- **Persistent Storage**:
  - Alarms and their configurations are stored in JSON format for later retrieval.

#### 5. **Web Interface**
- **Dynamic Rendering**:
  - Utilizes Flask templates (`index.html`) to present alarms and notifications dynamically.
- **Interactive Elements**:
  - Users can add, modify, or remove alarms and notifications directly from the web page.

#### 6. **Scheduler**
- **Alarm Scheduling**:
  - Converts alarm time into seconds for scheduling using the `sched` module.
  - Triggers announcements at the appropriate time without blocking other operations.

---

### Workflow

1. **Configuration Loading**:
   - Reads sensitive information (API keys, logging paths, image paths) from `config.json`.

2. **Main Application Logic**:
   - The `/` endpoint orchestrates:
     - Alarm generation and scheduling.
     - Notification fetching and deduplication.
     - Rendering the updated web interface.

3. **Notification Generation**:
   - Fetches and processes:
     - Weather updates from a specified location.
     - News articles based on a keyword and location.
     - COVID-19 updates.

4. **Alarm Management**:
   - Displays, saves, or removes alarms based on user interactions.
   - Validates alarm data before scheduling or saving.

5. **TTS Announcements**:
   - Builds a formatted announcement string including optional weather and news updates.
   - Reads the announcement aloud using `pyttsx3`.

---

### Key Strengths

1. **Modular Design**:
   - Functions are clearly defined for notifications, alarms, announcements, and data handling.
   - APIs and the scheduler are encapsulated for flexibility and reusability.

2. **Web Interface**:
   - A simple and user-friendly interface for managing alarms and notifications.
   - Real-time updates using Flask’s rendering capabilities.

3. **API Integration**:
   - Extends functionality by integrating weather, news, and COVID-19 APIs for contextual updates.

4. **Persistence**:
   - Uses JSON files to save alarms, ensuring data is retained across sessions.

5. **Logging**:
   - Implements structured logging for debugging and monitoring.

---

### Limitations

1. **Error Handling**:
   - Limited checks for API call failures or invalid configurations in `config.json`.

2. **Concurrency**:
   - The scheduler may encounter delays if multiple alarms are triggered simultaneously.

3. **Security**:
   - Sensitive information (e.g., API keys) is stored in a JSON file without encryption.

4. **Scalability**:
   - May struggle with large numbers of alarms or notifications due to reliance on simple data structures.

---

### Conclusion

The Smart Alarm Web Application effectively combines alarm management, notifications, and TTS into a cohesive system. With improvements in error handling, security, and scalability, it can be expanded for broader use cases beyond personal alarms.
