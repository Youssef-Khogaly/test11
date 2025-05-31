import cv2
import torch
import os
from pathlib import Path

# Set device
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

def detect_vehicles(image_path, output_dir='outputs'):
    """
    Process an image to detect vehicles and measure their widths
    
    Args:
        image_path (str): Path to input image
        output_dir (str): Directory to save results
    
    Returns:
        tuple: (output_image_path, vehicle_data)
    """
    os.makedirs(output_dir, exist_ok=True)
    
    img = cv2.imread(str(image_path))
    if img is None:
        raise FileNotFoundError(f"Could not read image at {image_path}")
    
    results = model(img)
    prediction = results.pred[0]
    class_tensor = torch.tensor([2, 3, 5, 7], device=prediction.device)
    vehicles = prediction[torch.isin(prediction[:, -1], class_tensor)]
    
    vehicle_data = []
    for *box, conf, cls in vehicles:
        x1, y1, x2, y2 = map(int, box)
        width_px = x2 - x1
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{model.names[int(cls)]} {width_px}px"
        cv2.putText(img, label, (x1, y1 - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        vehicle_data.append({
            'type': model.names[int(cls)],
            'width_px': width_px,
            'confidence': float(conf)
        })
    
    output_path = os.path.join(output_dir, f"detected_{os.path.basename(image_path)}")
    cv2.imwrite(output_path, img)
    return output_path, vehicle_data

if __name__ == "__main__":
    input_dir = Path("/home/khogaly/graduation/vehicle_detector/images/")
    output_dir = "/home/khogaly/graduation/vehicle_detector/output/"

    image_extensions = ('.jpg', '.jpeg', '.png', '.bmp')

    image_files = [p for p in input_dir.glob('*') if p.suffix.lower() in image_extensions]

    if not image_files:
        print("No image files found in the input directory.")
    else:
        for image_path in image_files:
            try:
                output_img, vehicles = detect_vehicles(image_path, output_dir)
                print(f"\nProcessed: {image_path.name}")
                print(f"Results saved to: {output_img}")
                print("Detected Vehicles:")
                for i, vehicle in enumerate(vehicles, 1):
                    print(f"{i}. {vehicle['type']}: Width = {vehicle['width_px']}px (Confidence: {vehicle['confidence']:.2f})")
            except Exception as e:
                print(f"Error processing {image_path.name}: {e}")
