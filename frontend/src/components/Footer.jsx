export default function Footer({ remaining }) {
  if (remaining === null) return null;

  return (
    <p className="footer-text">
      {remaining} {remaining === 1 ? "task" : "tasks"} left
    </p>
  );
}
