export interface CreatePreferenceDTO {
  description: string;
  updatedBy: string;
}

export interface CreateChatlogDTO {
  sentBy: string;
  message: string;
}

export interface PreferenceDTO {
  id: number;
  description: string;
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
  updatedBy: string;
}

export interface ChatlogDTO {
  id: number;
  time: string; // ISO date string
  sentBy: string;
  message: string;
}

export interface PaginationResponse<T> {
  data: T[];
  total_pages: number;
}

export interface IoTDataDTO {
  id: number;
  topic: string;
  unit: string;
  location: string;
  data: any; // raw json
  time: string; // ISO date string
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
}

export type PreferencesResponse = PaginationResponse<PreferenceDTO>;
export type ChatlogsResponse = PaginationResponse<ChatlogDTO>;
export type IoTDataResponse = PaginationResponse<IoTDataDTO>;
