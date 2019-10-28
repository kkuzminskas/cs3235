import React from "react";
import './AuthForm.css';

class AuthForm extends React.Component {
  // props:
  // - username: string
  // - onChange: (event) => void
  // - onSubmit: (event) => void
  // - prependedFields: React.Component
  // - appendedFields: React.Component
  // - additionalButtons: React.Component
  render() {
    return (
      <div className="centralize">
        {this.props.prependedFields}
        <form className="form" onSubmit={this.props.onSubmit}>
          <label>
            Username:
            <input id="username" type="text" value={this.props.username} required maxLength="15" onChange={this.props.onChange}/>
          </label>
          <div className="buttons-wrapper">
            {this.props.additionalButtons}
            <input type="submit" value="Enter password" />
          </div>
        </form>
        {this.props.appendedFields}
      </div>
    );
  }
}

export default AuthForm;
