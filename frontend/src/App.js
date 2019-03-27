import React, { Component } from "react";
import io from "socket.io-client";

import "./App.css";
import LoginForm from "./Components/LoginForm/LoginForm";
import Dashboard from "./Components/Dashboard/Dashboard";

class App extends Component {
  constructor(props, context) {
    super(props, context);
    this.state = {
      authenticated: false
    };
    this.handleLogin = this.handleLogin.bind(this);
    this.handleLogout = this.handleLogout.bind(this);
  }

  handleLogin(e) {
    e.preventDefault();
    console.log(e);
    this.setState(prevState => {
      return {
        authenticated: true
      };
    });
  }

  handleLogout(e) {
    e.preventDefault();
    this.setState(prevState => {
      return {
        authenticated: false
      };
    });
  }

  render() {
    return (
      <div className="App">
        {this.state.authenticated ? (
          <Dashboard io={io} handleLogout={this.handleLogout} />
        ) : (
          <LoginForm handleLogin={this.handleLogin} />
        )}
      </div>
    );
  }
}

export default App;
