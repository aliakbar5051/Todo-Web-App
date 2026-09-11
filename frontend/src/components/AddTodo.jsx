import { useState } from "react";

export default function AddTodo({ onAdd }) {
  const [text, setText] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    const trimmed = text.trim();
    if (!trimmed) return;
    const added = await onAdd(trimmed);
    if (added) setText("");
  }

  return (
    <form onSubmit={handleSubmit} className="add-form">
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="what needs doing?"
        maxLength={500}
      />
      <button type="submit">add</button>
    </form>
  );
}
