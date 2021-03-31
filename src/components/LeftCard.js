import React from "react";
import "../Itinerary.css";

function LeftCard(props) {
  return (
    <div className="left-card">
      <div>
        <img className="picture" src={`https://projectdd-front-end.s3.amazonaws.com/${props.picture}`} alt={props.name} />
      </div>
      <div className="details">
        <h5 className="text">{props.name}</h5>
        <div>
          <label className="text bold">Travelling There:</label>
          <label className="text bold">{props.travelTime}</label>
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

export default LeftCard;
