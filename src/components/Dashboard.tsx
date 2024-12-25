import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { MetricsCard } from './MetricsCard';
import { DashboardMetrics } from '../types/kafka';
import { socket } from '../services/socket';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

export const Dashboard = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics>({});
  const [chartData, setChartData] = useState<any>({
    labels: [],
    datasets: []
  });

  useEffect(() => {
    socket.on('metrics', (newMetrics: DashboardMetrics) => {
      setMetrics(newMetrics);
      updateChartData(newMetrics);
    });

    return () => {
      socket.off('metrics');
    };
  }, []);

  const updateChartData = (newMetrics: DashboardMetrics) => {
    const timestamp = new Date().toLocaleTimeString();
    
    setChartData(prev => ({
      labels: [...prev.labels, timestamp].slice(-10),
      datasets: Object.entries(newMetrics).map(([topic, data]) => ({
        label: topic,
        data: [...(prev.datasets.find((d: any) => d.label === topic)?.data || []), 
              data.messageCount].slice(-10),
        borderColor: `hsl(${Math.random() * 360}, 70%, 50%)`,
        tension: 0.4
      }))
    }));
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
        {Object.entries(metrics).map(([topic, topicMetrics]) => (
          <MetricsCard key={topic} topic={topic} metrics={topicMetrics} />
        ))}
      </div>
      
      <div className="bg-white rounded-lg shadow p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Message Flow</h3>
        <div className="h-96">
          <Line
            data={chartData}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                y: {
                  beginAtZero: true
                }
              }
            }}
          />
        </div>
      </div>
    </div>
  );
};