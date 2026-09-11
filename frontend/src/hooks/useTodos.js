import { useEffect, useMemo, useState } from "react";
import * as todoApi from "../api/todoApi";

export default function useTodos() {
  const [todos, setTodos] = useState([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    todoApi
      .fetchTodos()
      .then((data) => {
        if (!cancelled) setTodos(data);
      })
      .catch((err) => {
        if (!cancelled) setError(err.message);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  async function addTodo(task) {
    try {
      const todo = await todoApi.createTodo(task);
      setTodos((prev) => [todo, ...prev]);
      setError(null);
      return true;
    } catch (err) {
      setError(err.message);
      return false;
    }
  }

  async function toggleTodo(id) {
    const todo = todos.find((t) => t.id === id);
    if (!todo) return;
    try {
      const updated = await todoApi.updateTodo(id, {
        completed: !todo.completed,
      });
      setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)));
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  }

  async function updateTodo(id, task) {
    try {
      const updated = await todoApi.updateTodo(id, { task });
      setTodos((prev) => prev.map((t) => (t.id === id ? updated : t)));
      setError(null);
      return true;
    } catch (err) {
      setError(err.message);
      return false;
    }
  }

  async function deleteTodo(id) {
    try {
      await todoApi.deleteTodo(id);
      setTodos((prev) => prev.filter((t) => t.id !== id));
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  }

  async function clearCompleted() {
    try {
      await todoApi.deleteCompletedTodos();
      setTodos((prev) => prev.filter((t) => !t.completed));
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  }

  async function removeAll() {
    try {
      await todoApi.deleteAllTodos();
      setTodos([]);
      setError(null);
    } catch (err) {
      setError(err.message);
    }
  }

  const filteredTodos = useMemo(() => {
    return todos.filter((todo) => {
      const matchesFilter =
        filter === "all" ||
        (filter === "completed" && todo.completed) ||
        (filter === "pending" && !todo.completed);

      const matchesSearch = todo.task
        .toLowerCase()
        .includes(searchQuery.toLowerCase());

      return matchesFilter && matchesSearch;
    });
  }, [todos, filter, searchQuery]);

  const remaining = todos.filter((t) => !t.completed).length;
  const hasCompleted = todos.some((t) => t.completed);
  const hasTodos = todos.length > 0;

  return {
    todos: filteredTodos,
    searchQuery,
    filter,
    remaining,
    hasCompleted,
    hasTodos,
    loading,
    error,
    setSearchQuery,
    setFilter,
    addTodo,
    toggleTodo,
    updateTodo,
    deleteTodo,
    clearCompleted,
    removeAll,
  };
}
