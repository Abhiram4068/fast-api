import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  FaTachometerAlt,
  FaBuilding,
  FaUsers,
  FaLaptop,
  FaBoxes,
  FaExchangeAlt,
  FaInbox,
  FaClipboardList,
} from 'react-icons/fa';

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();

const menuItems = [
  { id: 'dashboard', label: 'Dashboard', icon: <FaTachometerAlt />, path: '/dashboard' },
  { id: 'departments', label: 'Departments', icon: <FaBuilding />, path: '/departments' },
  { id: 'employees', label: 'Employees', icon: <FaUsers />, path: '/employees' },
  { id: 'assets', label: 'Assets', icon: <FaLaptop />, path: '/assets' },
  { id: 'inventory', label: 'Inventory', icon: <FaBoxes />, path: '/inventory' },
  { id: 'assign', label: 'Assign an Asset', icon: <FaExchangeAlt />, path: '/assign' },
  { id: 'requests', label: 'Requests', icon: <FaInbox />, path: '/requests' },
  { id: 'logs', label: 'Logs', icon: <FaClipboardList />, path: '/logs' },
];

  return (
    <aside className="w-64 p-4 border-r border-gray-200 flex flex-col space-y-6 bg-white min-h-full select-none flex-shrink-0">
      {/* Navigation Links */}
      <nav className="space-y-1">
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <button
              key={item.id}
              onClick={() => navigate(item.path)}
              className={`w-full flex items-center space-x-3 px-3 py-2 text-sm font-normal rounded-md transition-colors ${
                isActive
                  ? 'text-blue-600 bg-blue-50/60'
                  : 'text-gray-700 hover:bg-gray-50'
              }`}
            >
              <span>{item.icon}</span>
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <hr className="border-gray-200" />

      {/* Maintenance Status Card Block */}
      <div className="border border-gray-200 rounded-md overflow-hidden">
        <div className="bg-gray-50 px-3 py-2 border-b border-gray-200 flex justify-between items-center text-xs font-medium text-gray-600 uppercase tracking-wider">
          <span>Maintenance Status</span>
          <span>0/2 ▼</span>
        </div>
        <div className="p-3 text-xs text-gray-500 bg-white space-y-1.5">
          <div className="flex justify-between">
            <span>1. Idle</span>
            <span className="text-gray-400">Ready</span>
          </div>
          <div className="flex justify-between">
            <span>2. Idle</span>
            <span className="text-gray-400">Ready</span>
          </div>
        </div>
      </div>
    </aside>
  );
}