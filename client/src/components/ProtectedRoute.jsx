// src/components/ProtectedRoute.jsx
// [AUTH DISABLED] - Protection removed, routes accessible to all
import React from "react";
// [AUTH DISABLED] import { Navigate } from "react-router-dom";
// [AUTH DISABLED] import { useAuth } from "../contexts/AuthContext";

const ProtectedRoute = ({ children }) => {
  // [AUTH DISABLED] const { isAuthenticated, isLoading } = useAuth();

  // [AUTH DISABLED] if (isLoading) {
  //   return (
  //     <div className="min-h-screen bg-gray-50 flex items-center justify-center">
  //       <div className="text-center">
  //         <div className="w-16 h-16 border-4 border-green-200 border-t-green-600 rounded-full animate-spin mx-auto mb-4"></div>
  //         <p className="text-gray-600">Checking authentication...</p>
  //       </div>
  //     </div>
  //   );
  // }

  // [AUTH DISABLED] if (!isAuthenticated) {
  //   return <Navigate to="/login" replace />;
  // }

  // ✅ BYPASS: Always render children (no authentication check)
  return children;
};

export default ProtectedRoute;
