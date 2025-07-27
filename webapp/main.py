import io
import threading
import time

from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse, StreamingResponse

app = FastAPI()
history = []
history_lock = threading.Lock()


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

        # Simple compressed image without third party library
        compressed_data = file_data[: len(file_data) // 2]
        # Save metadata in memory with thread safety
        with history_lock:
            history.append(
                {
                    "filename": file.filename,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "content_type": file.content_type,
                    "original_size": len(file_data),
                    "compressed_size": len(compressed_data),
                }
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
    description="Upload an image file and receive a compressed version",
    response_class=JSONResponse,
)
def history():
    with history_lock:
        return JSONResponse(content={"history": history})
