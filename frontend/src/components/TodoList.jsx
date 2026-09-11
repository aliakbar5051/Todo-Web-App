import TodoItem from "./TodoItem";

export default function TodoList({ todos, loading, onToggle, onUpdate, onDelete }) {
  if (loading) {
    return <p className="empty">loading todos...</p>;
  }

  if (todos.length === 0) {
    return <p className="empty">nothing here yet... add your first task!</p>;
  }

  return (
    <ul className="todo-list">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onUpdate={onUpdate}
          onDelete={onDelete}
        />
      ))}
    </ul>
  );
}
