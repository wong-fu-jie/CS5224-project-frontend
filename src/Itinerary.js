import React, { useState, useEffect } from "react";
import Nav from "./components/Nav.js";
import LeftCard from "./components/LeftCard.js";
import RightCard from "./components/RightCard.js";
import "./Itinerary.css";

// Sample pics, should be fetched from server
import hortPark from "./pics/hort-park.jpg";
import mtFaberPark from "./pics/mount-faber.jpg";

function Itinerary() {
  // How to fetch this from server?
  const [travelPlan, setTravelPlan] = useState([]);
  //   {
  //     id: 1,
  //     picture: hortPark,
  //     name: "Hort Park",
  //     travelTime: "20 mins (Grab)",
  //     description:
  //       "Hort Park is a one-stop gardening resource hub that brings together gardening-related, recreational, educational, research and retail activities under one big canopy in a park setting. It also serves as a knowledge centre on plants and gardening, providing planting ideas and solutions, and offering a platform for the horticulture industry to share best practices and showcase garden designs, products and services.",
  //   },
  //   {
  //     id: 2,
  //     picture: mtFaberPark,
  //     name: "Mount Faber Park",
  //     travelTime: "15 mins (Grab)",
  //     description:
  //       "Mount Faber, originally known as Telok Blangah Hill is Singapore's second-highest hill and the park atop the hill is named as Mount Faber Park after Captain Charles Edward Faber in July 1845. It is among the oldest parks of Singapore and a major tourist attraction for nature lovers. Standing at an elevation of 105 metres Mount Faber is nestled inside the Bukit Merah town in Central Singapore overlooking Telok Blangah hill and the western region of the Central Area.",
  //   },
  // ]);

  const [plan, setPlan] = useState([]);

  useEffect(() => {
    fetch("/api/itinerary")
  });

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
                id={plan.id}
                picture={plan.picture}
                name={plan.name}
                travelTime={plan.travelTime}
                description={plan.description}
              />
            );
          } else {
            return (
              <RightCard
                id={plan.id}
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
