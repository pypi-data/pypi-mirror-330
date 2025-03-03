export interface ICPGPortalFile {
  name: string;
  file_type: string;
  size: number;
  saved: boolean;
  tags: string[];
  id: string;
  run_id: string;
  created_at: string;
}

export interface ICPGPortalContents {
  data: ICPGPortalFile[];
  count: number;
}
