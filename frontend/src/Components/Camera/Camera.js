import React, {Component} from 'react';
import "./Camera.css";
class Camera extends Component {
    render() {
        return (
            <div className="Camera">
                <img src="http://127.0.0.1:5000/video_feed" alt="camera_feed"/>
            </div>
        );
    }
}

export default Camera;