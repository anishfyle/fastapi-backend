from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
import sqlite3
from datetime import datetime

app = FastAPI(title="URL Shortener Service", version="1.0.0")
DATABASE = "urls.db"


# Pydantic model for request validation
class URLRequest(BaseModel):
    long_url: HttpUrl


# Base62 character set for encoding
BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def encode_base62(num: int) -> str:
    """
    Encode a positive integer to Base62 string.
    Uses characters: 0-9, A-Z, a-z (62 total characters)
    """
    if num == 0:
        return BASE62[0]
    encoded = ""
    while num > 0:
        num, rem = divmod(num, 62)
        encoded = BASE62[rem] + encoded
    return encoded


def get_db():
    """
    Create and return a database connection with Row factory.
    This allows accessing columns by name.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.on_event("startup")
def setup_db():
    """
    Initialize the database on application startup.
    Creates the urls table if it doesn't exist.
    """
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            long_url TEXT NOT NULL,
            short_code TEXT UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()
    print("✓ Database initialized successfully")


@app.get("/")
def read_root():
    """
    Root endpoint - provides API information
    """
    return {
        "message": "URL Shortener API",
        "endpoints": {
            "POST /shorten": "Shorten a long URL",
            "GET /{short_code}": "Redirect to original URL"
        }
    }


@app.post("/shorten")
def shorten_url(request: URLRequest):
    """
    Shorten a long URL and return the shortened version.
    
    - Checks if URL already exists in database
    - If yes, returns existing short code
    - If no, creates new entry with Base62 encoded ID as short code
    """
    conn = get_db()
    cur = conn.cursor()

    # Check if URL already exists
    existing = cur.execute(
        "SELECT short_code FROM urls WHERE long_url = ?", 
        (str(request.long_url),)
    ).fetchone()
    
    if existing:
        conn.close()
        return {"short_url": f"http://localhost:8000/{existing['short_code']}"}

    # Insert new record
    cur.execute("INSERT INTO urls (long_url) VALUES (?)", (str(request.long_url),))
    conn.commit()

    # Fetch ID and generate Base62 short code
    new_id = cur.lastrowid
    if new_id is None:
        conn.close()
        raise HTTPException(status_code=500, detail="Failed to create short URL")
    
    short_code = encode_base62(new_id)

    # Update record with short_code
    cur.execute("UPDATE urls SET short_code = ? WHERE id = ?", (short_code, new_id))
    conn.commit()
    conn.close()

    return {"short_url": f"http://localhost:8000/{short_code}"}


@app.get("/{short_code}")
def resolve_url(short_code: str):
    """
    Resolve a short code and redirect to the original long URL.
    
    - Queries database for the short code
    - If found, redirects to original URL
    - If not found, returns 404 error
    """
    conn = get_db()
    cur = conn.cursor()

    result = cur.execute(
        "SELECT long_url FROM urls WHERE short_code = ?", 
        (short_code,)
    ).fetchone()
    conn.close()

    if not result:
        raise HTTPException(status_code=404, detail="Short URL not found")

    # Redirect to the original URL
    return RedirectResponse(url=result["long_url"], status_code=307)