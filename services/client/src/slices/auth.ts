import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import axios from 'axios';

import { AppThunk } from '../store';
import { AuthPayload, AuthState, LoginParams, SignupParams } from '../custom';
import setAuthToken from '../utils/axiosConfig';

const initialState: AuthState = {
  token: localStorage.getItem('token'),
  isAuthenticated: false,
  loading: true,
  user: null,
};

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    authSuccess(state, { payload }: PayloadAction<{ data: object }>) {
      state.loading = false;
      state.isAuthenticated = true;
      state.user = payload;
    },
    signinSuccess(state, { payload }: PayloadAction<AuthPayload>) {
      payload.token && localStorage.setItem('token', payload.token);
      state.loading = false;
      state.isAuthenticated = true;
      state.token = payload.token;
    },
    authError(state) {
      localStorage.removeItem('token');
      state.token = null;
      state.loading = false;
      state.isAuthenticated = false;
    },
  },
});

export const { authSuccess, signinSuccess, authError } = authSlice.actions;

export default authSlice.reducer;

export const loadUser = (): AppThunk => async (dispatch) => {
  localStorage.token && setAuthToken(localStorage.token);

  try {
    const response = await axios.get('/auth/user');

    dispatch(authSuccess(response.data));
  } catch (error) {
    // const message = error.response.data.message;

    dispatch(authError());
  }
};

export const signup = (values: SignupParams): AppThunk => async (dispatch) => {
  const { firstname, lastname, email, password } = values;

  const body = JSON.stringify({ firstname, lastname, email, password });

  try {
    const response = await axios.post('/auth/register', body);

    dispatch(signinSuccess(response.data));
    dispatch(loadUser());
  } catch (error) {
    // const message = error.response.data.message;

    dispatch(authError());
  }
};

export const login = (values: LoginParams): AppThunk => async (dispatch) => {
  const { email, password } = values;

  const body = JSON.stringify({ email, password });

  try {
    const response = await axios.post('/auth/login', body);

    dispatch(signinSuccess(response.data));
    dispatch(loadUser());
  } catch (error) {
    // const message = error.response.data.message;

    dispatch(authError());
  }
};

export const logout = (): AppThunk => async (dispatch) => dispatch(authError());
