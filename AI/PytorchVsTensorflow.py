import pandas as pd
import os
import matplotlib.pyplot as plt

# ================== COMMON SETUP ==================
df = pd.read_csv(r"C:\Users\nanim\Downloads\cats_and_dogs_labels.csv")
df['label'] = df['filename'].apply(lambda x: x.split(os.sep)[-2])
df['label'] = df['label'].map({'cats': 0, 'dogs': 1})

# ------------------ TENSORFLOW ------------------
import tensorflow as tf
from sklearn.model_selection import train_test_split

IMG_SIZE = (150, 150)

train_df, val_df = train_test_split(df, test_size=0.2, stratify=df['label'], random_state=42)

def load_image_tf(path, label):
    img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, IMG_SIZE)
    img = img / 255.0
    return img, label

train_ds = tf.data.Dataset.from_tensor_slices((train_df['filename'].values, train_df['label'].values))
val_ds = tf.data.Dataset.from_tensor_slices((val_df['filename'].values, val_df['label'].values))

train_ds = train_ds.map(load_image_tf).shuffle(1000).batch(32).prefetch(tf.data.AUTOTUNE)
val_ds = val_ds.map(load_image_tf).batch(32).prefetch(tf.data.AUTOTUNE)

model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(150,150,3)),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(train_ds, validation_data=val_ds, epochs=5)

plt.plot(history.history['accuracy'], label='Train Acc')
plt.plot(history.history['val_accuracy'], label='Val Acc')
plt.legend(); plt.title("TensorFlow Accuracy"); plt.show()


# ------------------ PYTORCH ------------------
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim

class CatDogDataset(Dataset):
    def __init__(self, df, transform=None):
        self.df = df.reset_index(drop=True)
        self.transform = transform

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        img_path = self.df.loc[idx, 'filename']
        label = self.df.loc[idx, 'label']
        image = Image.open(img_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        return image, label

transform = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.ToTensor(),
])

train_data = CatDogDataset(train_df, transform)
val_data = CatDogDataset(val_df, transform)

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
val_loader = DataLoader(val_data, batch_size=32)

class CNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, 3), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3), nn.ReLU(), nn.MaxPool2d(2),
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64*36*36, 128), nn.ReLU(),
            nn.Linear(128, 1), nn.Sigmoid()
        )

    def forward(self, x):
        x = self.conv(x)
        return self.fc(x)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_pt = CNN().to(device)
loss_fn = nn.BCELoss()
optimizer = optim.Adam(model_pt.parameters(), lr=0.001)

# Training loop
for epoch in range(5):
    model_pt.train()
    total_loss = 0
    for images, labels in train_loader:
        images, labels = images.to(device), labels.float().unsqueeze(1).to(device)
        preds = model_pt(images)
        loss = loss_fn(preds, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}: Train Loss = {total_loss / len(train_loader):.4f}")
