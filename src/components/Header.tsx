import React from 'react';
import { BarChart3 } from 'lucide-react';

export const Header = () => {
  return (
    <header className="bg-white shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center">
            <BarChart3 className="h-8 w-8 text-indigo-600" />
            <h1 className="ml-3 text-2xl font-bold text-gray-900">Kafka Dashboard</h1>
          </div>
          <nav className="flex space-x-4">
            <a href="/" className="text-gray-600 hover:text-gray-900">Dashboard</a>
            <a href="/settings" className="text-gray-600 hover:text-gray-900">Settings</a>
          </nav>
        </div>
      </div>
    </header>
  );
};