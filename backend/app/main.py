from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

BASE_DIR = "/srv/docker/volumes/group-N"

class PathRequest(BaseModel):
    path: str

@app.get("/volumes")
def list_volumes():
    try:
        directories = next(os.walk(BASE_DIR))[1]
        return {"directories": directories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing directories: {str(e)}")

@app.post("/volumes")
def create_volume(request: PathRequest):
    dir_path = os.path.join(BASE_DIR, request.path)
    
    if not request.path.isalnum():
        raise HTTPException(status_code=400, detail="Path contains invalid characters.")
    
    if os.path.exists(dir_path):
        raise HTTPException(status_code=400, detail="Directory already exists.")
    
    try:
        os.makedirs(dir_path)
        return {"message": "Directory created successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating directory: {str(e)}")

@app.delete("/volumes")
def delete_volume(request: PathRequest):
    dir_path = os.path.join(BASE_DIR, request.path)
    
    if not os.path.exists(dir_path):
        raise HTTPException(status_code=400, detail="Directory does not exist.")
    
    try:
        os.rmdir(dir_path)
        return {"message": "Directory deleted successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting directory: {str(e)}")
