export default function Search({ value, onChange }) {
  return (
    <div className="search-wrapper">
      <input
        type="text"
        className="search-input"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="search todos..."
      />
    </div>
  );
}
