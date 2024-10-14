# body-segmentation-ai
body segmentation ML project with image manipulation

enlarges a specific body part using machine learning

- Jupyter Notebook for training, Detectron2 Mask R-CNN model for segmentation and openCV for image processing
- FastAPI, Python for backend
- Next, Tailwind, TS for frontend

Backend Setup:
```
1. cd backend
2. python -m venv env
3. env/Scripts/activate
4. pip install -r requirements.txt
5. git clone https://github.com/facebookresearch/detectron2.git
6. python -m pip install -e detectron2
7. uvicorn main:app
```
Frontend Setup:
```
1. cd frontend
2. npm install
3. npm run dev (developer mode)
4. npm run build
5. npm run start
```
