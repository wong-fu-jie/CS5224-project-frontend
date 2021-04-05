import React, { useState, useEffect } from "react";
import Nav from "./components/Nav.js";
import LeftCard from "./components/LeftCard.js";
import RightCard from "./components/RightCard.js";
import Loading from "./components/Loading.js";
import "./Itinerary.css";

function Itinerary() {
  const [loading, setLoading] = useState(true);
  const [loadCount, setLoadCount] = useState(0);
  const [travelPlan, setTravelPlan] = useState([]);

  useEffect(() => {
    fetch("/api/itinerary")
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
      })
      .then((data) => {
        console.log(data);
        if (data.loading === "no") {
          setLoading(false);
          setTravelPlan(data.itinerary);
        }
      });
  }, [loadCount]);

  useEffect(() => {
    let interval = null;
    if (loading) {
      interval = setInterval(() => {
        setLoadCount((prevLoadCount) => prevLoadCount + 1);
      }, 2000);
    } else {
      clearInterval(interval);
      setLoadCount(0);
    }
    return () => clearInterval(interval);
  }, [loading]);

  const ShowMapRedirect = () => {
    window.location.replace("http://34.207.205.251:8080/map");
  };

  const RenderContent = (isLoading) => {
    if (loading) {
      return (
        <div className="itinerary-cards">
          <Loading />
        </div>
      );
    } else {
      return (
        <div className="itinerary-cards">
          <h4 className="heading">
            "Here's your travel plan. We hope you are delighted with it!"
          </h4>
          <div className="start-location">
            <div>
              <h5>Starting From: NUS School of Computing</h5>
            </div>
            <button className="map-button" onClick={ShowMapRedirect}>
              Show Map
            </button>
          </div>
          {travelPlan.map((plan) => {
            if (plan.id % 2 === 1) {
              return (
                <LeftCard
                  key={plan.id}
                  picture={plan.picture}
                  name={plan.name}
                  travelTime={plan.travelTime}
                  spendTime={plan.spendTime}
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
                  spendTime={plan.spendTime}
                  description={plan.description}
                />
              );
            }
          })}
        </div>
      );
    }
  };

  return (
    <div className="itinerary">
      <Nav title="Delish & Delight!" subtitle="Itinerary" />
      <RenderContent isLoading={loading} />
    </div>
  );
}

export default Itinerary;
