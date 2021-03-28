import React, { useState } from "react";
import map from "./icons/map.png";
import { useHistory } from "react-router-dom";

function Recommend() {
  let history = useHistory();

  const [recState, setRecState] = useState({
    startDate: "2021-03-31T15:30",
    travelLength: 1,
    location: 117417,
  });

  const startDateHandler = (event) => {
    setRecState({
      startDate: event.target.value,
    });
  };

  const travelLengthHandler = (event) => {
    setRecState({
      travelLength: event.target.value,
    });
  };

  const locationHandler = (event) => {
    setRecState({
      location: event.target.value,
    });
  };

  const recommendSubmit = (event) => {
    event.preventDefault();
    fetch("/api/recommend", {
      method: "POST",
      body: JSON.stringify({
         content: recState
       }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    }).then(response => response.json())
    .then(message => console.log(message));
    history.push("/itinerary");
  };

  const icon_style = {
    width: "50px",
    height: "50px",
    marginLeft: "5px",
  };

  return (
    <div>
      <h3>
        Let us recommend you a plan! Just tell us where and how you want to
        start and let us get to work!
      </h3>
      <form className="main-form" onSubmit={recommendSubmit}>
        <div className="form-group row">
          <label
            htmlFor="travelStartDate"
            className="col-lg-4 col-form-label-lg"
          >
            When would you like to start travelling?
          </label>
          <div className="col-lg-5">
            <input
              value={recState.startDate}
              onChange={startDateHandler}
              type="datetime-local"
              className="form-control-lg col-lg-12"
              id="travelStartDate"
            />
          </div>
        </div>
        <div className="form-group row">
          <label htmlFor="travelLength" className="col-lg-4 col-form-label-lg">
            How long will you trip be?
          </label>
          <div className="col-lg-5">
            <input
              value={recState.travelLength}
              onChange={travelLengthHandler}
              type="number"
              className="col-lg-12 form-control-lg"
              id="travelLength"
            />
          </div>
          <label className="col-form-label-lg">Hour(s)</label>
        </div>
        <div className="form-group row">
          <label htmlFor="travelFrom" className="col-lg-4 col-form-label-lg">
            Where will you be starting your trip?
          </label>
          <div className="col-lg-5">
            <select
              value={recState.location}
              type="search"
              className="col-lg-10 form-control-lg"
              id="travelFrom"
              onChange={locationHandler}
            >
              <option value="117417">
                NUS School of Computing, 13 Computing Dr, S(117417)
              </option>
              <option value="119245">
                NUS School of Business, 15 Kent Ridge Dr, S(119245)
              </option>
            </select>
            <img style={icon_style} src={map} alt="map icon" />
          </div>
        </div>
        <button className="submit-button" type="submit">
          Recommend me!
        </button>
      </form>
    </div>
  );
}

export default Recommend;
