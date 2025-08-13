import React from "react";
import { Heart, Calendar } from "lucide-react";

const Footer = () => {
  const currentYear = new Date().getFullYear();
  const creationDate = "Agustus 2025";

  return (
    <footer className="mt-12 py-8 border-t border-gray-200/30 bg-white/30 backdrop-blur-sm animate-fade-in">
      <div className="text-center space-y-3">
        <div className="flex items-center justify-center gap-2 text-gray-600 text-sm">
          <Calendar size={16} />
          <span>Dibuat pada {creationDate}</span>
        </div>
        
        <div className="flex items-center justify-center gap-2 text-gray-700 text-sm font-medium">
          <span>Dibuat oleh</span>
          <span className="text-blue-600 font-semibold">Moch. Syafril Ramadhani</span>
          <Heart size={16} className="text-red-500 animate-pulse" />
        </div>
        
        <div className="text-xs text-gray-500 pt-2">
          © {currentYear} - Website Profil Sosial Media
        </div>
      </div>
    </footer>
  );
};

export default Footer;