import React from "react";
import Sidebar from "./Components/sidebar/Sidebar";
import Container from "./Components/Container/container";

function Root() {
    return (
        <div className="App">
      <Sidebar/>
      <div className="empty"></div>
      <div className="Content"> 
        <Container />
        <Container />
        <Container />
      </div>
    </div>
    )
}

export default Root