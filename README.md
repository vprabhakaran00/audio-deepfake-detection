# Audio Deepfake Detection App

This project is an audio file deepfake detection application built using Flask, Python, and a Convolutional Neural Network (CNN). The application allows users to upload `.mp3` or `.wav` audio files and receive predictions based on the neural network.

## Table of Contents

- [Features](#features)
- [Project Overview](#project-overview)
- [Data Source](#data-source)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [How the App Works](#how-the-app-works)
- [DVC for Pipeline Tracking](#dvc-for-pipeline-tracking)
- [Dockerization](#dockerization)
- [Continuous Integration and Deployment](#continuous-integration-and-deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- Upload `.mp3` or `.wav` audio files.
- Receive predictions on the uploaded audio files.
- Audio playback supported after uploading a file.
- Visual feedback on the prediction results.
- Supports Docker for easy deployment.
- Efficient pipeline management using DVC.

## Project Overview

The core of the application is a Convolutional Neural Network (CNN) based on the MobileNetV3Large architecture. This base model is augmented with a few additional layers to form the final model used for processing audio data and generating predictions. 

## Data Source

The dataset used for training the model was obtained from Kaggle. The dataset can be found in the following Kaggle directory: [Deep Voice: Deepfake Voice Recognition](https://www.kaggle.com/datasets/birdy654/deep-voice-deepfake-voice-recognition).

## Requirements

- Python 3.9.13
- Flask
- DVC (Data Version Control) for pipeline tracking
- Docker (optional, for containerization)
- GitHub Actions (optional, for CI/CD)
- Azure (optional, for cloud deployment)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/audio-file-prediction.git
cd audio-file-prediction
```

### 2. Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Running the Pipeline End-to-End (Optional)

If you wish to run the entire pipeline from start to finish:

1. **Download the Dataset:** Visit the [Deep Voice: Deepfake Voice Recognition](https://www.kaggle.com/datasets/birdy654/deep-voice-deepfake-voice-recognition) page on Kaggle and copy the download link for the dataset.

2. **Update the Config File:** In the `config` folder, open the `config.yaml` file. Replace the `source_URL` value with the download link you copied from Kaggle.

3. **Run the Pipeline:**

```bash
dvc repro
```

DVC will download the dataset, process it, and run all stages of the pipeline.

## Usage
### Running the Application

To run the Flask application locally:

```bash
python app.py
```

The application will be available at **`http://127.0.0.1:5000`**.

### Uploading Audio Files

1. Go to the application in your browser.
2. Click "Choose File" and select a **`.mp3`** or **`.wav`** file.
3. Click "Predict" to receive the prediction.
4. **Playback**: Once the audio file is uploaded, you can listen to the audio directly on the app using the built-in audio player.

## How the App Works

1. **Model Details:** The application uses a custom-trained model based on the MobileNetV3Large architecture, with a few additional layers added on top to adapt the model to the specific prediction task.

2. **Convolutional Neural Network (CNN):** The core of the prediction mechanism relies on a Convolutional Neural Network, which is highly effective for processing and classifying images, including spectrograms generated from audio files.

3. **Audio Processing:**
    - When an audio file is uploaded, a random 10-second segment is extracted from the audio.
    - A spectrogram image is generated from this 10-second audio segment, which visually represents the audio frequencies over time.
    - From the spectrogram image, a 224x224 pixel portion is cropped out. This size is chosen to match the input dimensions expected by the MobileNetV3Large model.

4. **Prediction Process:**
    - The 224x224 pixel image is fed into the model to generate a prediction.
    - This process is repeated five times for each uploaded audio file, with different random 10-second segments being used each time.
    - The final prediction is determined by taking the mode of the five predictions.
    - The final confidence score is calculated as the average confidence across the five predictions.

## DVC for Pipeline Tracking

This project uses DVC (Data Version Control) to manage and track the machine learning pipeline.

### Benefits of Using DVC

- **Pipeline Tracking:** DVC allows you to track each stage of the pipeline.
- **Efficient Re-Execution:** With DVC, you can rerun the entire pipeline using the `dvc repro` command. This will only rerun stages where changes have been made, saving time and computational resources.
- **Pipeline Visualization:** You can visualize the relationships and dependencies between the stages in the pipeline using the `dvc dag` command.

### Running the Pipeline

To run the entire pipeline:

```bash
dvc repro
```

If no changes are detected in certain stages, DVC will skip them, ensuring that only the necessary computations are performed.

### Visualizing the Pipeline

To visualize the relationships and dependencies between the stages in the pipeline:

```bash
dvc dag
```

This will generate a graph showing the flow of data through the pipeline, helping you to understand the structure and dependencies of the pipeline.

## Dockerization
### Building the Docker Image
```bash
docker build -t deepfake-detection-app .
```

### Running the Docker Container
```bash
docker run -p 5000:5000 deepfake-detection-app
```

The application will be available at `http://localhost:5000`.

### Dockerizing for Azure

1. Create an Azure Container Registry.
2. Tag your Docker image:
```bash
docker tag deepfake-detection-app:latest <azure-registry-name>.azurecr.io/deepfake-detection-app:latest
```
3. Push the Docker image to Azure:
```bash
docker push <azure-registry-name>.azurecr.io/deepfake-detection-app:latest
```

## Continuous Integration and Deployment

This project uses GitHub Actions for CI/CD. The CI/CD pipeline is defined in `.github/workflows/` directory in a `.yaml` file created through Azure.

## Contributing

Contributions are welcome! Please fork this repository, create a new branch, and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/vprabhakaran00/audio-deepfake-detection?tab=MIT-1-ov-file#) file for details.