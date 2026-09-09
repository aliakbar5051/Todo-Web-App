export default function TodoItem({ todo, onToggle, onDelete }) {
  return (
    <li className={todo.done ? "done" : ""}>
      <label>
        <input
          type="checkbox"
          checked={todo.done}
          onChange={() => onToggle(todo.id)}
        />
        <span>{todo.text}</span>
      </label>
      <button
        className="delete-btn"
        onClick={() => onDelete(todo.id)}
        aria-label="delete"
      >
        ✕
      </button>
    </li>
  );
}
