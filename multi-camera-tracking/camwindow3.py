import tkinter as tk
from PIL import Image, ImageTk
import os
import cv2
from ultralytics import YOLO
import time
import threading
import imutils
from skimage.metrics import structural_similarity as ssim

class CamWindow3:
    def __init__(self, stream_link, device):
        self.stream_link = stream_link
        self.photo_images = []
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

        # Table button
        self.table_button = tk.Button(self.button_frame, text="Table", command=self.open_table, bg="pink")
        self.table_button.pack(side=tk.LEFT, padx=10, pady=10)  # Add padx and pady
        
        # Compare button
        self.compare_button = tk.Button(self.button_frame, text="Compare Images", command=self.compare_images, bg="purple")
        self.compare_button.pack(side=tk.LEFT, padx=10, pady=10)  # Add padx and pady
        
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
                    results = model.track(frame, show = True, persist=True, classes=[0], save_crop=True, tracker="bytetrack.yaml", project = 'output/predict3', name="infer", exist_ok=True, conf = 0.8, device = self.device)

                    # Wait for 25 milliseconds. If 'q' is pressed, exit the loop
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break   
                else:
                    break

        # Start object detection in a separate thread
        self.detect_thread = threading.Thread(target=run_detection)
        self.detect_thread.start()

        # Disable the detect button while detection is running
        self.detect_button.config(state=tk.NORMAL)
        # self.stop_detect_button.config(state=tk.NORMAL)


    def compare_images(self):
        try:
        # Define the folders to compare
            folder1 = "output/predict/infer/crops/person"
            folder2 = "output/predict3/infer/crops/person"
        except Exception as error:
            print(error)

        # Call the function to compare images
        self.image_comparison(folder1, folder2)       


    def image_comparison(self, folder1, folder2):
        try: 
            output_folder="output/similar_images"
            target_shape = (480,640)
            similarity_threshold = 0.5
        except Exception as error:
            print (error)

        self.compare_image(folder1, folder2, target_shape, similarity_threshold, output_folder)
        self.convert_jpg_to_png(output_folder)


    def compare_image(self, folder1, folder2, target_shape=(480,640), similarity_threshold=0.9, output_folder="similar_images"):
    # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        saved_images = set()  # To keep track of saved images
        try:
            images1 = os.listdir(folder1)
            images2 = os.listdir(folder2)
        except Exception as error:
            print(error)

        for img1_name in images1:
            for img2_name in images2:
                try:
                    img1_path = os.path.join(folder1, img1_name)
                    img2_path = os.path.join(folder2, img2_name)
                except Exception as error:
                    print(error)

                # Read images
                try:
                    img1 = cv2.imread(img1_path)
                    img2 = cv2.imread(img2_path)
                except Exception as error:
                    print(error)

                # Check if images were successfully loaded
                if img1 is None or img2 is None:
                    print(f"Error: Unable to read images '{img1_name}' or '{img2_name}'")
                    continue

                # Resize images if target shape is provided
                if target_shape is not None:
                    img1 = cv2.resize(img1, target_shape)
                    img2 = cv2.resize(img2, target_shape)

                # Compare images using Structural Similarity Index (SSIM)
                gray_img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
                gray_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                similarity_index = ssim(gray_img1, gray_img2)

                # If SSIM is greater than the threshold and image hasn't been saved, save it
                if similarity_index > similarity_threshold and img1_name not in saved_images:
                    output_path = os.path.join(output_folder, img1_name)
                    cv2.imwrite(output_path, img1)
                    saved_images.add(img1_name)  # Add image to saved images set
                    print(f"Saved Similar Image '{img1_name}' to '{output_folder}' (SSIM: {similarity_index})")


    def convert_jpg_to_png(self, output_folder):
        # Iterate through each file in the folder
        for filename in os.listdir(output_folder):
            if filename.endswith(".jpg"):
                # Open the JPG file
                with Image.open(os.path.join(output_folder, filename)) as img:
                    text_before = "cam3"
                    # Convert the image to PNG format
                    png_filename = text_before + os.path.splitext(filename)[0] + ".png"
                    # Save the converted image to the same folder
                    img.save(os.path.join(output_folder, png_filename), "PNG")
                    print(f"{filename} converted to {png_filename}")
                    # Remove the original JPG file
                    os.remove(os.path.join(output_folder, filename))
        

    def open_table(self):
        # Create a new window for displaying the images
        table_window = tk.Toplevel()
        table_window.title("Table of Images")

        # Create a scrollable frame inside the window
        scrollable_frame = tk.Frame(table_window)
        scrollable_frame.pack(fill="both", expand=True)

        # Create a vertical scrollbar
        scrollbar = tk.Scrollbar(scrollable_frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Create a canvas to contain the images and attach the scrollbar
        canvas = tk.Canvas(scrollable_frame, yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=canvas.yview)

        # Create another frame inside the canvas to hold the images
        image_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=image_frame, anchor="nw")

        # Function to update the canvas scroll region
        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        image_frame.bind("<Configure>", on_frame_configure)

        # Get the list of images in the folder
        folder_path = "output/similar_images"  # Change this to your folder path
        images = os.listdir(folder_path)

        # Display each image in the frame
        for img_name in images:
            img_path = os.path.join(folder_path, img_name)
            img = Image.open(img_path)
            img.thumbnail((200, 200))  # Resize the image if needed
            photo = ImageTk.PhotoImage(img)

            # Create a label to display the image
            img_label = tk.Label(image_frame, image=photo)
            img_label.image = photo  # Keep a reference to prevent garbage collection
            img_label.pack(pady=5)

        # Update the canvas to show the images
        canvas.update_idletasks()


        # Function to destroy the window and release resources when closed
        def close_window():
            table_window.destroy()

        # Create a close button
        close_button = tk.Button(table_window, text="Close", command=close_window, bg = 'red')
        close_button.pack(pady=10)


    def stop_detect(self):
        if self.detect_objects:
            # Terminate the detection process
            self.detect_objects.terminate()
            self.detect_button.config(state=tk.NORMAL)
            self.stop_detect_button.config(state=tk.DISABLED)


    def close(self):
        self.window.destroy()
        self.cap.release()


    def capture_frame_on_event(self, event):
        # Call the capture_frame method when the event occurs
        self.capture_frame()