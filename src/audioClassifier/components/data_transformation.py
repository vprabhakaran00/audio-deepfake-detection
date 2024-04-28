import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from audioClassifier import logger
from pathlib import Path
from audioClassifier.entity.config_entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
    
    def load_data(self):
        data, labels = self._load_audio_data()
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.2, random_state=42)
        np.save(os.path.join(self.config.root_dir, "X_train.npy"), X_train)
        np.save(os.path.join(self.config.root_dir, "X_test.npy"), X_test)
        np.save(os.path.join(self.config.root_dir, "y_train.npy"), y_train)
        np.save(os.path.join(self.config.root_dir, "y_test.npy"), y_test)
        logger.info("Split data and labels into training and test sets.")
        logger.info(f"Shape of X_train - {X_train.shape}")
        logger.info(f"Shape of X_test - {X_test.shape}")
        logger.info(f"Shape of y_train - {y_train.shape}")
        logger.info(f"Shape of y_test - {y_test.shape}")
        
    def _load_audio_data(self):
        data = []
        labels = []
        folders = os.listdir(self.config.data_path)
        folders.reverse()
        for label, folder in enumerate(folders):
            folder_path = os.path.join(self.config.data_path, folder)
            for filename in os.listdir(folder_path):
                if filename.endswith('.wav') or filename.endswith('.mp3'):
                    filepath = os.path.join(folder_path, filename)
                    try:
                        data.append(self._process_audio(filepath))
                        labels.append(label)
                    except Exception as e:
                        logger.error(f"Error processing audio file: {filepath}, Error: {e}")
                    
        X = np.array(data)
        y = np.array(labels)

        return X, y
        
    def _process_audio(self, filepath: Path ):
        try:
            audio = self._load_and_resample_audio(filepath)
            audio = self._pad_or_truncate_audio(audio)
            spectrogram = self._compute_spectrogram(audio)
            return spectrogram
        except Exception as e:
            logger.error(f"Error processing audio file: {filepath}, Error: {e}")
            raise
        
    def _load_and_resample_audio(self, filepath: Path):
        try:
            audio, _ = librosa.load(filepath, sr = self.config.sampling_rate, mono = True)
            return audio
        except Exception as e:
            logger.error(f"Error loading audio file: {filepath}, Error: {e}")
            raise
        
    def _pad_or_truncate_audio(self, audio):
        audio_length = len(audio)
        desired_length = self.config.max_length
        try:
            if audio_length < desired_length:
                padding = desired_length - audio_length
                audio = np.pad(audio, (0, padding), mode='constant')
            else:
                audio = audio[:desired_length]
            return audio
        except Exception as e:
            logger.error(f"Error padding/truncating audio: {e}")
            raise

    def _compute_spectrogram(self, audio):
        try:
            spectrogram = np.abs(librosa.stft(y = audio, n_fft = self.config.n_fft))
            spectrogram = librosa.amplitude_to_db(spectrogram, ref=np.max)
            return spectrogram
        except Exception as e:
            logger.error(f"Error computing spectrogram: {e}")
            raise
            