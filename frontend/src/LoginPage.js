import React from 'react';
import api from './backend/api';
import AuthForm from "./AuthForm";
import PasswordGrid from "./PasswordGrid";

const progress = {
  USERNAME: 1,
  PASSWORD: 2
};

class LoginPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      username: this.props.username ? this.props.username : '',
      progress: progress.USERNAME,
      error: null
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handleLogin = this.handleLogin.bind(this);
    this.handleRegisterPressed = this.handleRegisterPressed.bind(this);
  }

  handleChange(e) {
    const username = e.target.value.trim();
    this.setState({ username });
  }

  handleSubmit(e) {
    e.preventDefault();
    if (this.state.username === '') {
      return;
    }

    this.setState({ progress: progress.PASSWORD, error: null });
  }

  handleCancel() {
    this.setState({ progress: progress.USERNAME });
  }

  handleLogin(password, height, width) {
    api.login(this.state.username, password, height, width)
      .then(() => this.props.history.push(`/home`))
      .catch(() => this.setState({ progress: progress.USERNAME, error: 'Failed to log in.' }));
  }

  handleRegisterPressed() {
    this.props.history.push({ pathname: '/register', state: { username: this.state.username } });
  }

  render() {
    const errorField = (
      <div className="failure">{this.state.error}</div>
    );

    const registerButton = (
      <input type="button" value="Register" onClick={this.handleRegisterPressed}/>
    );

    const usernameFields = (
      <AuthForm username={this.state.username}
                onChange={this.handleChange}
                onSubmit={this.handleSubmit}
                prependedFields={<h1>Eye tracking authentication demo</h1>}
                appendedFields={this.state.error ? errorField : null}
                additionalButtons={registerButton}/>
    );

    const passwordGrid = (
      <PasswordGrid prePrompt={`Hi ${this.state.username}!`} onCancel={this.handleCancel} onSubmit={this.handleLogin} />
    );

    return this.state.progress === progress.USERNAME ? usernameFields : passwordGrid;
  }
}

export default LoginPage;
