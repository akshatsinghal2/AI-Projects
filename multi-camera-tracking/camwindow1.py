import tkinter as tk
from PIL import Image, ImageTk
import os
import cv2
from ultralytics import YOLO
import time
import threading
import imutils


class CamWindow1:
    def __init__(self, stream_link, device):
        self.stream_link = stream_link
        self.device = device
        
        self.window = tk.Toplevel()
        self.window.title("Camera Stream")
        
        # OpenCV video capture with custom output size
        self.cap = cv2.VideoCapture(self.stream_link)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set width to 640 pixels
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set height to 480 pixels
        self.streaming = False  # Flag to indicate streaming state
        
        # Canvas to display video stream
        self.canvas = tk.Canvas(self.window, width=640, height=480)  # Set canvas size accordingly
        self.canvas.pack()
        
        # Frame to contain buttons
        self.button_frame = tk.Frame(self.window)
        self.button_frame.pack(pady=5)
        
        # Start button
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_stream, bg="green")
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_button = tk.Button(self.button_frame, text="Stop", command=self.stop_stream, bg="blue", state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # Capture button
        self.capture_button = tk.Button(self.button_frame, text="Capture", command=self.capture_frame, bg="cyan")
        self.capture_button.pack(side=tk.LEFT, padx=5)

        # Bind the "c" key to the capture_frame method
        self.window.bind("c", self.capture_frame_on_event)
        
        # Detect button
        self.detect_button = tk.Button(self.button_frame, text="Detect", command=self.detect_objects, bg="yellow")
        self.detect_button.pack(side=tk.LEFT, padx=5)
        
        # Close button
        self.close_button = tk.Button(self.button_frame, text="Close", command=self.close, bg="red")
        self.close_button.pack(side=tk.LEFT, padx=5)
        
        # Counter for naming captured frames
        self.frame_counter = 0
        
        # Automatically start streaming when the window is initialized
        self.start_stream()
        
        self.update()


    def update(self):
        if self.streaming:
            ret, frame = self.cap.read()
            if ret:
                # Resize frame if needed
                frame = cv2.resize(frame, (640, 480))
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.window.after(10, self.update)


    def start_stream(self):
        self.streaming = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)


    def stop_stream(self):
        self.streaming = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)


    def capture_frame(self):
        ret, frame = self.cap.read()
        if ret:
            folder_path = "captured_frames"
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            filename = os.path.join(folder_path, f"frame_{self.frame_counter}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Frame captured and saved as {filename}")
            self.frame_counter += 1

            # Resize frame to fit the size of the window
            resized_frame = cv2.resize(frame, (640, 480))

            # Display captured frame in a new window
            captured_window = tk.Toplevel()
            captured_window.title(f"Captured Frame {self.frame_counter}")

            # Calculate the position to center the frame
            x = (captured_window.winfo_screenwidth() - 640) // 2
            y = (captured_window.winfo_screenheight() - 480) // 2

            # Set the window size and position
            captured_window.geometry(f"640x480+{x}+{y}")

            captured_canvas = tk.Canvas(captured_window, width=640, height=480)
            captured_canvas.pack()

            # Convert the resized frame to an ImageTk object
            captured_photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)))
            captured_canvas.create_image(0, 0, image=captured_photo, anchor=tk.NW)

            # Keep a reference to the PhotoImage object to prevent it from being garbage collected
            captured_canvas.image = captured_photo

            captured_window.mainloop()
        else:
            print("Error capturing frame")


    def detect_objects(self):
    # Add code here to detect objects using YOLO model
        cap = cv2.VideoCapture(self.stream_link)

        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        output_video = 'output/output_video1.mp4'
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change the codec as needed
        output = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

        delay_time = 1000  # Adjust this value as needed
        time.sleep(delay_time / 1000)
        
        def run_detection():
            model = YOLO('yolov8n.pt')
            start_time = time.time()
            duration = 10
            while(time.time() - start_time) < duration:
                
                ret, frame = cap.read()
                frame = imutils.resize(frame, width=700, height=600)
                if not ret:
                    print("Error reading frame from the live stream")
                    break

                # Display the frame or perform any desired operations
                if ret:
                    # Display the frame
                    # cv2.imshow('Video', frame)
                    # Detect objects
                    results = model.track(frame, show = True, persist=True, classes=[0], save_crop=True, tracker="bytetrack.yaml", project = 'output/predict', name="infer", exist_ok=True, conf = 0.8, device = self.device)

                    # Wait for 25 milliseconds. If 'q' is pressed, exit the loop
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break   
                else:
                    break

        # Start object detection in a separate thread
        self.detect_thread = threading.Thread(target=run_detection)
        self.detect_thread.start()


    def close(self):
        self.window.destroy()
        self.cap.release()


    def capture_frame_on_event(self, event):
        # Call the capture_frame method when the event occurs
        self.capture_frame()