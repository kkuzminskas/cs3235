import React from 'react';
import {BrowserRouter, Switch, Route} from "react-router-dom";
import LoginPage from "./LoginPage";
import RegisterPage from "./RegisterPage";
import HomePage from "./HomePage";
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <Switch>
        <Route exact path="/login" component={LoginPage}/>
        <Route exact path="/register" component={RegisterPage}/>
        <Route exact path="/home" component={HomePage}/>
        <Route component={HomePage}/>
      </Switch>
    </BrowserRouter>
  );
}

export default App;
