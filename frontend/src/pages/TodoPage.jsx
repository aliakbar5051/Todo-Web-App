import AddTodo from "../components/AddTodo";
import Filter from "../components/Filter";
import Footer from "../components/Footer";
import Navbar from "../components/Navbar";
import Search from "../components/Search";
import TodoActions from "../components/TodoActions";
import TodoList from "../components/TodoList";
import useTodos from "../hooks/useTodos";

export default function TodoPage() {
  const {
    todos,
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
  } = useTodos();

  return (
    <div className="app">
      <div className="card">
        <Navbar />

        <div className="todo-header">
          <h1>my todos</h1>
        </div>

        <AddTodo onAdd={addTodo} />

        {error && <p className="error-banner">{error}</p>}

        {hasTodos && <Search value={searchQuery} onChange={setSearchQuery} />}
        {hasTodos && <Filter current={filter} onChange={setFilter} />}

        <TodoList
          todos={todos}
          loading={loading}
          onToggle={toggleTodo}
          onUpdate={updateTodo}
          onDelete={deleteTodo}
        />

        <TodoActions
          onClearCompleted={clearCompleted}
          onRemoveAll={removeAll}
          hasCompleted={hasCompleted}
          hasTodos={hasTodos}
        />

        <Footer remaining={hasTodos ? remaining : null} />
      </div>
    </div>
  );
}
