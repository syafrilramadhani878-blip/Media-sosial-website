import React from "react";
import SocialLinkCard from "./SocialLinkCard";

const SocialLinksGrid = ({ links }) => {
  return (
    <div className="space-y-4 animate-fade-in-up">
      {links.map((link, index) => (
        <SocialLinkCard 
          key={link.id} 
          link={link} 
          index={index}
        />
      ))}
    </div>
  );
};

export default SocialLinksGrid;