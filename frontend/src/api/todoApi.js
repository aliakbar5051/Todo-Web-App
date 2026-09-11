const BASE_URL = "/api/todos";

async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch {
    throw new Error("Cannot reach the server. Is the backend running?");
  }

  if (!response.ok) {
    throw new Error(await errorMessage(response));
  }

  if (response.status === 204) return null;
  return response.json();
}

async function errorMessage(response) {
  try {
    const body = await response.json();
    if (typeof body.detail === "string") return body.detail;
    if (Array.isArray(body.detail)) {
      return body.detail.map((issue) => issue.msg).join(", ");
    }
  } catch {
    // response had no JSON body
  }
  return `Request failed with status ${response.status}`;
}

export function fetchTodos() {
  return request("");
}

export function createTodo(task) {
  return request("", {
    method: "POST",
    body: JSON.stringify({ task, completed: false }),
  });
}

export function updateTodo(id, changes) {
  return request(`/${id}`, {
    method: "PUT",
    body: JSON.stringify(changes),
  });
}

export function deleteTodo(id) {
  return request(`/${id}`, { method: "DELETE" });
}

export function deleteAllTodos() {
  return request("", { method: "DELETE" });
}

export function deleteCompletedTodos() {
  return request("?completed_only=true", { method: "DELETE" });
}
