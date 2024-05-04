from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
import cv2
import numpy as np
from segment_enlarger import get_enlarged_segment

app = FastAPI()

@app.get("/enlarged")
async def enlarge_segment(file: UploadFile = File(...)):
    contents = await file.read()
    image = np.frombuffer(contents, np.uint8)
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)

    processed_image = get_enlarged_segment(image)
    _, image_encoded = cv2.imencode('.jpg', processed_image)
    
    return Response(content=image_encoded.tobytes(), media_type='image/jpeg')

def process_image(image):
    # Dummy function for image processing
    # Replace with actual Detectron2 and OpenCV manipulation
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)