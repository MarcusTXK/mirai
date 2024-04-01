import useSWR from "swr";
import { ChatlogsResponse, PreferencesResponse } from "@/constants/interfaces";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:5000";

export function useChatLogs(page: number, pageSize: number = 10) {
  const { data, error } = useSWR<ChatlogsResponse>(
    `${API_URL}/chatlog?page=${page}&size=${pageSize}`,
    fetcher,
  );

  return {
    chatlog: data?.data,
    totalPages: data?.total_pages,
    isLoading: !error && !data,
    isError: error,
  };
}
