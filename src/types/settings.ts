export type MessageFormat = 'JSON' | 'AVRO';

export interface TopicConfig {
  name: string;
  format: MessageFormat;
  schemaFile?: File;
}

export interface KafkaSettings {
  topics: TopicConfig[];
}