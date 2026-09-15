import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <div className="navbar">
      <div className="user-profile">
        <div className="user-avatar" title={user?.email}>
          {user?.name ? user.name.charAt(0).toUpperCase() : "U"}
        </div>
        <div className="user-info">
          <span className="user-name">{user?.name || "User"}</span>
          <span className="user-email">{user?.email}</span>
        </div>
      </div>
      <button
        type="button"
        className="logout-btn"
        onClick={logout}
        title="Sign out of your account"
      >
        Sign out
      </button>
    </div>
  );
}
