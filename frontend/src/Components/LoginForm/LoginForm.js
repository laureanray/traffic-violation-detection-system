import React, { Component } from "react";
import { Route, Link, Redirect, withRouter } from "react-router-dom";
import "./LoginForm.css";
class Login extends Component {
  constructor(props, context) {
    super(props, context);
  }

  render() {
    return (
      <div className="Login">
        <h1> Traffic Violation Detection System </h1>
        <p className="subtitle"> Version 1.0.0</p>
        <form action="" onSubmit={this.props.handleLogin} className="LoginForm">
          <h2> Administrator Login</h2>
          <input
            type="text"
            placeholder="Username"
            autoComplete="false"
            name="username"
          />
          <input
            type="password"
            placeholder="Password"
            autoComplete="false"
            name="password"
          />

          <input
            type="text"
            placeholder="IP Address"
            autoComplete="false"
            name="ip"
            id="ip"
          />
          <button> Login </button>
          <p className="footer">Copyright &copy; 2019 TVDS. </p>
        </form>
      </div>
    );
  }
}

export default Login;
