import sys
from datetime import timedelta
from pathlib import Path

# Add backend dir to sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from sqlalchemy import text

from core.security import create_access_token
from database import engine
from main import app

client = TestClient(app)


def run_tests():
    print("\n" + "=" * 60)
    print("RUNNING COMPLETE AUTHENTICATION & ISOLATION TEST SUITE")
    print("=" * 60)

    # Clean up test users if existing
    with engine.begin() as conn:
        conn.execute(
            text("DELETE FROM users WHERE email IN ('usera@example.com', 'userb@example.com')")
        )

    # ----------------------------------------------------
    # Test 1: Register User A
    # ----------------------------------------------------
    print("\n[Test 1] Register User A...")
    resp_reg_a = client.post(
        "/api/auth/register",
        json={"name": "Alice User", "email": "usera@example.com", "password": "Password123!"},
    )
    assert resp_reg_a.status_code == 201, f"Failed: {resp_reg_a.text}"
    user_a_data = resp_reg_a.json()
    assert user_a_data["email"] == "usera@example.com"
    assert "password" not in user_a_data
    assert "password_hash" not in user_a_data
    print("  -> Passed: User A registered (id:", user_a_data["id"], ")")

    # Duplicate registration test (Requirement 1 error check)
    print("  -> Verifying duplicate registration rejection (409 Conflict)...")
    dup_resp = client.post(
        "/api/auth/register",
        json={"name": "Alice Duplicate", "email": "usera@example.com", "password": "Password123!"},
    )
    assert dup_resp.status_code == 409, f"Expected 409, got {dup_resp.status_code}"
    print("  -> Passed: Duplicate registration correctly rejected with 409.")

    # ----------------------------------------------------
    # Test 2: Register User B
    # ----------------------------------------------------
    print("\n[Test 2] Register User B...")
    resp_reg_b = client.post(
        "/api/auth/register",
        json={"name": "Bob User", "email": "userb@example.com", "password": "SecurePassword456!"},
    )
    assert resp_reg_b.status_code == 201, f"Failed: {resp_reg_b.text}"
    user_b_data = resp_reg_b.json()
    assert user_b_data["email"] == "userb@example.com"
    assert "password" not in user_b_data
    assert "password_hash" not in user_b_data
    print("  -> Passed: User B registered (id:", user_b_data["id"], ")")

    # ----------------------------------------------------
    # Test 3: Login as User A
    # ----------------------------------------------------
    print("\n[Test 3] Login as User A...")
    resp_login_a = client.post(
        "/api/auth/login",
        json={"email": "usera@example.com", "password": "Password123!"},
    )
    assert resp_login_a.status_code == 200, f"Failed: {resp_login_a.text}"
    token_data_a = resp_login_a.json()
    token_a = token_data_a["access_token"]
    assert token_a, "No access_token returned"
    headers_a = {"Authorization": f"Bearer {token_a}"}
    print("  -> Passed: User A logged in successfully. Received JWT token.")

    # Test invalid login credentials rejection
    print("  -> Verifying invalid credentials rejection (401 Unauthorized)...")
    bad_login = client.post(
        "/api/auth/login",
        json={"email": "usera@example.com", "password": "WrongPassword!"},
    )
    assert bad_login.status_code == 401
    assert bad_login.json()["detail"] == "Invalid email or password."
    print("  -> Passed: Generic error message returned without information leakage.")

    # ----------------------------------------------------
    # Test 4: Create multiple todos as User A
    # ----------------------------------------------------
    print("\n[Test 4] Create multiple todos as User A...")
    todo_a1_resp = client.post("/api/todos", json={"task": "Alice Task 1"}, headers=headers_a)
    assert todo_a1_resp.status_code == 201
    todo_a1 = todo_a1_resp.json()

    todo_a2_resp = client.post("/api/todos", json={"task": "Alice Task 2"}, headers=headers_a)
    assert todo_a2_resp.status_code == 201
    todo_a2 = todo_a2_resp.json()

    todo_a3_resp = client.post("/api/todos", json={"task": "Alice Task 3"}, headers=headers_a)
    assert todo_a3_resp.status_code == 201
    todo_a3 = todo_a3_resp.json()

    alice_todos_resp = client.get("/api/todos", headers=headers_a)
    assert alice_todos_resp.status_code == 200
    assert len(alice_todos_resp.json()) == 3
    print("  -> Passed: User A created 3 todos:", [t["id"] for t in alice_todos_resp.json()])

    # ----------------------------------------------------
    # Test 5: Logout and login as User B
    # ----------------------------------------------------
    print("\n[Test 5] Login as User B...")
    resp_login_b = client.post(
        "/api/auth/login",
        json={"email": "userb@example.com", "password": "SecurePassword456!"},
    )
    assert resp_login_b.status_code == 200, f"Failed: {resp_login_b.text}"
    token_b = resp_login_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    print("  -> Passed: User B logged in successfully.")

    # ----------------------------------------------------
    # Test 6: Verify User B cannot see User A's todos
    # ----------------------------------------------------
    print("\n[Test 6] Verify User B cannot see User A's todos...")
    bob_todos_resp = client.get("/api/todos", headers=headers_b)
    assert bob_todos_resp.status_code == 200
    bob_todos = bob_todos_resp.json()
    assert len(bob_todos) == 0, f"Expected 0 todos for Bob, found: {bob_todos}"
    print("  -> Passed: User B sees 0 todos (User A's todos are completely hidden).")

    # ----------------------------------------------------
    # Test 7: Create todos as User B
    # ----------------------------------------------------
    print("\n[Test 7] Create todos as User B...")
    todo_b1_resp = client.post("/api/todos", json={"task": "Bob Task 1"}, headers=headers_b)
    assert todo_b1_resp.status_code == 201
    todo_b1 = todo_b1_resp.json()

    todo_b2_resp = client.post("/api/todos", json={"task": "Bob Task 2"}, headers=headers_b)
    assert todo_b2_resp.status_code == 201
    todo_b2 = todo_b2_resp.json()

    bob_todos_resp = client.get("/api/todos", headers=headers_b)
    assert len(bob_todos_resp.json()) == 2
    print("  -> Passed: User B created 2 todos:", [t["id"] for t in bob_todos_resp.json()])

    # ----------------------------------------------------
    # Test 8: Verify User A can only see User A's todos after logging back in
    # ----------------------------------------------------
    print("\n[Test 8] Verify User A only sees User A's todos...")
    alice_check = client.get("/api/todos", headers=headers_a)
    alice_items = alice_check.json()
    assert len(alice_items) == 3
    alice_ids = {t["id"] for t in alice_items}
    assert todo_a1["id"] in alice_ids
    assert todo_a2["id"] in alice_ids
    assert todo_a3["id"] in alice_ids
    assert todo_b1["id"] not in alice_ids
    assert todo_b2["id"] not in alice_ids
    print("  -> Passed: User A sees only User A's 3 todos and none of User B's.")

    # ----------------------------------------------------
    # Test 9: Try to update a Todo belonging to another user (IDOR rejection)
    # ----------------------------------------------------
    print("\n[Test 9] User B attempts to UPDATE User A's todo (IDOR test)...")
    idor_put_resp = client.put(
        f"/api/todos/{todo_a1['id']}",
        json={"task": "Hacked by Bob!", "completed": True},
        headers=headers_b,
    )
    assert idor_put_resp.status_code == 404, f"Expected 404, got {idor_put_resp.status_code}"
    # Verify task was NOT modified
    verify_a1 = client.get("/api/todos", headers=headers_a).json()
    task_a1_curr = next(t for t in verify_a1 if t["id"] == todo_a1["id"])
    assert task_a1_curr["task"] == "Alice Task 1"
    assert task_a1_curr["completed"] is False
    print("  -> Passed: Update rejected with 404 Not Found. Data is intact.")

    # ----------------------------------------------------
    # Test 10: Try to delete another user's todo (IDOR rejection)
    # ----------------------------------------------------
    print("\n[Test 10] User B attempts to DELETE User A's todo (IDOR test)...")
    idor_del_resp = client.delete(f"/api/todos/{todo_a1['id']}", headers=headers_b)
    assert idor_del_resp.status_code == 404, f"Expected 404, got {idor_del_resp.status_code}"
    # Verify still exists for Alice
    verify_a1_still = client.get("/api/todos", headers=headers_a).json()
    assert any(t["id"] == todo_a1["id"] for t in verify_a1_still)
    print("  -> Passed: Delete rejected with 404 Not Found. Alice's todo is safe.")

    # ----------------------------------------------------
    # Test 11: Test Remove All Todos (only removes current user's todos)
    # ----------------------------------------------------
    print("\n[Test 11] Test Remove All Todos for User B...")
    del_all_b = client.delete("/api/todos", headers=headers_b)
    assert del_all_b.status_code == 200
    assert del_all_b.json()["deleted"] == 2

    bob_after_del = client.get("/api/todos", headers=headers_b).json()
    assert len(bob_after_del) == 0

    alice_after_b_del = client.get("/api/todos", headers=headers_a).json()
    assert len(alice_after_b_del) == 3
    print("  -> Passed: User B's todos removed, User A's 3 todos remain untouched.")

    # ----------------------------------------------------
    # Test 12: Test expired / invalid JWT
    # ----------------------------------------------------
    print("\n[Test 12] Test expired/invalid JWT tokens...")
    # 1) Missing token
    resp_no_token = client.get("/api/todos")
    assert resp_no_token.status_code == 401
    print("  -> 12a: Missing token returned 401")

    # 2) Tampered/invalid token
    resp_bad_token = client.get(
        "/api/todos",
        headers={"Authorization": "Bearer invalid.token.value"},
    )
    assert resp_bad_token.status_code == 401
    print("  -> 12b: Invalid token returned 401")

    # 3) Expired token
    expired_token = create_access_token(
        data={"sub": str(user_a_data["id"])},
        expires_delta=timedelta(seconds=-10),  # expired 10s ago
    )
    resp_expired = client.get(
        "/api/todos",
        headers={"Authorization": f"Bearer {expired_token}"},
    )
    assert resp_expired.status_code == 401
    assert "expired" in resp_expired.json()["detail"].lower()
    print("  -> 12c: Expired token returned 401 with appropriate message")

    # ----------------------------------------------------
    # Test 13: Verify passwords stored only as hashes in PostgreSQL
    # ----------------------------------------------------
    print("\n[Test 13] Inspect PostgreSQL to confirm password hashing...")
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT email, password_hash FROM users WHERE email IN ('usera@example.com', 'userb@example.com')")
        ).fetchall()
        for row in result:
            email, pwd_hash = row[0], row[1]
            assert "Password123!" not in pwd_hash
            assert "SecurePassword456!" not in pwd_hash
            assert pwd_hash.startswith("$argon2"), f"Hash is not Argon2 format: {pwd_hash}"
            print(f"  -> User {email} stored password hash: {pwd_hash[:30]}...")
    print("  -> Passed: All passwords stored strictly as Argon2 hashes.")

    print("\n" + "=" * 60)
    print("ALL 13 TESTS PASSED PERFECTLY!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    run_tests()
