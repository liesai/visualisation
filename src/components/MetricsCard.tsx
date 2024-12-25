import React from 'react';
import { TopicMetrics } from '../types/kafka';

interface MetricsCardProps {
  topic: string;
  metrics: TopicMetrics;
}

export const MetricsCard: React.FC<MetricsCardProps> = ({ topic, metrics }) => {
  // Parse the ISO string into a Date object
  const lastUpdateDate = new Date(metrics.lastUpdate);

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-medium text-gray-900">{topic}</h3>
      <dl className="mt-4 grid grid-cols-2 gap-4">
        <div>
          <dt className="text-sm font-medium text-gray-500">Messages</dt>
          <dd className="mt-1 text-2xl font-semibold text-indigo-600">
            {metrics.messageCount.toLocaleString()}
          </dd>
        </div>
        <div>
          <dt className="text-sm font-medium text-gray-500">Bytes Processed</dt>
          <dd className="mt-1 text-2xl font-semibold text-indigo-600">
            {(metrics.bytesProcessed / 1024).toFixed(2)} KB
          </dd>
        </div>
      </dl>
      <div className="mt-4 text-sm text-gray-500">
        Last updated: {lastUpdateDate.toLocaleTimeString()}
      </div>
    </div>
  );
};