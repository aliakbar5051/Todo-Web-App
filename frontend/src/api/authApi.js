const BASE_URL = "/api/auth";

async function errorMessage(response) {
  try {
    const body = await response.json();
    if (typeof body.detail === "string") return body.detail;
    if (Array.isArray(body.detail)) {
      return body.detail.map((issue) => issue.msg).join(", ");
    }
  } catch {
    // Non-JSON response
  }
  return `Request failed with status ${response.status}`;
}

export async function registerUser({ name, email, password }) {
  let response;
  try {
    response = await fetch(`${BASE_URL}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, email, password }),
    });
  } catch {
    throw new Error("Cannot reach the server. Is the backend running?");
  }

  if (!response.ok) {
    throw new Error(await errorMessage(response));
  }

  return response.json();
}

export async function loginUser({ email, password }) {
  let response;
  try {
    response = await fetch(`${BASE_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
  } catch {
    throw new Error("Cannot reach the server. Is the backend running?");
  }

  if (!response.ok) {
    throw new Error(await errorMessage(response));
  }

  return response.json();
}

export async function getMe(token) {
  let response;
  try {
    response = await fetch(`${BASE_URL}/me`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    });
  } catch {
    throw new Error("Cannot reach the server. Is the backend running?");
  }

  if (!response.ok) {
    throw new Error(await errorMessage(response));
  }

  return response.json();
}
