import React from 'react';

export default function DashboardPage() {
  // Mock data reflecting your FastAPI backend models and state
  const metrics = [
    { label: 'Total Employees', count: 142, color: 'text-blue-600' },
    { label: 'Total Departments', count: 8, color: 'text-purple-600' },
    { label: 'Total Assets', count: 324, color: 'text-gray-800' },
    { label: 'Assets Returned (This Month)', count: 18, color: 'text-green-600' },
    { label: 'Damaged / In Repair', count: 3, color: 'text-amber-600' },
    { label: 'New / Unassigned', count: 24, color: 'text-indigo-600' },
    { label: 'Out of Stock Categories', count: 2, color: 'text-red-600' },
  ];

  const recentActivities = [
    { id: '#12', type: 'Assignment', asset: 'Dell XPS 15 (ST-094)', target: 'Sarah Jenkins (DevOps)', time: '12 min ago', status: 'SUCCESS' },
    { id: '#11', type: 'Return', asset: 'MacBook Pro 14 (ST-012)', target: 'John Doe (Sales)', time: '45 min ago', status: 'SUCCESS' },
    { id: '#10', type: 'Maintenance', asset: 'HP LaserJet Pro (ST-441)', target: 'Hardware Failure', time: '2 hrs ago', status: 'WARNING' },
  ];

  return (
    <div class="flex-1 p-6 bg-white overflow-y-auto">
      {/* Tab Filter Header Row */}
      <div class="flex items-center space-x-1 mb-6 border-b border-gray-200 pb-px select-none">
        <button class="px-4 py-1.5 text-sm font-medium bg-gray-100 text-gray-800 rounded-t-md border-t border-x border-gray-200">
          System Overview
        </button>
      </div>

      {/* Grid Metrics Panel */}
      <div class="grid grid-cols-1 md-grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        {metrics.map((metric, idx) => (
          <div key={idx} class="border border-gray-200 rounded-md p-4 bg-white shadow-sm flex items-center justify-between">
            <div class="space-y-1">
              <span class="text-xs font-bold text-gray-500 uppercase tracking-wider block">
                {metric.label}
              </span>
              <span class={`text-2xl font-semibold tracking-tight ${metric.color}`}>
                {metric.count}
              </span>
            </div>
            <span class="text-2xl opacity-80 select-none">{metric.icon}</span>
          </div>
        ))}
      </div>

      {/* Recent Operations / Logs Table Header */}
      <div class="mb-3 flex justify-between items-center select-none">
        <h2 class="text-base font-semibold text-gray-800 tracking-tight">
          Recent System Activities
        </h2>
      </div>

      {/* Main Jenkins-style Status Table */}
      <div class="border border-gray-200 rounded-md overflow-hidden shadow-sm">
        <table class="w-full text-left border-collapse bg-white text-sm">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-200 text-gray-600 font-semibold select-none">
              <th class="p-3 w-12 text-center">S</th>
              <th class="p-3 w-16">ID</th>
              <th class="p-3 w-32">Operation Type</th>
              <th class="p-3">Asset Target</th>
              <th class="p-3">Assigned To / Detail</th>
              <th class="p-3 w-32">Timestamp</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 text-gray-700">
            {recentActivities.map((activity) => (
              <tr key={activity.id} class="hover:bg-gray-50/70 transition-colors">
                <td class="p-3 text-center select-none">
                  {activity.status === 'SUCCESS' ? (
                    <span class="inline-flex items-center justify-center w-5 h-5 bg-green-100 border border-green-500 rounded-full text-green-700 text-xs font-bold">✓</span>
                  ) : (
                    <span class="inline-flex items-center justify-center w-5 h-5 bg-amber-100 border border-amber-500 rounded-full text-amber-700 text-xs font-bold">!</span>
                  )}
                </td>
                <td class="p-3 font-mono text-xs text-gray-500">{activity.id}</td>
                <td class="p-3">
                  <span class="font-medium text-gray-900">{activity.type}</span>
                </td>
                <td class="p-3 font-medium text-blue-600 hover:underline cursor-pointer">
                  {activity.asset}
                </td>
                <td class="p-3 text-gray-600">{activity.target}</td>
                <td class="p-3 text-gray-500 text-xs">{activity.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}