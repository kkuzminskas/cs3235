import React from 'react';
import {fetchToken} from './backend/utilities';
import api from './backend/api';

class HomePage extends React.Component {
  constructor(props) {
    super(props);

    const token = fetchToken();
    if (!token) {
      props.history.push('/login');
    }

    this.state = { token, username: null, error: null };

    this.handleLogout = this.handleLogout.bind(this);
  }

  componentDidMount() {
    if (this.state.token) {
      api.validateToken(this.state.token)
        .then((user) => this.setState(user))
        .catch(() => this.props.history.push('/login'));
    }
  }

  handleLogout() {
    api.logout()
      .then(() => this.props.history.push('/login'))
      .catch(() => this.setState({ error: 'Failed to log out' }));
  }

  render() {
    const errorField = (
      <div className="failure">{this.state.error}</div>
    );

    return this.state.username ? (
      <div className="centralize">
        <h1>Welcome {this.state.username}!</h1>
        <button onClick={this.handleLogout}>Logout</button>
        {this.state.error ? errorField : null}
      </div>
    ) : null;
  }
}

export default HomePage;
