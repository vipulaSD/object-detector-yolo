import logging
from fastapi import FastAPI, UploadFile, File, HTTPException

from predictor import Predictor

app = FastAPI(title="Object recognizer using YOLOv3")
predictor = Predictor()

@app.post("/detect")
async def detect_objects(file: UploadFile = File(description="Upload image file")):
    if not file.content_type.startswith('image/'):
        logging.info('bad request from user')
        raise HTTPException(status_code=400, detail=f"File {file.filename} is not an image")

    content = await file.read()
    return predictor.make_predictions(content)
