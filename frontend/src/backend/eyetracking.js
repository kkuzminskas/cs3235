class EyeTracker {
  constructor() {
    this.data = null;
  }

  wakeUpEyeTracker() {

  }

  startTracking() {
    this.data = null;
  }

  stopTracking() {

  }

  finishTracking() {

  }

  getData() {
    return this.data;
  }
}

const eyeTracker = new EyeTracker();

export default eyeTracker;
