from fastapi import FastAPI, UploadFile, HTTPException
from starlette.responses import FileResponse
from moviepy.editor import *

app = FastAPI()

# Storage for audio and video files
audio_storage = {}
video_storage = {}
audio_id_counter = 0
video_id_counter = 0

@app.post("/upload-audio/")
async def upload_audio(audio: UploadFile = UploadFile(...), orientation: str = "panoramic"):
    global audio_id_counter
    audio_id_counter += 1

    # Save the audio file
    audio_filename = f"audio_{audio_id_counter}.mp3"
    audio_storage[audio_id_counter] = audio_filename
    with open(audio_filename, "wb") as buffer:
        buffer.write(audio.file.read())

    # Process the audio to create a video
    video_id = await create_video_from_audio(audio_id_counter, orientation)
    
    return {"audioId": audio_id_counter, "videoId": video_id}

async def create_video_from_audio(audio_id: int, orientation: str):
    global video_id_counter
    video_id_counter += 1

    audio_filename = audio_storage[audio_id]
    video_filename = f"video_{video_id_counter}.mp4"

    # Set video resolution based on orientation
    if orientation == "panoramic":
        resolution = (1280, 720)  # Example for panoramic
    elif orientation == "vertical":
        resolution = (720, 1280)  # Example for vertical
    else:
        raise HTTPException(status_code=400, detail="Invalid orientation")

    # CREATE THE VIDEO (NOT DONE YET)

    
    #video_storage[video_id_counter] = video_filename
    
    #Ereturn video_id_counter

@app.get("/get-video/{video_id}")
async def get_video(video_id: int):
    video_filename = video_storage.get(video_id)
    if not video_filename:
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(video_filename)
