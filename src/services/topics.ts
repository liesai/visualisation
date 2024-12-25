import { TopicConfig } from '../types/settings';
import { socket } from './socket';

export async function saveTopics(topics: TopicConfig[]) {
  try {
    const response = await fetch('/api/topics', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ topics }),
    });

    if (!response.ok) {
      throw new Error('Failed to save topics');
    }

    // Notify backend about topic changes
    socket.emit('update_topics', { topics });
  } catch (error) {
    console.error('Error saving topics:', error);
    throw error;
  }
}

export async function getTopics() {
  try {
    const response = await fetch('/api/topics');
    if (!response.ok) {
      throw new Error('Failed to fetch topics');
    }
    return await response.json();
  } catch (error) {
    console.error('Error fetching topics:', error);
    throw error;
  }
}