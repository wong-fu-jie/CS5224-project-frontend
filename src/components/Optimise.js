import React from "react";
import map from "./icons/map.png";

function Optimise() {
  const optimiseSubmit = (event) => {
    event.preventDefault();
    alert("Optimising!!!");
  };

  const icon_style = {
    width: "50px",
    height: "50px",
    marginLeft: "5px",
  };

  return (
    <div>
      <h3>
        Provide us with some information and let us help personalise an
        itenerary for you.
      </h3>
      <form class="main-form" onSubmit={optimiseSubmit}>
        <h5>Trip Information</h5>
        <div class="form-row">
          <div class="form-group col-md-4">
            <label for="travelStartDate">Starting Date & Time</label>
            <input
              id="travelStartDate"
              type="datetime-local"
              class="form-control"
            />
          </div>
          <div class="form-group col-md-6">
            <label for="travelLength">Travelling Time</label>
            <div class="form-inline">
              <input
                id="travelLength"
                type="number"
                class="col-md-6 form-control"
              />
              <label class="col-md-1">Hours</label>
            </div>
          </div>
          <div class="form-group col-md-8">
            <label for="travelFrom">Starting Location</label>
            <div class="form-inline">
              <select id="travelForm" class="form-control">
                <option selected>
                  NUS School of Computing, 13 Computing Dr, S(117417)
                </option>
              </select>
              <img style={icon_style} src={map} alt="map icon" />
            </div>
          </div>
        </div>
        <h5>Your Travel Preferences</h5>
        <div class="form-row">
          <div class="form-group col-md-4">
            <label for="travelPace">Travel Pace</label>
            <select id="travelPace" class="form-control">
              <option>Slow</option>
              <option>Normal</option>
              <option selected>Fast</option>
            </select>
          </div>
          <div class="form-group col-md-4">
            <label for="travelFood">Are you a foodie?</label>
            <select id="travelFood" class="form-control">
              <option  selected>Live to Eat</option>
              <option>Eat to Live</option>
            </select>
          </div>
          <div class="form-group col-md-4">
            <label for="poiInterests">POI Interests</label>
            <select id="poiInterests" class="form-control">
              <option  selected>Sights & Sounds</option>
              <option>Action Oriented</option>
              <option>Shopping!</option>
            </select>
          </div>
        </div>
        <button class="submit-button" type="submit">Optimise!</button>
      </form>
    </div>
  );
}

export default Optimise;
