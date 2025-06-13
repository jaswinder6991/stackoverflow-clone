import React from 'react';
import TopBar from './TopBar';
import LeftSidebar from './LeftSidebar';
import RightSidebar from './RightSidebar';

interface LayoutProps {
  children: React.ReactNode;
  showSidebars?: boolean;
}

const Layout = ({ children, showSidebars = true }: LayoutProps) => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Top Bar */}
      <TopBar />
      
      {/* Main Container */}
      <div className="pt-12">
        <div className="container mx-auto max-w-[1264px]">
          <div className="flex">
            {/* Left Sidebar */}
            {showSidebars && (
              <div className="hidden md:block">
                <LeftSidebar />
              </div>
            )}
            
            {/* Main Content */}
            <div className={`flex-1 ${showSidebars ? 'px-6' : 'px-4'} py-6`}>
              {children}
            </div>
            
            {/* Right Sidebar */}
            {showSidebars && (
              <div className="hidden lg:block">
                <RightSidebar />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Layout;
