// React Libraries
import React from "react";
import { useState } from "react";

// Our Website Components
import Img from "./Img.js";
import Title from "./Title.js";
import Description from "./Description.js";

// Font Awesome imports
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlay } from "@fortawesome/free-solid-svg-icons";

//Main Function
function Card({image, title, description, id}) {
  // For Mouse Hover Effect of Play button.
  const [isHovering, setIsHovering] = useState(false);

  const handleMouseOver = () => {
    setIsHovering(true);
  };

  const handleMouseOut = () => {
    setIsHovering(false);
  };

  return (
    <div
      className="songCard"
      onMouseOver={handleMouseOver}
      onMouseOut={handleMouseOut}
    >
      <Img imgurl={image}/>
      <Title title={title}/>
      <Description description={description}/>

      {/* This is the part which would be shown on hover effect */}

      {isHovering && (
        <div className="playButton animate__animated animate__fadeInUp">
          <FontAwesomeIcon icon={faPlay} color={"#202020"} />
        </div>
      )}

      {}
    </div>
  );
}

export default Card;
