import React from "react";
import "./Main.css";
import Nav from "./components/Nav.js";
import Tab from "./components/Tab.js";
import TabNav from "./components/TabNav.js";
import Recommend from "./components/Recommend.js";
import Optimise from "./components/Optimise.js";
import TripSearch from "./components/TripSearch.js";

class Main extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      selected: "Recommend",
    };
  }

  setSelected = (tab) => {
    this.setState({ selected: tab });
  };

  render() {
    return (
      <div className="main">
        <Nav
          title="Welcome!"
          subtitle="How would you like us to recommend your trip today?"
        />
        <div className="tabs-box">
          <TabNav
            tabs={["Recommend", "Optimise", "Search"]}
            selected={this.state.selected}
            setSelected={this.setSelected}
          >
            <Tab isSelected={this.state.selected === "Recommend"}>
              <Recommend />
            </Tab>
            <Tab isSelected={this.state.selected === "Optimise"}>
              <Optimise />
            </Tab>
            <Tab isSelected={this.state.selected === "Search"}>
              <TripSearch />
            </Tab>
          </TabNav>
        </div>
      </div>
    );
  }
}

export default Main;
