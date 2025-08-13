import React from "react";
import ProfileSection from "../components/ProfileSection";
import SocialLinksGrid from "../components/SocialLinksGrid";
import ContactForm from "../components/ContactForm";
import Footer from "../components/Footer";
import { Toaster } from "../components/ui/toaster";
import { socialLinks } from "../data/mock";

const HomePage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-gray-100">
      <div className="container mx-auto px-4 py-8 max-w-md">
        <div className="space-y-8">
          <ProfileSection />
          <SocialLinksGrid links={socialLinks} />
          <ContactForm />
          <Footer />
        </div>
      </div>
      <Toaster />
    </div>
  );
};

export default HomePage;