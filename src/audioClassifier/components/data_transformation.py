import os
import numpy as np
import librosa
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from audioClassifier import logger
from pathlib import Path
from audioClassifier.entity.config_entity import DataTransformationConfig


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
    
    def load_and_oversample(self):
        data, labels = self._load_audio_data()
        X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size = 0.2, random_state=42, stratify=labels)
        X_train_resampled, y_train_resampled = self._oversample_data(X_train, y_train)
        np.save(os.path.join(self.config.root_dir, "X_train.npy"), X_train_resampled)
        np.save(os.path.join(self.config.root_dir, "X_test.npy"), X_test)
        np.save(os.path.join(self.config.root_dir, "y_train.npy"), y_train_resampled)
        np.save(os.path.join(self.config.root_dir, "y_test.npy"), y_test)
        logger.info("Split data and labels into training and test sets.")
        logger.info(f"Shape of X_train - {X_train_resampled.shape}")
        logger.info(f"Shape of X_test - {X_test.shape}")
        logger.info(f"Shape of y_train - {y_train_resampled.shape}")
        logger.info(f"Shape of y_test - {y_test.shape}")
        
    def _load_audio_data(self):
        spectrograms = []
        labels = []
        audio_files = self._read_audio_filenames(self.config.data_path)
        for file, label in audio_files:
            audio, sr = librosa.load(file, sr=16000)
            segments = self._split_audio_into_segments(audio, sr, segment_length_secs=10)
            for segment in segments:
                spectrogram = self._create_spectrogram(segment, sr, n_fft=self.config.n_fft, hop_length=self.config.hop_length, n_mels=self.config.n_mels)
                augmented_spectrogram = self._augment_data(spectrogram)
                spectrograms.append(augmented_spectrogram)
                labels.append(label)
                    
        X = np.array(spectrograms)
        y = np.array(labels)
        
        X = np.expand_dims(X, axis=-1)
        X = np.repeat(X, 3, axis=-1)

        return X, y
    
    @staticmethod
    def _read_audio_filenames(audio_directory: Path):
        try:
            audio_files = []
            folders = os.listdir(audio_directory)
            folders.reverse()
            for label, folder in enumerate(folders):
                folder_path = os.path.join(audio_directory, folder)
                for filename in os.listdir(folder_path):
                    if filename.endswith('.wav') or filename.endswith('.mp3'):
                        filepath = os.path.join(folder_path, filename)
                        audio_files.append((filepath, label))
            return audio_files
        except Exception as e:
            logger.error(f"Error while reading audio filenames: {e}")
            raise e
    
    @staticmethod
    def _split_audio_into_segments(audio, sr, segment_length_secs):
        try:
            segment_length_samps = segment_length_secs * sr
            num_segments = len(audio) // segment_length_samps
            segments = [audio[i * segment_length_samps:(i + 1) * segment_length_samps] for i in range(num_segments)]
            return segments
        except Exception as e:
            logger.error(f"Error while splitting audio file into segments: {e}")
            raise e
    
    @staticmethod
    def _create_spectrogram(audio, sr, n_fft, hop_length, n_mels):
        try:
            spectrogram = librosa.feature.melspectrogram(y=audio, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
            spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
            return spectrogram
        except Exception as e:
            logger.error(f"Error while creating spectrogram: {e}")
            raise e
    
    @staticmethod
    def _random_crop(spectrogram, crop_size):
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
    
    @staticmethod
    def _time_shift(spectrogram, max_shift):
        try:
            shift_amount = np.random.randint(-max_shift, max_shift)
            shifted_spectrogram = np.roll(spectrogram, shift_amount, axis=1)
            return shifted_spectrogram
        except Exception as e:
            logger.error(f"Error while shifting spectrogram: {e}")
            raise e

    @staticmethod
    def _add_noise(spectrogram, noise_factor):
        try:
            noise = np.random.randn(*spectrogram.shape) * noise_factor
            noisy_spectrogram = spectrogram + noise
            return noisy_spectrogram
        except Exception as e:
            logger.error(f"Error while adding noise to spectrogram: {e}")
            raise e

    def _augment_data(self, spectrogram):
        spectrogram = self._random_crop(spectrogram, crop_size=224)
        spectrogram = self._time_shift(spectrogram, max_shift=10)
        spectrogram = self._add_noise(spectrogram, noise_factor=0.005)
        return spectrogram
    
    @staticmethod
    def _oversample_data(X, y):
        try:
            X_flat = X.reshape((X.shape[0], -1))
            ros = RandomOverSampler(random_state=42)
            X_resampled_flat, y_resampled = ros.fit_resample(X_flat, y)
            X_resampled = X_resampled_flat.reshape((-1, 224, 224, 3))
            unique, counts = np.unique(y_resampled, return_counts=True)
            logger.info(f"Class distribution after resampling: {dict(zip(unique, counts))}")
            return X_resampled, y_resampled
        except Exception as e:
            logger.error(f"Error while oversampling data: {e}")
            raise e