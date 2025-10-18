import json
import os
import urllib.request
import urllib.error
import urllib.parse
from typing import Dict, Any, Optional, List

SERVER_BASE = os.environ.get("SERVER_BASE", "http://127.0.0.1:8000")


class APIClientError(Exception):
    """Custom exception for API client errors."""
    pass


def _server_request(
    path: str,
    method: str,
    data: Optional[dict] = None,
    params: Optional[Dict[str, str]] = None,
) -> Optional[Dict | List]:
    """Generic helper to talk to the local server."""
    query_string = f"?{urllib.parse.urlencode(params)}" if params else ""
    url = f"{SERVER_BASE}{path}{query_string}"

    body = json.dumps(data).encode("utf-8") if data is not None else None
    headers = {"Content-Type": "application/json"} if body else {}

    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            response_text = resp.read().decode("utf-8")
            return json.loads(response_text) if response_text else None
    except urllib.error.HTTPError as e:
        error_message = f"HTTP Error {e.code}: {e.reason}"
        print(error_message)
        raise APIClientError(error_message) from e
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        raise APIClientError(error_message) from e


def server_get(path: str, params: Optional[Dict[str, str]] = None) -> Optional[Dict | List]:
    """Helper for GET requests."""
    return _server_request(path, "GET", params=params)


def server_post(path: str, data: dict) -> Optional[Dict | List]:
    """Helper for POST requests."""
    return _server_request(path, "POST", data=data)


def server_patch(path: str, data: dict) -> Optional[Dict | List]:
    """Helper for PATCH requests."""
    return _server_request(path, "PATCH", data=data)


# --- Convenience Functions ---

def get_user_connections(username: str) -> List[Dict[str, Any]]:
    """Get all connections for a user"""
    try:
        return server_get(f"/requests?user={username}") or []
    except APIClientError:
        return []


def get_user_projects(username: str) -> List[Dict[str, Any]]:
    """Get all projects for a user"""
    try:
        return server_get(f"/projects?user={username}") or []
    except APIClientError:
        return []


def get_project_comments(project_id: str) -> List[Dict[str, Any]]:
    """Get all comments for a project"""
    try:
        return server_get(f"/comments?project_id={project_id}") or []
    except APIClientError:
        return []


# --- Example Usage ---
if __name__ == "__main__":
    print("--- Testing API Client ---")

    try:
        # 1. Register a new user
        print("Attempting to register 'testuser'...")
        registration_data = server_post("/register", {"username": "testuser", "password": "password123"})
        print(f"Registered user: {registration_data}")

        # 2. Log in with that user
        print("\nAttempting to log in as 'testuser'...")
        login_data = server_post("/login", {"username": "testuser", "password": "password123"})
        print(f"Login successful: {login_data}")
        
        # 3. Get user connections
        print("\nFetching connections...")
        connections = get_user_connections("testuser")
        print(f"Connections: {connections}")

    except APIClientError as e:
        print(f"\nAn API error occurred: {e}")

    print("--- Test Complete ---")