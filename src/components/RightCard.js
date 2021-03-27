import React from "react";
import "../Itinerary.css";

function RightCard(props) {
  return (
    <div className="right-card">
      <div>
        <img className="picture" src={props.picture} alt="Mount Faber Park" />
      </div>
      <div className="details">
        <h5 className="text">{props.name}</h5>
        <div>
          <label className="text bold">Travel Time:</label>
          <label className="text bold">{props.travelTime}</label>
          <label className="text">show map</label>
        </div>
        <div className="text">
          <p>{props.description}</p>
        </div>


      </div>
    </div>
  );
}

export default RightCard;
