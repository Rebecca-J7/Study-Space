"use client";
import React from "react";

const Planet: React.FC = () => {
  return (
    <div className="planet-container mt-16 flex justify-center">
      <div className="planet" aria-hidden>
        <div className="planet-ring" />
      </div>
    </div>
  );
};

export default Planet;
