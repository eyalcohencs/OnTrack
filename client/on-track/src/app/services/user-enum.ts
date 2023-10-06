export interface User {
  id?: number;
  first_name: string;
  last_name: string;
  email: string;
  user_type?: string;
  username: string;
  password?: string;
}

export enum UserType {
  SYSTEM = 'system',
  REGULAR = 'regular',
  INACTIVE = 'inactive'
}