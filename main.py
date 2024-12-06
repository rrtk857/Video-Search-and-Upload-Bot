import os
import asyncio
import aiohttp
import aiofiles
from aiohttp import ClientSession
from hashlib import sha256
from tqdm import tqdm

# Constants
BASE_API_URL = "https://api.socialverseapp.com"
HEADERS = {
    "Flic-Token": "<YOUR_TOKEN>",  
    "Content-Type": "application/json"
}
VIDEO_DIR = "./videos"

async def fetch_upload_url(session: ClientSession):
    """Fetches the pre-signed upload URL."""
    url = f"{BASE_API_URL}/posts/generate-upload-url"
    async with session.post(url, headers=HEADERS) as response:
        if response.status == 200:
            return await response.json()
        else:
            print(f"Error fetching upload URL: {response.status}")
            return None

async def upload_video(session: ClientSession, video_path: str, upload_url: str):
    """Uploads a video to the pre-signed URL."""
    async with aiofiles.open(video_path, 'rb') as file:
        data = await file.read()
    async with session.put(upload_url, data=data) as response:
        if response.status == 200:
            print(f"Uploaded {os.path.basename(video_path)} successfully.")
            return True
        else:
            print(f"Failed to upload {os.path.basename(video_path)}. Status: {response.status}")
            return False

async def create_post(session: ClientSession, title: str, video_hash: str, category_id: int):
    """Creates a post with the uploaded video information."""
    url = f"{BASE_API_URL}/posts"
    payload = {
        "title": title,
        "hash": video_hash,
        "is_available_in_public_feed": False,
        "category_id": category_id,
    }
    async with session.post(url, headers=HEADERS, json=payload) as response:
        if response.status == 201:
            print(f"Post created successfully: {title}")
        else:
            print(f"Error creating post: {response.status}")

async def calculate_file_hash(file_path: str):
    """Calculates the SHA256 hash of a file."""
    hash_sha256 = sha256()
    async with aiofiles.open(file_path, 'rb') as file:
        while chunk := await file.read(8192):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

async def process_video(file_path: str, session: ClientSession, category_id: int):
    """Handles the complete workflow for a single video."""
    upload_data = await fetch_upload_url(session)
    if not upload_data:
        return

    upload_url = upload_data['upload_url']
    video_hash = upload_data['hash']

    if await upload_video(session, file_path, upload_url):
        title = os.path.basename(file_path)
        await create_post(session, title, video_hash, category_id)
        os.remove(file_path)
        print(f"Deleted local file: {file_path}")

async def monitor_directory():
    """Monitors the /videos directory for new .mp4 files."""
    async with aiohttp.ClientSession() as session:
        while True:
            video_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.mp4')]
            for video in video_files:
                video_path = os.path.join(VIDEO_DIR, video)
                await process_video(video_path, session, category_id=1)  
            await asyncio.sleep(5)

if __name__ == "__main__":
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)

    print("Starting video bot...")
    asyncio.run(monitor_directory())
