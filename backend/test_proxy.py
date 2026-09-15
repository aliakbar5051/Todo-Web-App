import httpx

client = httpx.Client(base_url="http://localhost:5173")

# 1. Test frontend dev server responds with HTML
resp = client.get("/")
assert resp.status_code == 200, f"Vite dev server failed: {resp.status_code}"
assert '<div id="root"></div>' in resp.text, "Root element not found in HTML"
print("✓ Frontend dev server serves React app correctly")

# 2. Test Vite proxy forwarding to backend
reg_resp = client.post("/api/auth/register", json={
    "name": "Clara Oswald",
    "email": "clara@example.com",
    "password": "Password123!"
})
print("✓ /api/auth/register proxied through Vite, status:", reg_resp.status_code)

login_resp = client.post("/api/auth/login", json={
    "email": "clara@example.com",
    "password": "Password123!"
})
assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
token = login_resp.json()["access_token"]
print("✓ /api/auth/login proxied through Vite, token received")

headers = {"Authorization": f"Bearer {token}"}

# 3. Test /api/todos proxied through Vite
todo_resp = client.post("/api/todos", json={"task": "Vite Proxy Task"}, headers=headers)
assert todo_resp.status_code == 201, f"Create todo failed: {todo_resp.text}"
todo = todo_resp.json()
print(f"✓ /api/todos POST proxied through Vite, created task id: {todo['id']}")

get_todos = client.get("/api/todos", headers=headers)
assert get_todos.status_code == 200
assert any(t["id"] == todo["id"] for t in get_todos.json())
print("✓ /api/todos GET proxied through Vite, retrieved successfully")

del_todo = client.delete(f"/api/todos/{todo['id']}", headers=headers)
assert del_todo.status_code == 204
print("✓ /api/todos DELETE proxied through Vite, deleted successfully")

print("\n✓ ALL VITE PROXY AND BACKEND INTEGRATION CHECKS PASSED!")
