import React from "react";
import Card from "../Card/Cards";
import "./container.css"

function Container({image, title, description, id}) {
    return (
        <div className="container">
            <div className="Title">
            </div>
            <Card />
            <Card />
            <Card />
        </div>
    )
}

export default Container