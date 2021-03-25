import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import "./App.css";
import Time from "./Time.js";
import Login from "./Login.js";
import Main from "./Main.js"
import Itinerary from "./Itinerary.js"

function App() {
  return (
    <Router>
      <div className = "App">
        <Switch>
          <Route path="/" exact component={Login} />
          <Route path="/time" component={Time} />
          <Route path="/main" component={Main} />
          <Route path="/itinerary" component={Itinerary} />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
