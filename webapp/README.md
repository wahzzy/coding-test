# Image Service
This is a lightweight, dependency-free web service built with FastAPI that allows users to:
1.	Upload an image and get a compressed version
2.	Query the processing history (stored in memory only)

# Installation
1. Install dependencies
```
pip install "fastapi[standard]"
```
2. Run the service
```
fastapi dev webapp/main.py
```

## Test
1. Manual test with curl
Test image compression
```
curl -X POST "http://127.0.0.1:8000/compress" -F "file=@your_file.png" --output compressed.png
```
Get processing history
```
curl -X GET "http://127.0.0.1:8000/history"
```