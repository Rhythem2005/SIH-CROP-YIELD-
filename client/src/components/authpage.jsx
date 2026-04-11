// src/pages/AuthPage.jsx
// [AUTH DISABLED] - Authentication completely disabled
import { useState } from "react";
import { FaEnvelope, FaLock, FaUser } from "react-icons/fa";
import { useNavigate } from "react-router-dom";
// [AUTH DISABLED] import { Navigate } from "react-router-dom";
import { useTranslation } from "react-i18next";
// [AUTH DISABLED] import { useAuth } from "../contexts/AuthContext";

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [formData, setFormData] = useState({ name: "", email: "", password: "", confirmPassword: "" });
  // [AUTH DISABLED] const [message, setMessage] = useState("");
  // [AUTH DISABLED] const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { t } = useTranslation();
  // [AUTH DISABLED] const { login, isAuthenticated } = useAuth();

  // [AUTH DISABLED] // If already authenticated, redirect to home
  // [AUTH DISABLED] if (isAuthenticated) {
  // [AUTH DISABLED]   return <Navigate to="/" replace />;
  // [AUTH DISABLED] }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    // [AUTH DISABLED] setMessage("");
    // [AUTH DISABLED] setIsLoading(true);

    // [AUTH DISABLED] // Validation for signup
    // [AUTH DISABLED] if (!isLogin && formData.password !== formData.confirmPassword) {
    // [AUTH DISABLED]   setMessage("Passwords do not match");
    // [AUTH DISABLED]   setIsLoading(false);
    // [AUTH DISABLED]   return;
    // [AUTH DISABLED] }

    // [AUTH DISABLED] try {
    // [AUTH DISABLED]   const url = isLogin ? "http://127.0.0.1:8000/login" : "http://127.0.0.1:8000/signup";
    // [AUTH DISABLED]   const body = isLogin
    // [AUTH DISABLED]     ? { email: formData.email, password: formData.password }
    // [AUTH DISABLED]     : { username: formData.name, email: formData.email, password: formData.password };

    // [AUTH DISABLED]   const res = await fetch(url, {
    // [AUTH DISABLED]     method: "POST",
    // [AUTH DISABLED]     headers: { "Content-Type": "application/json" },
    // [AUTH DISABLED]     body: JSON.stringify(body),
    // [AUTH DISABLED]   });

    // [AUTH DISABLED]   const data = await res.json();

    // [AUTH DISABLED]   if (!res.ok) {
    // [AUTH DISABLED]     setMessage(data.detail || t("auth.serverError"));
    // [AUTH DISABLED]     setIsLoading(false);
    // [AUTH DISABLED]     return;
    // [AUTH DISABLED]   }

    // [AUTH DISABLED]   if (isLogin) {
    // [AUTH DISABLED]     // Use the auth context login function
    // [AUTH DISABLED]     const userData = {
    // [AUTH DISABLED]       email: formData.email,
    // [AUTH DISABLED]       name: data.user?.name || data.user?.username || formData.email.split('@')[0],
    // [AUTH DISABLED]     };
    // [AUTH DISABLED]     
    // [AUTH DISABLED]     login(data.access_token, userData);
    // [AUTH DISABLED]     setMessage(t("auth.loginSuccess"));
    // [AUTH DISABLED]     
    // [AUTH DISABLED]     // Navigate to the appropriate dashboard or home
    // [AUTH DISABLED]     setTimeout(() => {
    // [AUTH DISABLED]       navigate("/");
    // [AUTH DISABLED]     }, 1000);
    // [AUTH DISABLED]   } else {
    // [AUTH DISABLED]     setMessage(t("auth.signupSuccess"));
    // [AUTH DISABLED]     // Clear form and switch to login
    // [AUTH DISABLED]     setFormData({ name: "", email: "", password: "", confirmPassword: "" });
    // [AUTH DISABLED]     setIsLogin(true);
    // [AUTH DISABLED]   }
    // [AUTH DISABLED] } catch (err) {
    // [AUTH DISABLED]   console.error(err);
    // [AUTH DISABLED]   setMessage(t("auth.serverError"));
    // [AUTH DISABLED] } finally {
    // [AUTH DISABLED]   setIsLoading(false);
    // [AUTH DISABLED] }

    // ✅ BYPASS: Skip authentication, just navigate to home
    navigate("/");
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center">
      <video autoPlay loop muted playsInline className="absolute inset-0 w-full h-full object-cover">
        <source src="/farm.mp4" type="video/mp4" />
      </video>
      <div className="absolute inset-0 bg-black/50"></div>

      <div className="relative z-10 w-full max-w-md bg-white/90 backdrop-blur-md shadow-lg rounded-2xl p-8">
        <h2 className="text-3xl font-bold text-gray-800 text-center">
          {isLogin ? t("auth.welcomeBack") : t("auth.createAccount")}
        </h2>
        <p className="text-gray-500 text-center mt-2">
          {isLogin ? t("auth.loginSubtitle") : t("auth.signupSubtitle")}
        </p>

        <form className="mt-6 flex flex-col gap-5" onSubmit={handleSubmit}>
          {!isLogin && (
            <div className="flex items-center border border-gray-300 rounded-lg px-4 py-3">
              <FaUser className="text-gray-500 mr-3" />
              <input
                type="text"
                name="name"
                placeholder={t("auth.namePlaceholder")}
                value={formData.name}
                onChange={handleChange}
                className="w-full outline-none text-gray-700 bg-transparent"
                required={!isLogin}
                // [AUTH DISABLED] disabled={isLoading}
              />
            </div>
          )}

          <div className="flex items-center border border-gray-300 rounded-lg px-4 py-3">
            <FaEnvelope className="text-gray-500 mr-3" />
            <input
              type="email"
              name="email"
              placeholder={t("auth.emailPlaceholder")}
              value={formData.email}
              onChange={handleChange}
              className="w-full outline-none text-gray-700 bg-transparent"
              required
              // [AUTH DISABLED] disabled={isLoading}
            />
          </div>

          <div className="flex items-center border border-gray-300 rounded-lg px-4 py-3">
            <FaLock className="text-gray-500 mr-3" />
            <input
              type="password"
              name="password"
              placeholder={t("auth.passwordPlaceholder")}
              value={formData.password}
              onChange={handleChange}
              className="w-full outline-none text-gray-700 bg-transparent"
              required
              // [AUTH DISABLED] disabled={isLoading}
            />
          </div>

          {!isLogin && (
            <div className="flex items-center border border-gray-300 rounded-lg px-4 py-3">
              <FaLock className="text-gray-500 mr-3" />
              <input
                type="password"
                name="confirmPassword"
                placeholder={t("auth.confirmPasswordPlaceholder")}
                value={formData.confirmPassword}
                onChange={handleChange}
                className="w-full outline-none text-gray-700 bg-transparent"
                required={!isLogin}
                // [AUTH DISABLED] disabled={isLoading}
              />
            </div>
          )}

          <button
            type="submit"
            // [AUTH DISABLED] disabled={isLoading}
            className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-medium shadow transition flex items-center justify-center"
          >
            {/* [AUTH DISABLED] {isLoading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
            ) : null}
            {isLoading 
              ? (isLogin ? "Signing in..." : "Creating account...") 
              : (isLogin ? t("auth.loginButton") : t("auth.signupButton"))
            } */}
            {isLogin ? t("auth.loginButton") : t("auth.signupButton")}
          </button>
        </form>

        {/* [AUTH DISABLED] {message && (
          <p className={`text-center text-sm mt-4 ${
            message.includes("success") || message.includes("Success") 
              ? "text-green-600" 
              : "text-red-500"
          }`}>
            {message}
          </p>
        )} */}

        <p className="text-gray-600 text-sm text-center mt-6">
          {isLogin ? (
            <>
              {t("auth.noAccount")}{" "}
              <button 
                type="button" 
                onClick={() => {
                  setIsLogin(false);
                  // [AUTH DISABLED] setMessage("");
                  setFormData({ name: "", email: "", password: "", confirmPassword: "" });
                }} 
                className="text-green-600 font-medium hover:underline"
                // [AUTH DISABLED] disabled={isLoading}
              >
                {t("auth.signupLink")}
              </button>
            </>
          ) : (
            <>
              {t("auth.alreadyAccount")}{" "}
              <button 
                type="button" 
                onClick={() => {
                  setIsLogin(true);
                  // [AUTH DISABLED] setMessage("");
                  setFormData({ name: "", email: "", password: "", confirmPassword: "" });
                }} 
                className="text-green-600 font-medium hover:underline"
                // [AUTH DISABLED] disabled={isLoading}
              >
                {t("auth.loginLink")}
              </button>
            </>
          )}
        </p>
      </div>
    </section>
  );
}