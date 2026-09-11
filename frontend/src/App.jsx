import "./App.css";
import useTodos from "./hooks/useTodos";
import AddTodo from "./components/AddTodo";
import Search from "./components/Search";
import Filter from "./components/Filter";
import TodoList from "./components/TodoList";
import TodoActions from "./components/TodoActions";
import Footer from "./components/Footer";

function App() {
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
        <h1>my todos</h1>

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

export default App;
