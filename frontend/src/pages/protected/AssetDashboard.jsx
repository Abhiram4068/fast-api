import React from 'react';

export default function AssetDashboard() {
  return (
    <div class="flex-1 p-6 bg-white overflow-x-auto">
      {/* Upper Tab Filter Row */}
      <div class="flex items-center space-x-1 mb-4 border-b border-gray-200 pb-px">
        <button class="px-4 py-1.5 text-sm font-medium bg-gray-100 text-gray-800 rounded-t-md border-t border-x border-gray-200">
          All Assets
        </button>
        <button class="px-3 py-1.5 text-sm font-medium text-blue-600 hover:bg-gray-50 rounded-t-md transition-colors">
          ➕
        </button>
      </div>

      {/* Description Actions */}
      <div class="flex justify-end mb-4">
        <button class="text-xs border border-gray-300 rounded px-2.5 py-1 text-gray-600 hover:bg-gray-50 flex items-center space-x-1 transition-colors">
          <span>📝</span> <span>Add System Description</span>
        </button>
      </div>

      {/* Classic Jenkins-style Data Table */}
      <div class="border border-gray-200 rounded-md overflow-hidden shadow-sm">
        <table class="w-full text-left border-collapse bg-white text-sm">
          <thead>
            <tr class="bg-gray-50 border-b border-gray-200 text-gray-600 font-semibold select-none">
              <th class="p-3 w-12 text-center">S</th>
              <th class="p-3 w-12 text-center">W</th>
              <th class="p-3">Asset Name (Tag)</th>
              <th class="p-3">Last Assignment</th>
              <th class="p-3">Last Failure/Issue</th>
              <th class="p-3">Warranty Remaining</th>
              <th class="p-3 w-16 text-center">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-100 text-gray-700">
            <tr class="hover:bg-gray-50/70 transition-colors">
              <td class="p-3 text-center">
                <span class="inline-flex items-center justify-center w-5 h-5 bg-green-100 border border-green-500 rounded-full text-green-700 text-xs font-bold">
                  ✓
                </span>
              </td>
              <td class="p-3 text-center text-lg leading-none">☀️</td>
              <td class="p-3 font-medium text-blue-600 hover:underline cursor-pointer">
                fastapi-backend-macbook-01
              </td>
              <td class="p-3 flex items-center space-x-1.5">
                <span>1 hr 21 min ago</span>
                <span class="bg-blue-100 text-blue-800 text-xs font-semibold px-2 py-0.5 rounded-full border border-blue-200">
                  #6
                </span>
              </td>
              <td class="p-3 text-gray-400">N/A</td>
              <td class="p-3 text-gray-500">24 Months</td>
              <td class="p-3 text-center">
                <button class="text-green-600 hover:text-green-800 font-bold transition-transform active:scale-95 text-lg leading-none">
                  ▶
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      {/* Sizing Toggles Footer */}
      <div class="mt-4 flex items-center justify-between text-xs text-gray-500 select-none">
        <div class="flex items-center space-x-2">
          <span>Icon size:</span>
          <button class="px-1.5 py-0.5 border border-gray-200 rounded bg-gray-50 hover:bg-gray-100">S</button>
          <button class="px-1.5 py-0.5 border border-gray-200 rounded bg-gray-50 hover:bg-gray-100">M</button>
          <button class="px-1.5 py-0.5 border border-gray-300 rounded bg-gray-200 font-semibold text-gray-700">L</button>
        </div>
      </div>
    </div>
  );
}