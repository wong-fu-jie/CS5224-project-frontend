import React from "react";

function Tab(props) {
  if (props.isSelected) {
    return <div> {props.children}</div>;
  }

  return null;
}

export default Tab;
