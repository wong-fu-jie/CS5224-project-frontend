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
      <form className="main-form" onSubmit={optimiseSubmit}>
        <h5>Trip Information</h5>
        <div className="form-row">
          <div className="form-group col-md-4">
            <label htmlFor="travelStartDate">Starting Date & Time</label>
            <input
              id="travelStartDate"
              type="datetime-local"
              className="form-control"
            />
          </div>
          <div className="form-group col-md-6">
            <label htmlFor="travelLength">Travelling Time</label>
            <div className="form-inline">
              <input
                id="travelLength"
                type="number"
                className="col-md-6 form-control"
              />
              <label className="col-md-1">Hours</label>
            </div>
          </div>
          <div className="form-group col-md-8">
            <label htmlFor="travelFrom">Starting Location</label>
            <div className="form-inline">
              <select id="travelForm" className="form-control">
                <option value='1'>
                  NUS School of Computing, 13 Computing Dr, S(117417)
                </option>
              </select>
              <img style={icon_style} src={map} alt="map icon" />
            </div>
          </div>
        </div>
        <h5>Your Travel Preferences</h5>
        <div className="form-row">
          <div className="form-group col-md-4">
            <label htmlFor="travelPace">Travel Pace</label>
            <select id="travelPace" className="form-control" defaultValue='2'>
              <option value='1'>Slow</option>
              <option value='2'>Normal</option>
              <option value='3'>Fast</option>
            </select>
          </div>
          <div className="form-group col-md-4">
            <label htmlFor="travelFood">Are you a foodie?</label>
            <select id="travelFood" className="form-control" defaultValue='1'>
              <option value='1'>Live to Eat</option>
              <option value='2'>Eat to Live</option>
            </select>
          </div>
          <div className="form-group col-md-4">
            <label htmlFor="poiInterests">POI Interests</label>
            <select id="poiInterests" className="form-control" defaultValue='3'>
              <option value='1'>Adventure</option>
              <option value='2'>Arts</option>
              <option value='3'>History & Culture</option>
              <option value='4'>Leisure & Recreation</option>
              <option value='5'>Nature & Wildlife</option>
              <option value='6'>Others</option>
            </select>
          </div>
        </div>
        <button className="submit-button" type="submit">Optimise!</button>
      </form>
    </div>
  );
}

export default Optimise;
