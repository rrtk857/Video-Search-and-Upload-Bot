# Video Search and Upload Bot

A Python-based bot to search, download, and upload videos from social media platforms to a server using provided APIs.

## 🎯 Objective
The bot automates the process of:
- Searching and downloading videos from Instagram, TikTok, and Reddit.
- Uploading videos to a server using pre-signed URLs.
- Auto-deleting local files after upload.
- Monitoring the `/videos` directory for new `.mp4` files.

---

## 📋 Features
- **Search and Download**: Fetch videos from specified social media platforms.
- **Upload to Server**: Use pre-signed URLs for secure uploads.
- **Asynchronous Operations**: Concurrent processing for efficient uploads.
- **Auto File Cleanup**: Delete local files after successful uploads.
- **Directory Monitoring**: Watch `/videos` for new `.mp4` files.
- **Progress Bar**: Visualize upload progress with `tqdm`.

---

## 🚀 How It Works
1. **Fetch Upload URL**: The bot retrieves an upload URL from the API.
2. **Upload Video**: The video is uploaded to the pre-signed URL via a `PUT` request.
3. **Create Post**: Video metadata is submitted to the API to finalize the upload.
4. **File Cleanup**: Deletes the video from the local `/videos` directory.
5. **Repeat**: Monitors the `/videos` directory for additional `.mp4` files.

---

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.7 or higher.
- A valid **Flic-Token** from Empowerverse. Message their team on Telegram with your username to receive it.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/Video-Search-and-Upload-Bot.git
   cd Video-Search-and-Upload-Bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create the `/videos` directory:
   - Run the following command to create the directory manually:
     ```bash
     mkdir videos
     ```

4. Update the `Flic-Token`:
   - Replace the `<YOUR_TOKEN>` placeholder in the `HEADERS` dictionary inside `main.py` with your token.

### Running the Bot
1. Run the script:
   ```bash
   python main.py
   ```
2. Add `.mp4` files to the `/videos` directory to trigger processing.
3. Verify the uploads in the Empowerverse app under the "Super Feed" category.

---

## 📁 Project Structure
```
Video-Search-and-Upload-Bot/
├── main.py                # Main script
├── requirements.txt       # Dependencies
├── README.md              # Documentation
└── videos/                # Directory to monitor for .mp4 files
```

---

## 📝 API Details
### 1. **Get Upload URL**
- **Endpoint**: `https://api.socialverseapp.com/posts/generate-upload-url`
- **Headers**:
  ```json
  {
    "Flic-Token": "<YOUR_TOKEN>",
    "Content-Type": "application/json"
  }
  ```

### 2. **Upload Video**
- **Method**: `PUT`
- **URL**: Use the pre-signed URL returned by Step 1.

### 3. **Create Post**
- **Endpoint**: `https://api.socialverseapp.com/posts`
- **Headers**:
  ```json
  {
    "Flic-Token": "<YOUR_TOKEN>",
    "Content-Type": "application/json"
  }
  ```
- **Body**:
  ```json
  {
    "title": "<video title>",
    "hash": "<hash from Step 1>",
    "is_available_in_public_feed": false,
    "category_id": <category_id>
  }
  ```

---

## 🧹 Cleanup
The bot automatically deletes processed `.mp4` files from the `/videos` directory after a successful upload.

---
