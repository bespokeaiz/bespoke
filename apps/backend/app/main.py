from fastapi import FastAPI

app = FastAPI(title="Artist Market API")

@app.get("/health")
def health():
    return {"ok": True}
