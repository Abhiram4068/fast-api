import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import TopNavbar from './components/TopNavbar';
import Sidebar from './components/Sidebar';
import AssetDashboard from './pages/protected/AssetDashboard';
import DashboardPage from './pages/protected/DashboardPage';

function PlaceholderPage({ name }) {
  return (
    <div className="flex-1 p-6 text-gray-500 bg-white font-medium">
      Content module for <span className="capitalize font-bold text-gray-800">"{name}"</span> is ready to hook up to your FastAPI backend.
    </div>
  );
}

export default function App() {
  return (
    <div className="min-h-screen bg-white text-gray-900 flex flex-col font-sans">
      {/* Header */}
      <TopNavbar />

      {/* Middle Layout Pane */}
      <div className="flex flex-1 items-stretch">
        <Sidebar />
        <main className="flex flex-1">
          <Routes>
            <Route path="/" element={<Navigate to="/assets" replace />} />
            <Route path="/dashboard" element={<DashboardPage />} />
            <Route path="/assets" element={<AssetDashboard />} />
            <Route path="/departments" element={<PlaceholderPage name="departments" />} />
            <Route path="/employees" element={<PlaceholderPage name="employees" />} />
            <Route path="/inventory" element={<PlaceholderPage name="inventory" />} />
            <Route path="/assign" element={<PlaceholderPage name="assign" />} />
            <Route path="/requests" element={<PlaceholderPage name="requests" />} />
            <Route path="/logs" element={<PlaceholderPage name="logs" />} />
            <Route path="*" element={<Navigate to="/assets" replace />} />
          </Routes>
        </main>
      </div>

      {/* Page Layout Base Footer */}
      <footer className="h-8 border-t border-gray-200 bg-gray-50 flex items-center justify-between px-6 text-xs text-gray-500 select-none">
        <div>
          <a href="/docs" target="_blank" rel="noreferrer" className="hover:underline text-blue-600 font-medium">
            REST API
          </a>
        </div>
        <div>
          <span>ITAM Engine v1.0.0</span>
        </div>
      </footer>
    </div>
  );
}