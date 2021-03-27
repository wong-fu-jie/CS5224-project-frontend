import React, { useState, useEffect } from "react";
import Nav from "./components/Nav.js";
import LeftCard from "./components/LeftCard.js";
import RightCard from "./components/RightCard.js";
import "./Itinerary.css";

function Itinerary() {
  const [travelPlan, setTravelPlan] = useState([]);

  useEffect(() => {
    fetch("/api/itinerary").then(response => {
      if(response.ok){
        return response.json()
      }
    }).then(data => setTravelPlan(data))
  }, []);

  return (
    <div className="itinerary">
      <Nav title="Delish & Delight!" subtitle="Itinerary" />
      <div className="itinerary-cards">
        <h4 className="heading">
          "Here's your travel plan. We hope you are delighted with it!"
        </h4>
        <div>
          <h6>Starting From: NUS School of Computing</h6>
        </div>
        {travelPlan.map((plan) => {
          if (plan.id % 2 === 1) {
            return (
              <LeftCard
                key={plan.id}
                picture={plan.picture}
                name={plan.name}
                travelTime={plan.travelTime}
                description={plan.description}
              />
            );
          } else {
            return (
              <RightCard
                key={plan.id}
                picture={plan.picture}
                name={plan.name}
                travelTime={plan.travelTime}
                description={plan.description}
              />
            );
          }
        })}
      </div>
    </div>
  );
}

export default Itinerary;
