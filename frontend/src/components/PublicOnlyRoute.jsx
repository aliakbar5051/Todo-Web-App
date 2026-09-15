import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function PublicOnlyRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="app">
        <div className="card loading-card">
          <p className="loading-text">Loading...</p>
        </div>
      </div>
    );
  }

  if (isAuthenticated) {
    return <Navigate to="/todos" replace />;
  }

  return children;
}
