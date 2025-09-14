import pandas as pd
import numpy as np
import os
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf


class HAM10000DataLoader:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.metadata = None
        self.label_encoder = LabelEncoder()
        self.class_names = []

    def load_metadata(self):
        """Load the HAM10000 metadata CSV file"""
        metadata_path = os.path.join(self.data_dir, 'HAM10000_metadata.csv')

        if not os.path.exists(metadata_path):
            print(f"❌ Dataset not found at {metadata_path}")
            return None

        self.metadata = pd.read_csv(metadata_path)

        print(f"📊 Dataset loaded: {len(self.metadata)} images")
        print(f"📋 Classes distribution:")
        print(self.metadata['dx'].value_counts())

        # Encode labels
        self.metadata['label'] = self.label_encoder.fit_transform(self.metadata['dx'])
        self.class_names = self.label_encoder.classes_.tolist()

        return self.metadata

    def load_image(self, image_id, img_size=(224, 224)):
        """Load and preprocess a single image"""
        # Try both image folders
        img_path1 = os.path.join(self.data_dir, 'HAM10000_images_part_1', f'{image_id}.jpg')
        img_path2 = os.path.join(self.data_dir, 'HAM10000_images_part_2', f'{image_id}.jpg')

        img_path = img_path1 if os.path.exists(img_path1) else img_path2

        if os.path.exists(img_path):
            try:
                image = Image.open(img_path).convert('RGB')
                image = image.resize(img_size)
                return np.array(image) / 255.0
            except Exception as e:
                print(f"❌ Error loading image {image_id}: {e}")
                return None
        else:
            return None

    def create_balanced_dataset(self, max_per_class=200, img_size=(224, 224)):
        """Create a balanced dataset with limited samples per class"""
        if self.metadata is None:
            self.load_metadata()

        if self.metadata is None:
            return None, None

        # Sample balanced data
        balanced_data = []
        for class_name in self.metadata['dx'].unique():
            class_data = self.metadata[self.metadata['dx'] == class_name]
            sample_size = min(max_per_class, len(class_data))
            sampled = class_data.sample(n=sample_size, random_state=42)
            balanced_data.append(sampled)

        balanced_df = pd.concat(balanced_data, ignore_index=True)

        print(f"🎯 Creating balanced dataset with {len(balanced_df)} images...")
        print("📊 Class distribution:")
        print(balanced_df['dx'].value_counts())

        images = []
        labels = []
        failed_loads = 0

        for idx, row in balanced_df.iterrows():
            image = self.load_image(row['image_id'], img_size)
            if image is not None:
                images.append(image)
                labels.append(row['label'])

                if len(images) % 50 == 0:
                    print(f"✅ Loaded {len(images)} images...")
            else:
                failed_loads += 1

        if failed_loads > 0:
            print(f"⚠️ Failed to load {failed_loads} images")

        images = np.array(images)
        labels = np.array(labels)

        print(f"🎉 Dataset created: {images.shape}")
        return images, labels
