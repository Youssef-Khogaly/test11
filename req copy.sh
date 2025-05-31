#!/bin/bash

set -e

echo "🔧 Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "📦 Installing Python3, pip, git, and build dependencies..."
sudo apt install -y python3 python3-pip git build-essential cmake pkg-config \
    libjpeg-dev libtiff-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev \
    libv4l-dev libxvidcore-dev libx264-dev libgtk-3-dev libatlas-base-dev gfortran \
    python3-dev pigpio python3-pigpio

echo "🐍 Upgrading pip..."
pip3 install --upgrade pip

echo "🐍 Installing Python packages: numpy, opencv-python, matplotlib, torch, torchvision, torchaudio..."
pip3 install numpy opencv-python matplotlib torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

echo "⬇️ Cloning YOLOv5 repository..."
if [ ! -d "yolov5" ]; then
  git clone https://github.com/ultralytics/yolov5.git
fi

cd yolov5

echo "📦 Installing YOLOv5 Python requirements..."
pip3 install -r requirements.txt

echo "✅ Installation complete! YOLOv5 and dependencies are ready."

echo "👉 To start detection, run:"
echo "cd yolov5 && python3 detect.py --source data/images/bus.jpg"

echo "🐷 Starting pigpio daemon (required for pigpio library)..."
sudo systemctl enable pigpiod
sudo systemctl start pigpiod

echo "🐷 pigpio daemon started."
