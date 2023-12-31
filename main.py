from fastapi import File, UploadFile
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
from prediction import Prediction

prediction = Prediction()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/prediction")
def upload(file: UploadFile = File(...)):
    try:
        image_folder = "assets/images"
        if not os.path.exists(image_folder):
            os.makedirs(image_folder)
        image_path = os.path.join(image_folder, file.filename)
        with open(image_path, 'wb') as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    result = prediction.detect(file.filename)
    return result
