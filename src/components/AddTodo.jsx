import { useState } from "react";

export default function AddTodo({ onAdd }) {
  const [text, setText] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!text.trim()) return;
    onAdd(text.trim());
    setText("");
  }

  return (
    <form onSubmit={handleSubmit} className="add-form">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="what needs doing?"
      />
      <button type="submit">add</button>
    </form>
  );
}
