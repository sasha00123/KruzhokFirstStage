/* eslint react/jsx-props-no-spreading: off */
import React from 'react';
import { Switch, Route } from 'react-router-dom';
import routes from './constants/routes.json';
import App from './containers/App';
import WelcomePage from './pages/Welcome/Welcome';
import AnnotsPage from './pages/AnnotsPage/AnnotsPage';
import Deps from './pages/Deps/Deps';

export default function Routes() {
  return (
    <App>
      <Switch>
        <Route path={routes.DEPENDENCIES} component={Deps}/>
        <Route path={routes.ANNOTATIONS} component={AnnotsPage}/>
        <Route path={routes.WELCOME} component={WelcomePage}/>
      </Switch>
    </App>
  );
}
