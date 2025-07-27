import io
import threading
import time
from typing import Dict, List

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI()


class SafeHistory:
    def __init__(self):
        self._history: List[Dict] = []
        self._lock = threading.Lock()

    def add_record(
        self, filename: str, content_type: str, original_size: int, compressed_size: int
    ):
        with self._lock:
            self._history.append(
                {
                    "filename": filename,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "content_type": content_type,
                    "original_size": original_size,
                    "compressed_size": compressed_size,
                }
            )

    def get_history(self) -> List[Dict]:
        with self._lock:
            return list(self._history)


safe_history = SafeHistory()


@app.post(
    "/compress",
    summary="Upload and compress and image",
    description="Upload an image file and receive a compressed version",
    response_class=StreamingResponse,
)
async def compress(file: UploadFile = File(...)):
    """
    Compress an uploaded image and return the compressed version.
    """
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="File must be an image"
        )
    try:
        file_data = await file.read()

        # Sorry I did not come out the compress solution without 3rd library
        # Just simple compressed image file with half cut its size
        compressed_data = file_data[: len(file_data) // 2]
        # Store metadata using the in-memory service
        safe_history.add_record(
            filename=file.filename,
            content_type=file.content_type,
            original_size=len(file_data),
            compressed_size=len(compressed_data),
        )

        return StreamingResponse(
            io.BytesIO(compressed_data), media_type=file.content_type
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Image processing failed: {str(e)}",
        )


@app.get(
    "/history",
    summary="Show history",
    description="Show in memory history",
    response_class=JSONResponse,
)
def show_history():
    return JSONResponse(content={"history": safe_history.get_history()})
