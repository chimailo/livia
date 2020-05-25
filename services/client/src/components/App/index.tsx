import React, { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import axios from 'axios';

import Boards from '../Pages/Boards';
import Home from '../Pages/Home';
import Landing from '../Pages/Landing';
import Login from '../Pages/Login';
import Navigation from '../Navigation';
import Signup from '../Pages/Signup';
import Team from '../Pages/Team';
import Templates from '../Pages/Templates';
import * as ROUTES from '../../utils/routes';
import { loadUser } from '../../slices/auth';
import setAuthToken from '../../utils/axiosConfig';

(function () {
  axios.defaults.baseURL = process.env.REACT_APP_API_URL;
  axios.defaults.headers.post['Content-Type'] = 'application/json';
})();

export default function App() {
  const dispatch = useDispatch();

  localStorage.token && setAuthToken(localStorage.token);

  useEffect(() => {
    dispatch(loadUser());
  }, [dispatch]);

  return (
    <Router>
      <Navigation />
      <Switch>
        <Route exact path={ROUTES.LANDING}>
          <Landing />
        </Route>
        <Route exact path={ROUTES.HOME}>
          <Home />
        </Route>
        <Route exact path={ROUTES.BOARDS}>
          <Boards />
        </Route>
        <Route exact path={ROUTES.TEAM}>
          <Team />
        </Route>
        <Route exact path={ROUTES.TEMPLATES}>
          <Templates />
        </Route>
        <Route exact path={ROUTES.SIGNUP}>
          <Signup />
        </Route>
        <Route exact path={ROUTES.LOGIN}>
          <Login />
        </Route>
      </Switch>
    </Router>
  );
}
