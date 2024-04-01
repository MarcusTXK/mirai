import useSWR from "swr";
import { ChatlogsResponse } from "@/constants/interfaces";
import { useEffect, useState } from "react";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export function useChatLogs(page: number, pageSize: number = 10) {
  const [apiUrl, setApiUrl] = useState<string>("");

  useEffect(() => {
    // This code runs only in the browser, where `window` is defined
    const baseURL =
      process.env.REACT_APP_API_URL ||
      window.location.origin.replace(":3000", ":5000");
    setApiUrl(baseURL);
  }, []); // Empty dependency array means this runs once on mount

  const { data, error } = useSWR<ChatlogsResponse>(
    apiUrl ? `${apiUrl}/chatlog?page=${page}&size=${pageSize}` : null, // Only fetch when apiUrl is set
    fetcher,
  );

  return {
    chatlog: data?.data,
    totalPages: data?.total_pages,
    isLoading: !error && !data,
    isError: error,
  };
}
