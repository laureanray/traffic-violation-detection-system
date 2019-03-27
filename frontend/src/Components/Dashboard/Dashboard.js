import React, { Component } from "react";
import "./Dashboard.css";
class Dashboard extends Component {
  constructor(props, context) {
    super(props, context);

    this.state = {
      attached: false,
      logs: '',
      originalFrame: false,
      bdm: false,
      webcam: true
    };

    this.socket = null;
    this.toggleOriginalFrame = this.toggleOriginalFrame.bind(this); 
    this.toggleBdm = this.toggleBdm.bind(this);
    this.toggleWebCam = this.toggleWebCam.bind(this);
  }

  toggleWebCam(){
    this.setState((prevState) => {
      return {
        webcam: !prevState.webcam
      }
    });
    this.socket.emit('source', {
      source: 'webcam'
    });
  }

  toggleBdm(){
    this.setState((prevState) => {
      return {
        bdm: !prevState.bdm,
        originalFrame: false,
      }
    });
    this.socket.emit('button', {
      toggle: 'bdm'
    });
  }

  toggleOriginalFrame(){
    console.log('toggle');
    this.setState((prevState) => {
      return {
        originalFrame: !prevState.originalFrame,
        bdm: false,
      }
    });
    this.socket.emit('button', {
      toggle: 'original'
    });
  }

  componentDidMount() {
    this.socket = this.props.io.connect("http://127.0.0.1:3002");
    this.socket.on("connect", function(data) {
      console.log("connected", this.socket);
      });

      // socket.emit('something', {'data': 'hello'});

    this.socket.on("log", data => {
      this.setState((prevState) => {
        return {
          logs: prevState.logs + data.data + '\n'
        }
      });
    });
  }

  render() {
    return (
      <div className="Dashboard">
        <nav>
          <div className="brand">
            <h1> Traffic Violation Detection System </h1>
          </div>
          <ul>
            <li>
              <a href="test"> Home </a>
            </li>
            <li>
              <a href="test"> Database </a>
            </li>
            <li>
              <a href="test"> Operations </a>
            </li>
            <li>
              <button onClick={this.props.handleLogout}> Logout </button>
            </li>
          </ul>
        </nav>
        <div className="wrapper">
        <div className="Cameras">
          <img
            src="http://127.0.0.1:3002/video_feed"
            className="CameraPreview"
            alt="Camera"
          />
            <div className="buttons">
              <input placeholder="Enter URL" id="source"/>
              <button onClick={this.toggleurl} className={this.state.url && "active"}> URL </button>
              <button onClick={this.toggleWebCam} className={this.state.webcam && "active"}> Webcam </button>
              <button onClick={this.toggleOriginalFrame} className={this.state.originalFrame && "active"}> Original Frame </button>
              <button onClick={this.toggleBdm}  className={this.state.bdm && "active"}> Background Difference </button>
            </div>
        </div>
        <div className="Logging">
            <h1>System Logs</h1> 
            <textarea name="" value={this.state.logs} id="log" cols="30" rows="10" />
          </div>
      </div>
         </div> 
    );
  }
}

export default Dashboard;
