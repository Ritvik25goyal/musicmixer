import React from "react";
import "./login.css";
import LoginIcon from "./Logo/Logo.jpg";

const Login = () => {
  return (
    <div className="login">
      <img src={LoginIcon} alt="" />
      <a href="#">LOGIN WITH SPOTIFY</a>
    </div>
  );
};

export default Login;
