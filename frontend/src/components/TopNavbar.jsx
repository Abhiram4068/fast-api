import React from 'react';

export default function TopNavbar() {
  return (
    <header className="h-14 border-b border-gray-200 flex items-center justify-between px-6 bg-white w-full select-none">
      <div className="flex items-center space-x-3">
        <div className="bg-blue-600 text-white p-1.5 text-sm font-bold tracking-wider">
          ITAM
        </div>
        <span className="text-xl font-semibold tracking-tight text-gray-800">
          IT Asset Management
        </span>
      </div>
      <div className="flex items-center space-x-4 text-gray-600">
        <button className="hover:text-gray-900 transition-colors">🔍 Search</button>
        <button className="hover:text-gray-900 transition-colors">⚙️ Settings</button>
        <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center font-bold text-sm text-gray-700 border">
          A
        </div>
      </div>
    </header>
  );
}