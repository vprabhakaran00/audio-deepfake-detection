import io
import librosa
import numpy as np
from scipy import stats
from tensorflow.keras.models import load_model
from flask import Flask, request, render_template, jsonify
from audioClassifier import logger

app = Flask(__name__)

# Load the model once at the startup
model = load_model('artifacts/model_training/model.keras')
logger.info("Model loaded successfully at startup")

class DetectionPipeline:
    def __init__(self, audio_file):
        self.audio_file = audio_file
        
    def _load_test_file(self):
        try:
            audio, sr = librosa.load(io.BytesIO(self.audio_file), sr = 16000)
            return audio, sr
        except Exception as e:
            logger.error(f"Error loading audio file: {e}")
            raise e
    
    def _extract_segment(self, audio, sr, segment_length = 10):
        try:
            segment_length = segment_length * sr
            if len(audio) < segment_length:
                pad_width = segment_length - len(audio)
                audio = np.pad(audio, (0, pad_width), mode = 'constant')
            start = np.random.randint(0, len(audio) - segment_length + 1)
            segment = audio[start:start + segment_length]
            return segment
        except Exception as e:
            logger.error(f"Error extracting segment: {e}")
            raise e
    
    def _create_spectrogram(self, audio, sr, n_fft = 2048, hop_length = 512, n_mels = 128):
        try:
            spectrogram = librosa.feature.melspectrogram(y = audio, sr = sr, n_fft = n_fft, hop_length = hop_length, n_mels = n_mels)
            spectrogram = librosa.power_to_db(spectrogram, ref = np.max)
            return spectrogram
        except Exception as e:
            logger.error(f"Error creating spectrogram: {e}")
            raise e
    
    def _random_crop(self, spectrogram, crop_size):
        try:
            pad_width_x = max(crop_size - spectrogram.shape[1], 0)
            pad_width_y = max(crop_size - spectrogram.shape[0], 0)
            spectrogram = np.pad(spectrogram, ((0, pad_width_y), (0, pad_width_x)), mode='constant')
            max_x = spectrogram.shape[1] - crop_size
            max_y = spectrogram.shape[0] - crop_size
            x = np.random.randint(0, max_x + 1)
            y = np.random.randint(0, max_y + 1)
            cropped_spectrogram = spectrogram[y:y + crop_size, x:x + crop_size]
            return cropped_spectrogram
        except Exception as e:
            logger.error(f"Error randomly cropping spectrogram: {e}")
            raise e
    
    def _create_test_set_from_audio(self):
        try:
            audio, sr = self._load_test_file()
            segment = self._extract_segment(audio, sr, segment_length = 10)
            spectrogram = self._create_spectrogram(segment, sr)
            spectrogram = self._random_crop(spectrogram, crop_size = 224)
            spectrogram = np.expand_dims(spectrogram, axis = -1)
            spectrogram = np.repeat(spectrogram, 3, axis = -1)
            spectrogram = np.expand_dims(spectrogram, axis = 0)
            return spectrogram
        except Exception as e:
            logger.error(f"Error creating test file: {e}")
            raise e
            
    def make_prediction(self):
        try:
            results = []
            confidences = []
            for i in range(5):
                spectrogram = self._create_test_set_from_audio()
                prob = model.predict(spectrogram)[0][0]
                prediction = (prob > 0.59045565).astype(int)
                results.append(prediction)
                confidences.append(prob)
            final_pred = stats.mode(results)[0]
            avg_confidence = np.mean(confidences)
            logger.info("Prediction made successfully.")
            if final_pred == 1:
                return {"prediction": "Fake", "confidence": avg_confidence*100}
            else:
                return {"prediction": "Not Fake", "confidence": (1 - avg_confidence)*100}
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            raise e

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'prediction': 'No file part', 'confidence': 0})
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'prediction': 'No selected file', 'confidence': 0})
        
        if file and (file.filename.endswith('.wav') or file.filename.endswith('.mp3')):
            try:
                audio_data = file.read()
                pipeline = DetectionPipeline(audio_data)
                prediction_data = pipeline.make_prediction()
                return jsonify(prediction_data)
            except Exception as e:
                logger.error(f"Error in processing file: {e}")
                return jsonify({'prediction': 'Error in processing file', 'confidence': 0})
    
    return render_template('index.html', prediction = '', confidence = '')

if __name__ == '__main__':
    app.run(port=5000)
#    app.run(port = 80) # For Azure deployment