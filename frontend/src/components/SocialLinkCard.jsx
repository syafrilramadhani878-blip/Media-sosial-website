import React from "react";
import { Card, CardContent } from "./ui/card";
import { Instagram, MessageCircle, Mail, Music2 } from "lucide-react";

const SocialLinkCard = ({ link, index }) => {
  const getIcon = (platform) => {
    const iconProps = { size: 24, className: "flex-shrink-0" };
    
    switch (platform.toLowerCase()) {
      case 'instagram':
        return <Instagram {...iconProps} />;
      case 'whatsapp':
        return <MessageCircle {...iconProps} />;
      case 'email':
        return <Mail {...iconProps} />;
      case 'tiktok':
        return <Music2 {...iconProps} />;
      default:
        return <div className="w-6 h-6 rounded-full bg-gray-300" />;
    }
  };

  const handleClick = () => {
    if (link.url) {
      window.open(link.url, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <Card 
      className="group cursor-pointer transition-all duration-300 hover:shadow-lg hover:scale-[1.02] hover:-translate-y-1 bg-white/80 backdrop-blur-sm border border-gray-200/50"
      onClick={handleClick}
      style={{
        animationDelay: `${index * 100}ms`
      }}
    >
      <CardContent className="p-6">
        <div className="flex items-center space-x-4">
          <div className={`p-3 rounded-xl transition-all duration-300 group-hover:scale-110 ${link.iconBg}`}>
            {getIcon(link.platform)}
          </div>
          
          <div className="flex-1 min-w-0">
            <h3 className="font-semibold text-gray-900 text-lg tracking-tight">
              {link.title}
            </h3>
            <p className="text-gray-600 text-sm mt-1 truncate">
              {link.description}
            </p>
          </div>
          
          <div className="opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <div className="w-2 h-2 rounded-full bg-gray-400"></div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default SocialLinkCard;