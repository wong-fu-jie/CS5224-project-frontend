import React from "react";
import map from "./icons/map.png";

function Recommend() {
  const recommendSubmit = (event) => {
    event.preventDefault();
    alert("Recommending!!!");
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
      <form class="main-form" onSubmit={recommendSubmit}>
        <div class="form-group row">
          <label for="travelStartDate" class="col-lg-4 col-form-label-lg">
            When would you like to start travelling?
          </label>
          <div class="col-lg-5">
            <input
              type="datetime-local"
              class="form-control-lg col-lg-12"
              id="travelStartDate"
            />
          </div>
        </div>
        <div class="form-group row">
          <label for="travelLength" class="col-lg-4 col-form-label-lg">
            How long will you trip be?
          </label>
          <div class="col-lg-5">
            <input
              type="number"
              class="col-lg-12 form-control-lg"
              id="travelLength"
            />
          </div>
          <label class="col-form-label-lg">Hours</label>
        </div>
        <div class="form-group row">
          <label for="travelFrom" class="col-lg-4 col-form-label-lg">
            Where will you be starting your trip?
          </label>
          <div class="col-lg-5">
            <select
              type="search"
              class="col-lg-10 form-control-lg"
              id="travelFrom"
            >
              <option selected>
                NUS School of Computing, 13 Computing Dr, S(117417)
              </option>
            </select>
            <img style={icon_style} src={map} alt="map icon" />
          </div>
        </div>
        <button class="submit-button" type="submit">
          Recommend me!
        </button>
      </form>
    </div>
  );
}

export default Recommend;
