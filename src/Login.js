import React, {useEffect} from "react";
import { Link } from "react-router-dom";

function Login() {
  useEffect(() => {
    fetch("/api")
    .then((response) => response.json())
    .then(message => console.log(message));
  });

  const loginHandler = (event) => {
    event.preventDefault();
    alert("Loging You In!");
  };

  return (
    <div className="login-box" onSubmit={loginHandler}>
      <div className="login-title">
        <h1>Delish & Delight!</h1>
      </div>
      <form className="login-form">
        <div>
          <div>
            <label className="login-label">Username</label>
            <input type="text" />
          </div>
          <div>
            <label className="login-label">Password</label>
            <input type="text" />
          </div>
          <Link className="login-button " to={"/main"}>
            Sign In
          </Link>
        </div>
      </form>
      <a href="/#">Forgot Password?</a>
    </div>
  );
}

export default Login;
