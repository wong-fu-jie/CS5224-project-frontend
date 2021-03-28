import React from "react";
import loading from "../pics/loading.gif";

function Loading() {
  return (
    <div>
      <h2>Planning Your Itinerary...</h2>
      <img src={loading} alt="Loading"/>
    </div>
  );
}

export default Loading;
