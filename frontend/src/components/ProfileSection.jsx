import React from "react";
import { Avatar, AvatarImage, AvatarFallback } from "./ui/avatar";

const ProfileSection = () => {
  const profileData = {
    name: "Moch. Syafril Ramadhani",
    profilePhoto: "https://customer-assets.emergentagent.com/job_saferill-social/artifacts/ckzj1933_IMG-20250715-WA0000.jpg",
    bio: "Connect with me on social media"
  };

  return (
    <div className="text-center space-y-4 animate-fade-in">
      <div className="relative mx-auto w-32 h-32">
        <Avatar className="w-full h-full border-4 border-white shadow-xl ring-2 ring-gray-200">
          <AvatarImage 
            src={profileData.profilePhoto} 
            alt={profileData.name}
            className="object-cover"
          />
          <AvatarFallback className="text-2xl font-semibold bg-gradient-to-br from-blue-500 to-purple-600 text-white">
            {profileData.name.split(' ').map(n => n[0]).join('')}
          </AvatarFallback>
        </Avatar>
      </div>
      
      <div className="space-y-2">
        <h1 className="text-2xl font-bold text-gray-900 tracking-tight">
          {profileData.name}
        </h1>
        <p className="text-gray-600 text-sm max-w-xs mx-auto leading-relaxed">
          {profileData.bio}
        </p>
      </div>
    </div>
  );
};

export default ProfileSection;