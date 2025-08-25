# Posture Feedback Application

This application allows users to upload dance videos and receive feedback on their posture. It utilizes MediaPipe and OpenCV to analyze the uploaded videos and compare the detected postures against a trained model. The application provides suggestions for correcting any identified mistakes.

## Project Structure

```
posture-feedback-app
├── src
│   ├── main.py                # Entry point of the application
│   ├── video_upload.py        # Handles video uploads
│   ├── posture_analysis.py     # Analyzes video for posture
│   ├── feedback_generator.py   # Generates feedback based on analysis
│   └── utils
│       └── mediapipe_utils.py  # Utility functions for MediaPipe
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
└── trained_model
    └── model.pkl              # Trained model for posture analysis
```

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd posture-feedback-app
   ```

2. **Install Dependencies**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   Start the application by executing:
   ```bash
   python src/main.py
   ```

4. **Upload a Video**
   Access the application through your web browser and upload a dance video in the supported format.

## Usage Guidelines

- After uploading a video, the application will process it and analyze the dance postures.
- Feedback will be generated based on the analysis, highlighting areas for improvement.

## Overview of Functionality

- **Video Upload**: Users can upload their dance videos, which are stored for analysis.
- **Posture Analysis**: The application processes each frame of the video using MediaPipe and OpenCV to extract posture data.
- **Feedback Generation**: Based on the analysis, the application provides feedback on the user's posture, identifying mistakes and suggesting corrections.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.