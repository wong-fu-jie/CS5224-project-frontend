import React from "react";
import "./Nav.css";
import profile from "./pics/profile.jpg";

function Nav(props) {
  return (
    <div className="navigation">
      <div className="title">
        <h1>{props.title}</h1>
        <h3>{props.subtitle}</h3>
      </div>
      <img className="profile" src={profile} alt="profile" />
    </div>
  );
}

export default Nav;
