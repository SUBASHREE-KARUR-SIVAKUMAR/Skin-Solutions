import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import os
import streamlit as st
from data_loader import HAM10000DataLoader
from sklearn.model_selection import train_test_split


class SkinLesionModel:
    def __init__(self, data_dir=None, use_real_data=True):
        self.model = None
        self.class_names = []
        self.data_loader = None

        if use_real_data and data_dir and os.path.exists(os.path.join(data_dir, 'HAM10000_metadata.csv')):
            print("🎯 Using real HAM10000 dataset!")
            self.data_loader = HAM10000DataLoader(data_dir)
            self.train_with_real_data()
        else:
            print("⚠️ HAM10000 dataset not found, using transfer learning demo")
            self.load_demo_model()

    def create_model(self, num_classes):
        """Create model with transfer learning"""
        # Use MobileNetV2 as base
        base_model = tf.keras.applications.MobileNetV2(
            input_shape=(224, 224, 3),
            include_top=False,
            weights='imagenet'
        )

        # Freeze base model initially
        base_model.trainable = False

        model = tf.keras.Sequential([
            base_model,
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(num_classes, activation='softmax')
        ])

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        return model

    def train_with_real_data(self):
        """Train model on real HAM10000 data"""
        print("🚀 Starting training with real HAM10000 data...")

        # Load balanced dataset (smaller for demo)
        images, labels = self.data_loader.create_balanced_dataset(max_per_class=100)

        if images is None:
            print("❌ Failed to load dataset, falling back to demo mode")
            self.load_demo_model()
            return

        self.class_names = self.data_loader.class_names

        # Split data
        X_train, X_val, y_train, y_val = train_test_split(
            images, labels, test_size=0.2, random_state=42, stratify=labels
        )

        # Convert to categorical
        num_classes = len(self.class_names)
        y_train_cat = keras.utils.to_categorical(y_train, num_classes)
        y_val_cat = keras.utils.to_categorical(y_val, num_classes)

        # Create and train model
        self.model = self.create_model(num_classes)

        print("🏋️ Training model...")
        history = self.model.fit(
            X_train, y_train_cat,
            validation_data=(X_val, y_val_cat),
            epochs=5,  # Keep it reasonable for demo
            batch_size=16,
            verbose=1
        )

        # Save model
        self.model.save('ham10000_trained_model.h5')
        print("💾 Model saved!")

        # Save class names
        import pickle
        with open('class_names.pkl', 'wb') as f:
            pickle.dump(self.class_names, f)

        return history

    def load_demo_model(self):
        """Load demo model if real data not available"""
        # Try to load saved model first
        if os.path.exists('ham10000_trained_model.h5'):
            try:
                self.model = keras.models.load_model('ham10000_trained_model.h5')

                # Load class names
                import pickle
                with open('class_names.pkl', 'rb') as f:
                    self.class_names = pickle.load(f)

                print("✅ Loaded saved HAM10000 model!")
                return
            except:
                pass

        # Create demo model
        self.class_names = ['akiec', 'bcc', 'bkl', 'df', 'mel', 'nv', 'vasc']
        self.model = self.create_model(len(self.class_names))
        print("📝 Created demo model")

    def preprocess_image(self, image):
        """Preprocess image for prediction"""
        image = image.resize((224, 224))
        img_array = np.array(image).astype('float32') / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        return img_array

    def predict(self, image):
        """Make prediction"""
        try:
            processed_image = self.preprocess_image(image)
            predictions = self.model.predict(processed_image, verbose=0)

            result = {}
            for i, class_name in enumerate(self.class_names):
                result[class_name] = float(predictions[0][i])

            return result

        except Exception as e:
            print(f"❌ Error: {e}")
            # Return dummy predictions
            return {class_name: 1.0 / len(self.class_names) for class_name in self.class_names}
