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
    setSearchQuery,
    setFilter,
    addTodo,
    toggleTodo,
    deleteTodo,
    clearCompleted,
    removeAll,
  } = useTodos();

  return (
    <div className="app">
      <div className="card">
        <h1>my todos</h1>

        <AddTodo onAdd={addTodo} />

        {hasTodos && <Search value={searchQuery} onChange={setSearchQuery} />}
        {hasTodos && <Filter current={filter} onChange={setFilter} />}

        <TodoList todos={todos} onToggle={toggleTodo} onDelete={deleteTodo} />

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
