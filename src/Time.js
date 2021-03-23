import React, { useState, useEffect } from "react";

function Time() {
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch("/api/time")
      .then((response) => response.json())
      .then((data) => {
        setCurrentTime(data.time);
      });
  }, []);

  return (
    <div>
      <h2>Giving us the current time</h2>
      <p>The current time is {currentTime}.</p>
    </div>
  );
}

export default Time;
