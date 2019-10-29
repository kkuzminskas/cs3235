import React from 'react';
import api from './backend/api';
import AuthForm from "./AuthForm";
import PasswordGrid from "./PasswordGrid";

const progress = {
  USERNAME: 1,
  PASSWORD: 2,
  CONFIRM_PASSWORD: 3
};

class RegisterPage extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      username: props.location.state && props.location.state.username ? props.location.state.username : '',
      password: null,
      progress: progress.USERNAME,
      error: null
    };

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleCancel = this.handleCancel.bind(this);
    this.handlePwFinish = this.handlePwFinish.bind(this);
    this.handleConfirmPwFinish = this.handleConfirmPwFinish.bind(this);
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

    api.checkUsernameAvailability(this.state.username)
      .then((isAvailable) => {
        this.setState(isAvailable ? { progress: progress.PASSWORD, error: null } :
                                          { error: 'This username is taken.' });
      });
  }

  handleCancel() {
    this.setState({ progress: progress.USERNAME });
  }

  handlePwFinish(password) {
    this.setState({ password, progress: progress.CONFIRM_PASSWORD })
  }

  handleConfirmPwFinish(confirmPassword, height, width) {
    api.register(this.state.username, this.state.password, confirmPassword, height, width)
      .then(() => this.props.history.push(`/home`))
      .catch(() => this.setState({ progress: progress.USERNAME, error: 'Failed to register new user.' }));
  }

  render() {
    const errorField = (
      <div className="failure">{this.state.error}</div>
    );

    const usernameFields = (
      <AuthForm username={this.state.username}
                onChange={this.handleChange}
                onSubmit={this.handleSubmit}
                prependedFields={<h2>Register a new user</h2>}
                appendedFields={this.state.error ? errorField : null}/>
    );

    const passwordGrid = (
      <PasswordGrid prePrompt={`Hi ${this.state.username}, please set your password.`}
                    onCancel={this.handleCancel}
                    onSubmit={this.handlePwFinish} />
    );

    const confirmPasswordGrid = (
      <PasswordGrid prePrompt="Please confirm your password"
                    onCancel={this.handleCancel}
                    onSubmit={this.handleConfirmPwFinish} />
    );

    if (this.state.progress === progress.USERNAME) {
      return usernameFields;
    } else if (this.state.progress === progress.PASSWORD) {
      return passwordGrid;
    } else {
      return confirmPasswordGrid;
    }
  }
}

export default RegisterPage;
