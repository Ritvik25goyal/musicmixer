import React from "react";

function Img({imgurl}) {
  return (
    <div className="imageHolder">
      <img
        className="imgRounded"
        src={imgurl}
        alt="Any Random"
      />
    </div>
  );
}

export default Img;
    