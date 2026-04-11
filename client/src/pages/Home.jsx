import React, { useEffect, useState } from "react";
import Header from "../components/Header";
import { useTranslation } from "react-i18next";
import { useNavigate } from "react-router-dom";

const Home = () => {
  // [AUTH DISABLED] const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isLoggedIn] = useState(true); // ✅ BYPASS: Always consider logged in
  const { t } = useTranslation();
  const navigate = useNavigate();

  // [AUTH DISABLED] useEffect(() => {
  //   const token = localStorage.getItem("token");
  //   setIsLoggedIn(!!token);
  // }, []);

  const handleGetStarted = () => {
    // [AUTH DISABLED] if (isLoggedIn) {
    //   navigate("/input");
    // } else {
    //   navigate("/login");
    // }
    
    // ✅ BYPASS: Always navigate to input (no login check)
    navigate("/input");
  };

  return (
    <div>
      <Header />

     
     
    </div>
  );
};

export default Home;
