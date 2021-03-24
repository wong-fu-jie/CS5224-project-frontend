import React from "react";
import "../Main.css";

function TabNav(props) {
  return (
    <div style={{ width: "100%" }}>
      <ul className="nav nav-tabs">
        {props.tabs.map((tab) => {
          const active = tab === props.selected ? "active" : "";

          return (
            <li className="nav-item main-tabs" key={tab}>
              <button
                className={"nav-link " + active}
                onClick={() => props.setSelected(tab)}
              >
                {tab}
              </button>
            </li>
          );
        })}
      </ul>
      {props.children}
    </div>
  );
}

export default TabNav;
