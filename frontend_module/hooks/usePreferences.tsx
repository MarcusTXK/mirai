import useSWR from 'swr';
import { useState } from 'react';
import { PreferencesResponse } from '@/constants/interfaces';

const fetcher = (url: string) => fetch(url).then(res => res.json());

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000"

export function usePreferences(page: number, pageSize: number = 10) {
  const { data, error } = useSWR<PreferencesResponse>(`${API_URL}/preferences?page=${page}&size=${pageSize}`, fetcher);

  return {
    preferences: data?.data,
    totalPages: data?.total_pages,
    isLoading: !error && !data,
    isError: error,
  };
}
