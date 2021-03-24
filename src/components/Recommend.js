import React from "react";

function Recommend() {
  return (
    <div>
      <h3>Before we get started, help us by providing the below information.</h3>
      <form class="main-form">
        <div class="form-group row">
          <label for="travelStartDate" class="col-lg-4 col-form-label-lg">
            When would you like to start travelling?
          </label>
          <div class="col-lg-5">
            <input
              type="datetime-local"
              class="form-control-lg col-lg-10"
              id="travelStartDate"
            />
          </div>
        </div>
        <div class="form-group row">
          <label for="travelLength" class="col-lg-4 col-form-label-lg">
            How long will you trip be?
          </label>
          <div class="col-lg-5">
            <input type="number" class="col-lg-12 form-control-lg" id="travelLength" />
          </div>
          <label class="col-form-label-lg">Hours</label>
        </div>
        <div class="form-group row">
          <label for="travelFrom" class="col-lg-4 col-form-label-lg">
            Where will you be starting your trip?
          </label>
          <div class="col-lg-5">
            <input type="search" class="col-lg-12 form-control-lg" id="travelFrom" />
          </div>
        </div>
      </form>
    </div>
  );
}

export default Recommend;
