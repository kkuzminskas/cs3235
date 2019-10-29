import React from 'react';
import eyeTracker from './backend/eyetracking';
import './PasswordGrid.css';

const progress = {
  WAITING: 1,
  DRAWING: 2
};

class PasswordGrid extends React.Component {
  // props:
  // - prePrompt: string
  // - onSubmit: (password, height, width) => void
  // - onCancel: () => void
  constructor(props) {
    super(props);

    this.state = {
      progress: progress.WAITING,
      height: null,
      width: null
    };
    this.gridElem = null;

    this.onKeyPressed = this.onKeyPressed.bind(this);
    this.onSpacePressed = this.onSpacePressed.bind(this);
  }

  componentDidMount(){
    document.addEventListener("keydown", this.onKeyPressed, false);
    eyeTracker.wakeUpEyeTracker();
    const height = this.gridElem.clientHeight;
    const width = this.gridElem.clientWidth;
    this.setState({ height, width })
  }

  componentWillUnmount(){
    document.removeEventListener("keydown", this.onKeyPressed, false);
    if (this.state.progress === progress.DRAWING) {
      eyeTracker.stopTracking();
    }
  }

  onKeyPressed(e) {
    if (e.isComposing || e.keyCode === 229 || e.repeat) {
      return;
    }
    // Space key
    if (e.keyCode === 32) {
      this.onSpacePressed();
    }
    // Esc key
    if (e.keyCode === 27) {
      if (this.state.progress === progress.DRAWING) {
        eyeTracker.stopTracking();
      }
      this.setState({ progress: progress.WAITING });
      this.props.onCancel();
    }
  }

  onSpacePressed() {
    switch (this.state.progress) {
      case progress.WAITING:
        this.setState({ progress: progress.DRAWING });
        eyeTracker.startTracking();
        break;
      case progress.DRAWING:
        this.setState({ progress: progress.WAITING });
        eyeTracker.finishTracking();
        this.props.onSubmit(eyeTracker.getData(), this.state.height, this.state.width);
        break;
      default:

    }
  }

  render() {
    const startPrompt = (
      <div className="full-height full-width float-top password-prompt">
        <div>
          {this.props.prePrompt ? (<div>{this.props.prePrompt}</div>) : null}
          <div>Click anywhere or Press space to start recording your password. Press Esc to quit.</div>
        </div>
      </div>
    );

    const stopPrompt = (
      <div className="full-width float-bottom password-prompt">
        <div>Click anywhere or Press space to finish recording. Press Esc to quit.</div>
      </div>
    );

    const cell = (
      <div className="password-cell">
        <div className="dot"/>
      </div>
    );

    const column = (
      <div className="password-col">
        {cell}
        {cell}
        {cell}
      </div>
    );

    return (
      <div className="full-height full-width password-grid"
           onClick={this.onSpacePressed}
           ref={(elem) => this.gridElem = elem}>
        {column}
        {column}
        {column}
        {this.state.progress === progress.WAITING ? startPrompt :
                                                  this.state.progress === progress.DRAWING ? stopPrompt : null}
      </div>
    );
  }
}

export default PasswordGrid;
