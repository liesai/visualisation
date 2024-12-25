export interface KafkaMessage {
  topic: string;
  partition: number;
  offset: number;
  value: any;
  timestamp: number;
}

export interface TopicMetrics {
  messageCount: number;
  bytesProcessed: number;
  lastUpdate: string; // Changed from Date to string since we receive ISO string from backend
}

export interface DashboardMetrics {
  [topic: string]: TopicMetrics;
}