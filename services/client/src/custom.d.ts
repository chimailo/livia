export interface AuthPayload {
  token: string | null;
}

export type AuthState = {
  isAuthenticated: boolean;
  loading: boolean;
  user: object | null;
} & AuthPayload;

interface LoginParams {
  email: string;
  password: string;
}

type SignupParams = {
  firstname: string;
  lastname: string;
} & LoginParams;
