import { useEffect, useRef, useState } from "react";
import { formatDate } from "../utils/formatDate";

export default function TodoItem({ todo, onToggle, onUpdate, onDelete }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(todo.task);
  const [saving, setSaving] = useState(false);
  const inputRef = useRef(null);

  useEffect(() => {
    if (isEditing && inputRef.current) {
      inputRef.current.focus();
      inputRef.current.select();
    }
  }, [isEditing]);

  function startEditing() {
    setEditText(todo.task);
    setIsEditing(true);
  }

  function cancelEditing() {
    setEditText(todo.task);
    setIsEditing(false);
  }

  async function handleSave(e) {
    e.preventDefault();
    const trimmed = editText.trim();
    if (!trimmed || saving) return;

    // Nothing changed, so just leave edit mode without a request.
    if (trimmed === todo.task) {
      setIsEditing(false);
      return;
    }

    setSaving(true);
    const saved = await onUpdate(todo.id, trimmed);
    setSaving(false);
    if (saved) setIsEditing(false);
  }

  function handleKeyDown(e) {
    if (e.key === "Escape") cancelEditing();
  }

  const wasUpdated = todo.updated_at !== todo.created_at;

  return (
    <li className={todo.completed ? "done" : ""}>
      <div className="todo-row">
        {isEditing ? (
          <form className="edit-form" onSubmit={handleSave}>
            <input
              ref={inputRef}
              type="text"
              value={editText}
              onChange={(e) => setEditText(e.target.value)}
              onKeyDown={handleKeyDown}
              maxLength={500}
              aria-label="edit task"
            />
            <button type="submit" className="save-btn" disabled={saving || !editText.trim()}>
              save
            </button>
            <button
              type="button"
              className="cancel-btn"
              onClick={cancelEditing}
              disabled={saving}
            >
              cancel
            </button>
          </form>
        ) : (
          <>
            <label>
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => onToggle(todo.id)}
              />
              <span>{todo.task}</span>
            </label>
            <div className="item-actions">
              <button
                className="icon-btn edit-btn"
                onClick={startEditing}
                aria-label="edit"
                title="Edit"
              >
                ✎
              </button>
              <button
                className="icon-btn delete-btn"
                onClick={() => onDelete(todo.id)}
                aria-label="delete"
                title="Delete"
              >
                ✕
              </button>
            </div>
          </>
        )}
      </div>

      <p className="todo-meta">
        Created: {formatDate(todo.created_at)}
        {wasUpdated && ` · Updated: ${formatDate(todo.updated_at)}`}
      </p>
    </li>
  );
}
