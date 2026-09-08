import { useState } from "react";
import "./App.css";

function App() {
  const [todos, setTodos] = useState([]);
  const [text, setText] = useState("");

  function addTodo(e) {
    e.preventDefault();
    if (!text.trim()) return;

    setTodos([
      ...todos,
      { id: Date.now(), text: text.trim(), done: false },
    ]);
    setText("");
  }

  function toggleTodo(id) {
    setTodos(
      todos.map((todo) =>
        todo.id === id ? { ...todo, done: !todo.done } : todo
      )
    );
  }

  function deleteTodo(id) {
    setTodos(todos.filter((todo) => todo.id !== id));
  }

  const remaining = todos.filter((t) => !t.done).length;

  return (
    <div className="app">
      <div className="card">
        <h1>my todos</h1>

        <form onSubmit={addTodo} className="add-form">
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="what needs doing?"
          />
          <button type="submit">add</button>
        </form>

        {todos.length === 0 && (
          <p className="empty">nothing here yet... add your first task!</p>
        )}

        <ul className="todo-list">
          {todos.map((todo) => (
            <li key={todo.id} className={todo.done ? "done" : ""}>
              <label>
                <input
                  type="checkbox"
                  checked={todo.done}
                  onChange={() => toggleTodo(todo.id)}
                />
                <span>{todo.text}</span>
              </label>
              <button
                className="delete-btn"
                onClick={() => deleteTodo(todo.id)}
                aria-label="delete"
              >
                ✕
              </button>
            </li>
          ))}
        </ul>

        {todos.length > 0 && (
          <p className="footer-text">
            {remaining} {remaining === 1 ? "task" : "tasks"} left
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
