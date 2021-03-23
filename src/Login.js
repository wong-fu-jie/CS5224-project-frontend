import React from "react";
import { Link } from "react-router-dom";

function Login() {
  const loginHandler = (event) => {
    event.preventDefault();
    alert("Loging You In!");
  };

  return (
    <div className="login" onSubmit={loginHandler}>
      <h1>Delish & Delight!</h1>
      <form>
        <div>
          <label>Username</label>
          <input type="text" />
        </div>
        <div>
          <label>Password</label>
          <input type="text" />
        </div>
        <button type="submit">
          <Link className="login-button" to={"/main"}>
            Login
          </Link>
        </button>
      </form>
      <a  href="/#">Forgot Password?</a>
    </div>
  );
}

export default Login;
