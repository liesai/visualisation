import React, { useState } from 'react';
import { Settings as SettingsIcon, Plus, Trash2 } from 'lucide-react';
import { TopicConfig, MessageFormat } from '../types/settings';
import { socket } from '../services/socket';

export const Settings = () => {
  const [topics, setTopics] = useState<TopicConfig[]>([]);
  const [newTopic, setNewTopic] = useState<string>('');
  const [selectedFormat, setSelectedFormat] = useState<MessageFormat>('JSON');
  const [schemaFile, setSchemaFile] = useState<File | null>(null);

  const handleAddTopic = () => {
    if (!newTopic.trim()) return;

    const topicConfig: TopicConfig = {
      name: newTopic.trim(),
      format: selectedFormat,
      schemaFile: schemaFile || undefined
    };

    setTopics([...topics, topicConfig]);
    socket.emit('update_topics', { topics: [...topics, topicConfig] });
    
    // Reset form
    setNewTopic('');
    setSelectedFormat('JSON');
    setSchemaFile(null);
  };

  const handleRemoveTopic = (index: number) => {
    const updatedTopics = topics.filter((_, i) => i !== index);
    setTopics(updatedTopics);
    socket.emit('update_topics', { topics: updatedTopics });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSchemaFile(file);
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex items-center mb-6">
          <SettingsIcon className="h-6 w-6 text-indigo-600 mr-2" />
          <h2 className="text-xl font-semibold text-gray-900">Kafka Settings</h2>
        </div>

        <div className="space-y-6">
          {/* Topic List */}
          <div className="space-y-4">
            {topics.map((topic, index) => (
              <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-gray-900">{topic.name}</p>
                  <p className="text-sm text-gray-500">Format: {topic.format}</p>
                  {topic.schemaFile && (
                    <p className="text-sm text-gray-500">Schema: {topic.schemaFile.name}</p>
                  )}
                </div>
                <button
                  onClick={() => handleRemoveTopic(index)}
                  className="text-red-600 hover:text-red-800"
                >
                  <Trash2 className="h-5 w-5" />
                </button>
              </div>
            ))}
          </div>

          {/* Add New Topic Form */}
          <div className="border-t pt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Add New Topic</h3>
            <div className="space-y-4">
              <div>
                <label htmlFor="topic-name" className="block text-sm font-medium text-gray-700">
                  Topic Name
                </label>
                <input
                  type="text"
                  id="topic-name"
                  value={newTopic}
                  onChange={(e) => setNewTopic(e.target.value)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                  placeholder="Enter topic name"
                />
              </div>

              <div>
                <label htmlFor="message-format" className="block text-sm font-medium text-gray-700">
                  Message Format
                </label>
                <select
                  id="message-format"
                  value={selectedFormat}
                  onChange={(e) => setSelectedFormat(e.target.value as MessageFormat)}
                  className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
                >
                  <option value="JSON">JSON</option>
                  <option value="AVRO">AVRO</option>
                </select>
              </div>

              {selectedFormat === 'AVRO' && (
                <div>
                  <label htmlFor="schema-file" className="block text-sm font-medium text-gray-700">
                    Schema File
                  </label>
                  <input
                    type="file"
                    id="schema-file"
                    accept=".json,.avsc"
                    onChange={handleFileChange}
                    className="mt-1 block w-full text-sm text-gray-500
                             file:mr-4 file:py-2 file:px-4
                             file:rounded-md file:border-0
                             file:text-sm file:font-semibold
                             file:bg-indigo-50 file:text-indigo-700
                             hover:file:bg-indigo-100"
                  />
                </div>
              )}

              <button
                onClick={handleAddTopic}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <Plus className="h-5 w-5 mr-2" />
                Add Topic
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};