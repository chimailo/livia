import { combineReducers } from '@reduxjs/toolkit';
import authReducer from './slices/auth';

const rootReducer = combineReducers({
  auth: authReducer,
});

export type RootState = ReturnType<typeof rootReducer>;

export default rootReducer;
