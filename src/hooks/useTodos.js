import { useState, useMemo } from "react";

export default function useTodos() {
  const [todos, setTodos] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filter, setFilter] = useState("all");

  function addTodo(text) {
    setTodos((prev) => [...prev, { id: Date.now(), text, done: false }]);
  }

  function toggleTodo(id) {
    setTodos((prev) =>
      prev.map((todo) =>
        todo.id === id ? { ...todo, done: !todo.done } : todo
      )
    );
  }

  function deleteTodo(id) {
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  }

  function clearCompleted() {
    setTodos((prev) => prev.filter((todo) => !todo.done));
  }

  function removeAll() {
    setTodos([]);
  }

  const filteredTodos = useMemo(() => {
    return todos.filter((todo) => {
      const matchesFilter =
        filter === "all" ||
        (filter === "completed" && todo.done) ||
        (filter === "pending" && !todo.done);

      const matchesSearch = todo.text
        .toLowerCase()
        .includes(searchQuery.toLowerCase());

      return matchesFilter && matchesSearch;
    });
  }, [todos, filter, searchQuery]);

  const remaining = todos.filter((t) => !t.done).length;
  const hasCompleted = todos.some((t) => t.done);
  const hasTodos = todos.length > 0;

  return {
    todos: filteredTodos,
    searchQuery,
    filter,
    remaining,
    hasCompleted,
    hasTodos,
    setSearchQuery,
    setFilter,
    addTodo,
    toggleTodo,
    deleteTodo,
    clearCompleted,
    removeAll,
  };
}
