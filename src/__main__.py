from fastapi import FastAPI

app = FastAPI()

@app.get("/healthy", tags=["Health"])
def healthy():
    """Healthy check route"""
    return {"status": "Ok"}
