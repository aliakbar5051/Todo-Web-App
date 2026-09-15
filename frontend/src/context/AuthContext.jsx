import { createContext, useContext, useEffect, useState } from "react";
import * as authApi from "../api/authApi";
import { getStoredToken, setStoredToken } from "../api/todoApi";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => getStoredToken());
  const [loading, setLoading] = useState(true);

  // Validate session on mount if a token exists
  useEffect(() => {
    let cancelled = false;

    async function verifySession() {
      const stored = getStoredToken();
      if (!stored) {
        setLoading(false);
        return;
      }

      try {
        const userData = await authApi.getMe(stored);
        if (!cancelled) {
          setUser(userData);
          setToken(stored);
        }
      } catch {
        if (!cancelled) {
          setStoredToken(null);
          setToken(null);
          setUser(null);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    verifySession();

    // Listen for unauthorized 401 events from any API call
    function handleUnauthorized() {
      setStoredToken(null);
      setToken(null);
      setUser(null);
    }

    window.addEventListener("auth:unauthorized", handleUnauthorized);

    return () => {
      cancelled = true;
      window.removeEventListener("auth:unauthorized", handleUnauthorized);
    };
  }, []);

  async function login(email, password) {
    const data = await authApi.loginUser({ email, password });
    setStoredToken(data.access_token);
    setToken(data.access_token);
    setUser(data.user);
    return data.user;
  }

  async function register(name, email, password) {
    return await authApi.registerUser({ name, email, password });
  }

  function logout() {
    setStoredToken(null);
    setToken(null);
    setUser(null);
  }

  const value = {
    user,
    token,
    loading,
    isAuthenticated: Boolean(token && user),
    login,
    register,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
