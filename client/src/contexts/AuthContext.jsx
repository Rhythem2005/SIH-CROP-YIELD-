// src/contexts/AuthContext.jsx
// [AUTH DISABLED - All authentication code commented out]
import React, { createContext, useContext, useEffect, useState } from "react";

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  // [AUTH DISABLED] const [isAuthenticated, setIsAuthenticated] = useState(false);
  // [AUTH DISABLED] const [user, setUser] = useState(null);
  // [AUTH DISABLED] const [isLoading, setIsLoading] = useState(true);

  // ✅ BYPASS: Always consider user as authenticated (no actual auth)
  const [isAuthenticated] = useState(true);
  const [user] = useState({ name: "User", email: "user@farmwise.local" });
  const [isLoading] = useState(false);

  // [AUTH DISABLED] const checkAuthStatus = () => {
  //   try {
  //     const token = localStorage.getItem("token");
  //     const userData = localStorage.getItem("userData");
  //     
  //     if (token && userData) {
  //       setIsAuthenticated(true);
  //       setUser(JSON.parse(userData));
  //     } else {
  //       setIsAuthenticated(false);
  //       setUser(null);
  //     }
  //   } catch (error) {
  //     console.error("Auth check failed:", error);
  //     setIsAuthenticated(false);
  //     setUser(null);
  //   } finally {
  //     setIsLoading(false);
  //   }
  // };

  // [AUTH DISABLED] const login = (token, userData) => {
  //   localStorage.setItem("token", token);
  //   localStorage.setItem("userData", JSON.stringify(userData));
  //   setIsAuthenticated(true);
  //   setUser(userData);
  // };

  // [AUTH DISABLED] const logout = () => {
  //   localStorage.removeItem("token");
  //   localStorage.removeItem("userData");
  //   setIsAuthenticated(false);
  //   setUser(null);
  // };

  // [AUTH DISABLED] useEffect(() => {
  //   checkAuthStatus();
  // }, []);

  const value = {
    isAuthenticated,
    user,
    isLoading,
    // [AUTH DISABLED] login,
    // [AUTH DISABLED] logout,
    // [AUTH DISABLED] checkAuthStatus
    login: () => {}, // Stub function
    logout: () => {}, // Stub function
    checkAuthStatus: () => {}, // Stub function
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// [AUTH DISABLED] src/utils/auth.js - All functions commented out
// export const isAuthenticated = () => {
//   try {
//     const token = localStorage.getItem("token");
//     return !!token;
//   } catch (error) {
//     return false;
//   }
// };

// export const getAuthToken = () => {
//   try {
//     return localStorage.getItem("token");
//   } catch (error) {
//     return null;
//   }
// };

// export const getUserData = () => {
//   try {
//     const userData = localStorage.getItem("userData");
//     return userData ? JSON.parse(userData) : null;
//   } catch (error) {
//     return null;
//   }
// };

// export const clearAuthData = () => {
//   try {
//     localStorage.removeItem("token");
//     localStorage.removeItem("userData");
//   } catch (error) {
//     console.error("Error clearing auth data:", error);
//   }
// };