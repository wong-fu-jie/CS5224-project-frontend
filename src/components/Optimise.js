import React from "react";

function Optimise(){
  const optimiseSubmit = (event) => {
    event.preventDefault();
    alert("Optimising!!!")
  }

  return(
    <div>
      <h3>Provide us with some information and let us help to personalise an itenerary for you.</h3>
      <form class="main-form" onSubmit={optimiseSubmit}>

      </form>
    </div>
  );
}

export default Optimise;
