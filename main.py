import time
import uuid
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ---- YOUR SETTINGS ----
YOUR_EMAIL = "24f2000626@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-tmu0ua.example.com"

# ---- STEP A: CORS ----
# This is FastAPI's built-in tool for the "which websites can call me" rule.
# We give it a LIST containing only our one allowed origin (no "*").
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],   # only this origin gets the header
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# ---- STEP B: Custom middleware for X-Request-ID and X-Process-Time ----
# Middleware = a function that wraps EVERY request/response.
@app.middleware("http")
async def add_custom_headers(request: Request, call_next):
    start_time = time.time()          # note the time before we do any work
    request_id = str(uuid.uuid4())    # generate a random unique ID

    response = await call_next(request)  # this actually runs your endpoint code

    process_time = time.time() - start_time  # how long the endpoint took
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.6f}"
    return response

# ---- STEP C: The actual /stats endpoint ----
@app.get("/stats")
def get_stats(values: str = Query(...)):
    # values arrives as a string like "1,2,3,4"
    # Split on commas, strip whitespace, convert each piece to an int
    numbers = [int(v.strip()) for v in values.split(",") if v.strip() != ""]

    count = len(numbers)
    total = sum(numbers)
    minimum = min(numbers)
    maximum = max(numbers)
    mean = total / count

    return {
        "email": YOUR_EMAIL,
        "count": count,
        "sum": total,
        "min": minimum,
        "max": maximum,
        "mean": mean,
    }
