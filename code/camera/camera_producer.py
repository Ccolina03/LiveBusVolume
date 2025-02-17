"""Way to capture frames from a webcam or camera, compress them, and send them to a Kafka topic."""

import cv2
import lzma
import pickle
import time
import random
import uuid
import argparse
import json
import numpy as np
import datetime

import client

config:dict = client.read_config()


def capture(produce: bool, debug: bool, frame_count: int = -1) -> None:
    """Capture frames from a webcam, compress them, and send them to a Kafka topic."""

    cap = cv2.VideoCapture(0)
    count:int = 0

    if not cap.isOpened():
        raise IOError("Error: Could not open webcam.")

    print("Starting webcam feed... Press 'ctrl-c' to exit.")

    try:
        while True:
            # Only capture a certain number of frames if frame_count is set
            if frame_count >= 0:
                if count == frame_count:
                    break
                count += 1

            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                continue

            height, width, _ = frame.shape
            bottom_left_corner = frame[height-512:height, 0:512]

            ret, jpg_buffer = cv2.imencode('.jpg', bottom_left_corner, [cv2.IMWRITE_JPEG_QUALITY, 90])
            if not ret:
                print("JPEG encoding failed.")
                continue
            
            compressed_bytes = lzma.compress(jpg_buffer.tobytes())
            decompressed_bytes = lzma.decompress(compressed_bytes)
            nparr = np.frombuffer(decompressed_bytes, dtype=np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            cv2.imwrite("output.jpg", img)
            cv2.imwrite("frame.jpg", frame)

            if produce:
                timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='microseconds')
                message = {
                    'timestamp': timestamp,
                    'frame': str(compressed_bytes),
                    'bus_id': str(uuid.uuid4().int),
                    'route_id': random.randint(1, 114)
                }

                # serialized_message = pickle.dumps(message, protocol=pickle.HIGHEST_PROTOCOL) #serialize with pickle

                client.produce("camera-raw", config, json.dumps(message).encode("utf-8")) #send to kafka

            if debug: 
                print(f"JPEG size: {len(jpg_buffer)} bytes, Compressed size: {len(compressed_bytes)} bytes at timestamp {datetime.datetime.now().isoformat(timespec='microseconds')}")
            
            time.sleep(0.95)

    except KeyboardInterrupt:
        print("Interrupted by user.")

    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Resources released and producer flushed.")


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Capture webcam feed and send frames to Kafka.")
    #add argument for produce, which enables the capture function to produce to kafka
    parser.add_argument('--produce', action='store_true', help="Produce frames to Kafka.")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode.")
    parser.add_argument('--frame_count', type=int, default=-1, help="Number of frames to capture.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print("Starting producer...", args)
    capture(args.produce, args.debug, args.frame_count)

if __name__ == "__main__":
    main()
