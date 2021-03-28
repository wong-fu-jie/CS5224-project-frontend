import React from "react";

function TripSearch() {
  const searchSubmit = (event) => {
    event.preventDefault();
    alert("Searching " + event.searchInput);
  };

  return (
    <div>
      <h3>
        Search our database of places to travel to by typing in some key words
        below.
      </h3>
      <form className="main-form" onSubmit={searchSubmit}>
        <div className="form-group row justify-content-center">
          <input
            className="col-lg-8 form-control-lg"
            type="search"
            id="searchInput"
            placeholder="Search Here"
          />
          <div className="col-lg-12 row justify-content-center">
            <button className="submit-button" type="submit">
              Search!
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}

export default TripSearch;
