// hooks/useIoTData.ts
import useSWR from "swr";
import { IoTDataResponse } from "@/constants/interfaces";
import { useState, useEffect } from "react";
import { fetcher } from "@/utils/utils";

export function useIoTData(
  page: number,
  pageSize: number = 10,
  topic: string = "",
) {
  const [apiUrl, setApiUrl] = useState<string>("");

  useEffect(() => {
    const baseURL =
      process.env.REACT_APP_API_URL ||
      window.location.origin.replace(":3000", ":5000");
    setApiUrl(`${baseURL}/iot_data`);
  }, []);

  const { data, error } = useSWR<IoTDataResponse>(
    apiUrl
      ? `${apiUrl}?page=${page}&size=${pageSize}${topic ? `&topic=${encodeURIComponent(topic)}` : ""}`
      : null,
    fetcher,
  );

  return {
    iotData: data?.data,
    totalPages: data?.total_pages,
    isLoading: !error && !data,
    isError: error,
  };
}
