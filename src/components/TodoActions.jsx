export default function TodoActions({ onClearCompleted, onRemoveAll, hasCompleted, hasTodos }) {
  if (!hasTodos) return null;

  return (
    <div className="todo-actions">
      {hasCompleted && (
        <button className="action-btn" onClick={onClearCompleted}>
          Clear Completed
        </button>
      )}
      <button className="action-btn action-btn--danger" onClick={onRemoveAll}>
        Remove All Todos
      </button>
    </div>
  );
}
