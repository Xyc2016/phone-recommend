import { useState, useEffect, useCallback } from 'react';
import { Thread } from '../types';
import { getThreads, createThread, deleteThread } from '../services/api';

export const useThreads = () => {
  const [threads, setThreads] = useState<Thread[]>([]);
  const [loading, setLoading] = useState(true);

  const loadThreads = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getThreads();
      setThreads(data);
    } catch (error) {
      console.error('Failed to load threads:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadThreads();
  }, [loadThreads]);

  const addThread = useCallback(async () => {
    try {
      const newThread = await createThread();
      setThreads((prev) => [newThread, ...prev]);
      return newThread;
    } catch (error) {
      console.error('Failed to create thread:', error);
      throw error;
    }
  }, []);

  const removeThread = useCallback(async (id: string) => {
    try {
      await deleteThread(id);
      setThreads((prev) => prev.filter((t) => t.id !== id));
    } catch (error) {
      console.error('Failed to delete thread:', error);
    }
  }, []);

  return {
    threads,
    loading,
    addThread,
    removeThread,
    refreshThreads: loadThreads,
  };
};

