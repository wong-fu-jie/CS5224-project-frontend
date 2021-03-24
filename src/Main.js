import React from "react";
import PropTypes from "prop-types";
import "./Main.css";
import Nav from "./Nav.js";
import Tab from "./components/Tab.js";
import TabNav from "./components/TabNav.js";

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
      <div className='main'>
        <Nav
          title="Welcome!"
          subtitle="How would you like us to recommend your trip today?"
        />
        <div>
          <div className="tabs-box">
            <TabNav
              tabs={["Recommend", "Optimise", "Search"]}
              selected={this.state.selected}
              setSelected={this.setSelected}
            >
              <Tab isSelected={this.state.selected === "Recommend"}>
                <p>Some Test Text</p>
              </Tab>
              <Tab isSelected={this.state.selected === "Optimise"}>
                <h1>Some more Text</h1>
              </Tab>
              <Tab isSelected={this.state.selected === "Search"}>
                <ul>
                  <li> List test 1</li>
                  <li> List test 2</li>
                  <li> List test 3</li>
                </ul>
              </Tab>
            </TabNav>
          </div>
        </div>
      </div>
    );
  }
}

export default Main;
