from fastapi import FastAPI, HTTPException, Query, Request
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
import json
import uuid
import hashlib


# ---------- Storage paths ----------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "storage")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
REQUESTS_FILE = os.path.join(DATA_DIR, "requests.json")
PROJECTS_FILE = os.path.join(DATA_DIR, "projects.json")
COMMENTS_FILE = os.path.join(DATA_DIR, "comments.json")
os.makedirs(DATA_DIR, exist_ok=True)

# ---------- Password Hashing ----------
def get_password_hash(password: str) -> str:
    """Hashes a password for storage using SHA-256 with salt."""
    salt = "flashgig_salt_2024"
    return hashlib.sha256(f"{salt}{password}".encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed one."""
    return get_password_hash(plain_password) == hashed_password

# ---------- Helpers ----------
def load_json(path: str, default):
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return default

def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def now_iso() -> str:
    return datetime.utcnow().isoformat()

def get_user_or_404(username: str) -> Dict[str, Any]:
    users: List[Dict[str, Any]] = load_json(USERS_FILE, [])
    for u in users:
        if u.get("username") == username:
            return u
    raise HTTPException(status_code=404, detail="User not found")

# ---------- App ----------
app = FastAPI(title="FlashGig Local Server", version="0.1.2")

# ---------- User Endpoints ----------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/register", status_code=201)
async def register_user(request: Request) -> Dict[str, Any]:
    """Registers a new user."""
    try:
        data = await request.json()
        username = str(data.get("username", "")).strip()
        password = str(data.get("password", ""))

        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password are required")

        if len(username) < 3:
            raise HTTPException(status_code=400, detail="Username must be at least 3 characters")
        
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

        users: List[Dict[str, Any]] = load_json(USERS_FILE, [])

        for u in users:
            if u.get("username") == username:
                raise HTTPException(status_code=400, detail="Username already registered")

        user = {
            "id": str(uuid.uuid4()),
            "username": username,
            "hashed_password": get_password_hash(password),
            "created_at": now_iso(),
        }
        users.append(user)
        save_json(USERS_FILE, users)
        
        print(f"✓ User '{username}' registered successfully")
        return {"id": user["id"], "username": user["username"], "created_at": user["created_at"]}
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Registration error: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.post("/login")
async def login_user(request: Request) -> Dict[str, Any]:
    """Logs a user in by verifying their credentials."""
    try:
        data = await request.json()
        username = str(data.get("username", "")).strip()
        password = str(data.get("password", ""))

        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password are required")

        user = get_user_or_404(username)
        
        if not verify_password(password, user.get("hashed_password", "")):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        
        print(f"✓ User '{username}' logged in successfully")
        
        user_response = user.copy()
        user_response.pop("hashed_password", None)
        return user_response
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"✗ Login error: {e}")
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

@app.get("/users/{username}")
def get_user(username: str) -> Dict[str, Any]:
    user = get_user_or_404(username)
    user_response = user.copy()
    user_response.pop("hashed_password", None)
    return user_response

# ---------- Connection Request Endpoints ----------
@app.post("/requests", status_code=201)
async def create_request(request: Request) -> Dict[str, Any]:
    data = await request.json()
    from_username = str(data.get("from_username", "")).strip()
    to_username = str(data.get("to_username", "")).strip()
    project_name = str(data.get("project_name", "")).strip()

    if not from_username or not to_username or not project_name:
        raise HTTPException(status_code=400, detail="from_username, to_username and project_name are required")

    _ = get_user_or_404(from_username)
    _ = get_user_or_404(to_username)

    items: List[Dict[str, Any]] = load_json(REQUESTS_FILE, [])

    item = {
        "id": str(uuid.uuid4()),
        "from_username": from_username,
        "to_username": to_username,
        "project_name": project_name,
        "status": "requested",
        "created_at": now_iso(),
    }
    items.insert(0, item)
    save_json(REQUESTS_FILE, items)
    return item

@app.get("/requests")
def list_requests(user: str = Query(..., description="Filter by username")) -> List[Dict[str, Any]]:
    _ = get_user_or_404(user)
    items: List[Dict[str, Any]] = load_json(REQUESTS_FILE, [])
    return [r for r in items if r.get("from_username") == user or r.get("to_username") == user]

@app.patch("/requests/{req_id}")
async def update_request(req_id: str, request: Request) -> Dict[str, Any]:
    data = await request.json()
    status = data.get("status")

    items: List[Dict[str, Any]] = load_json(REQUESTS_FILE, [])
    for i, r in enumerate(items):
        if r.get("id") == req_id:
            if status is not None:
                if status not in ("requested", "accepted"):
                    raise HTTPException(status_code=400, detail="Invalid status")
                r["status"] = status
            items[i] = r
            save_json(REQUESTS_FILE, items)
            return r
    raise HTTPException(status_code=404, detail="Request not found")

# ---------- Project Endpoints ----------
@app.post("/projects", status_code=201)
async def create_project(request: Request) -> Dict[str, Any]:
    """Create a new project"""
    data = await request.json()
    request_id = str(data.get("request_id", "")).strip()
    title = str(data.get("title", "")).strip()
    description = str(data.get("description", "")).strip()
    
    if not request_id or not title:
        raise HTTPException(status_code=400, detail="request_id and title are required")
    
    # Verify the request exists and is accepted
    requests = load_json(REQUESTS_FILE, [])
    connection = None
    for r in requests:
        if r.get("id") == request_id:
            connection = r
            break
    
    if not connection:
        raise HTTPException(status_code=404, detail="Connection request not found")
    
    if connection.get("status") != "accepted":
        raise HTTPException(status_code=400, detail="Connection must be accepted first")
    
    projects = load_json(PROJECTS_FILE, [])
    
    project = {
        "id": str(uuid.uuid4()),
        "request_id": request_id,
        "title": title,
        "description": description,
        "status": "in_progress",
        "created_at": now_iso(),
    }
    
    projects.insert(0, project)
    save_json(PROJECTS_FILE, projects)
    return project

@app.get("/projects")
def list_projects(user: str = Query(..., description="Filter by user")) -> List[Dict[str, Any]]:
    """Get all projects for a user"""
    _ = get_user_or_404(user)
    
    # Get user's connections
    requests = load_json(REQUESTS_FILE, [])
    user_request_ids = [
        r["id"] for r in requests 
        if (r.get("from_username") == user or r.get("to_username") == user) 
        and r.get("status") == "accepted"
    ]
    
    # Get projects for those connections
    projects = load_json(PROJECTS_FILE, [])
    user_projects = [p for p in projects if p.get("request_id") in user_request_ids]
    
    return user_projects

@app.get("/projects/{project_id}")
def get_project(project_id: str) -> Dict[str, Any]:
    """Get a specific project"""
    projects = load_json(PROJECTS_FILE, [])
    for p in projects:
        if p.get("id") == project_id:
            return p
    raise HTTPException(status_code=404, detail="Project not found")

@app.patch("/projects/{project_id}")
async def update_project(project_id: str, request: Request) -> Dict[str, Any]:
    """Update project status or details"""
    data = await request.json()
    
    projects = load_json(PROJECTS_FILE, [])
    for i, p in enumerate(projects):
        if p.get("id") == project_id:
            # Update fields
            if "status" in data:
                p["status"] = data["status"]
            if "title" in data:
                p["title"] = data["title"]
            if "description" in data:
                p["description"] = data["description"]
            
            projects[i] = p
            save_json(PROJECTS_FILE, projects)
            return p
    
    raise HTTPException(status_code=404, detail="Project not found")

# ---------- Comment Endpoints ----------
@app.post("/comments", status_code=201)
async def create_comment(request: Request) -> Dict[str, Any]:
    """Add a comment to a project"""
    data = await request.json()
    project_id = str(data.get("project_id", "")).strip()
    username = str(data.get("username", "")).strip()
    text = str(data.get("text", "")).strip()
    timestamp = data.get("timestamp")  # Optional: for video/audio timestamps
    
    if not project_id or not username or not text:
        raise HTTPException(status_code=400, detail="project_id, username, and text are required")
    
    _ = get_user_or_404(username)
    
    comments = load_json(COMMENTS_FILE, [])
    
    comment = {
        "id": str(uuid.uuid4()),
        "project_id": project_id,
        "username": username,
        "text": text,
        "timestamp": timestamp,
        "created_at": now_iso(),
    }
    
    comments.insert(0, comment)
    save_json(COMMENTS_FILE, comments)
    return comment

@app.get("/comments")
def list_comments(project_id: str = Query(..., description="Project ID")) -> List[Dict[str, Any]]:
    """Get all comments for a project"""
    comments = load_json(COMMENTS_FILE, [])
    return [c for c in comments if c.get("project_id") == project_id]

# Run with:
#   pip install fastapi uvicorn
#   python -m uvicorn src.server:app --reload --port 8000