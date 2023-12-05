#!pip install scenedetect[opencv] --upgrade
#!pip install ffmpeg
from scenedetect import open_video, detect, AdaptiveDetector, split_video_ffmpeg, VideoManager, SceneManager, save_images
import ffmpeg

def videoProcessing():
    input_video_path = 'VF200827_113136_flv_middle_vojt.mp4'
    output_directory = 'output_directory'
    scene_list = detect(input_video_path, AdaptiveDetector())
    split_video_ffmpeg(input_video_path, scene_list)

    # získání obrázků -----------------------------
    video_stream = open_video(input_video_path)
    save_images(scene_list=scene_list, video=video_stream, num_images=1,
                image_name_template='Scene-$SCENE_NUMBER', output_dir='output')
    # Uvolní zdroje objektu VideoStream, jestliže existuje příslušná metoda.
    if hasattr(video_stream, 'release'):
        video_stream.release()
    elif hasattr(video_stream, 'close'):
        video_stream.close()
    # Pokud žádná z těchto metod neexistuje, Python uvolní objekt automaticky.

    return None



from fastapi import FastAPI
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()



@app.get("/get_image")
async def get_image():
    videoProcessing()
    image_path = Path("output/Scene-001.jpg")
    if not image_path.is_file():
        return {"error": "Image not found on the server"}
    return FileResponse(image_path)