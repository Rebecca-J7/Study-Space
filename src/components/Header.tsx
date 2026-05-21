"use client";
import React from "react";

const Header = () => {
  const scrollToSection = (sectionId: string) => {
    const section = document.getElementById(sectionId);
    const headerHeight = 56;
    if (section) {
      window.scrollTo({
        top: section.offsetTop - headerHeight,
        behavior: "smooth",
      });
    }
  };

  return (
    <div className="fixed top-0 z-50 h-14 w-full bg-web-ss-blue opacity-75">
      <div className="relative flex flex-row content-center gap-5 font-afacad text-xl font-semibold">
        <div
          className="absolute left-7 top-3 h-9 w-9 rounded-full bg-white"
          onClick={() => scrollToSection("welcome")}
        ></div>
        <p
          className="text-web-purple-2 absolute left-20 top-4 cursor-pointer scroll-mt-14 hover:text-white"
          onClick={() => scrollToSection("introduction")}
        >
          Study Space
        </p>
        <p
          className="absolute right-40 top-4 cursor-pointer scroll-mt-14 text-black hover:text-white"
          onClick={() => scrollToSection("about")}
        >
          about
        </p>
        {/* Pomodoro link removed per request */}
      </div>
    </div>
  );
};

export default Header;
