import React from "react";
import "../Itinerary.css";

function RightCard(props) {
  return (
    <div className="right-card">
      <div>
        <img className="picture" src={`https://projectdd-front-end.s3.amazonaws.com/${props.picture}`} alt={props.name} />
      </div>
      <div className="details">
        <h5 className="text">{props.name}</h5>
        <div>
          <label className="text bold">Travel Time:</label>
          <label className="text bold">{props.travelTime}</label>
          <label className="text">show map</label>
        </div>
        <div>
          <label className="text bold">Time to Spend Here:</label>
          <label className="text bold">{props.spendTime}</label>
        </div>
        <div className="text">
          <p>{props.description}</p>
        </div>
      </div>
    </div>
  );
}

export default RightCard;
