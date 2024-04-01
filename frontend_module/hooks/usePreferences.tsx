import useSWR from "swr";
import { useEffect, useState } from "react";
import { PreferencesResponse } from "@/constants/interfaces";
import { fetcher } from "@/utils/utils";

export function usePreferences(page: number, pageSize: number = 10) {
  const [apiUrl, setApiUrl] = useState<string>("");

  useEffect(() => {
    // This code runs only in the browser, where `window` is defined
    const baseURL =
      process.env.REACT_APP_API_URL ||
      window.location.origin.replace(":3000", ":5000");
    setApiUrl(baseURL);
  }, []);

  const { data, error } = useSWR<PreferencesResponse>(
    apiUrl ? `${apiUrl}/preferences?page=${page}&size=${pageSize}` : null,
    fetcher,
  );

  return {
    preferences: data?.data,
    totalPages: data?.total_pages,
    isLoading: !error && !data,
    isError: error,
  };
}
