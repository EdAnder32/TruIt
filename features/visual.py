from fastapi import UploadFile, File, FastAPI
from pathlib import Path
import uuid

app = FastAPI()

@app.post("/upload_video")
async def download_video(file: UploadFile = File(...)):
    tmp_dir = Path("tmp/files")
    tmp_dir.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename).suffix
    file_name = f"{uuid.uuid4()}{extension}"
    file_location = tmp_dir / file_name

    chunk_size = 1024 * 1024
    size = 0
    with open(file_location, "wb") as buffer:
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            size += len(chunk)
            buffer.write(chunk)

    return {"status": "success", "filename": file_name, "size_bytes": size}
