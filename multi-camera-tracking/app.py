import tkinter as tk
import threading
import torch
from camwindow1 import CamWindow1
from camwindow2 import CamWindow2
from camwindow3 import CamWindow3  


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)

        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
        # URLs for cameras
        self.cam1_url = 'rtsp://admin:admin12345@192.168.1.223:554/Streaming/channels/301'
        self.cam2_url = 'rtsp://admin:admin12345@192.168.1.223:554/Streaming/channels/401'
        self.cam3_url = 'rtsp://admin:admin12345@192.168.1.223:554/Streaming/channels/1001'  # Add URL for cam3
        
        # Frame to contain buttons
        self.button_frame = tk.Frame(window)
        self.button_frame.pack(pady=5)
        
        # Cam1 button
        self.cam1_button = tk.Button(self.button_frame, text="Cam1", command=self.open_cam1, bg="green")
        self.cam1_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Cam2 button
        self.cam2_button = tk.Button(self.button_frame, text="Cam2", command=self.open_cam2, bg="green")
        self.cam2_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Cam3 button
        self.cam3_button = tk.Button(self.button_frame, text="Cam3", command=self.open_cam3, bg="green")
        self.cam3_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Close button
        self.close_button = tk.Button(self.button_frame, text="Close All", command=self.close_all, bg="red")
        self.close_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # List to store references to opened camera windows
        self.cam_windows = []
        
    def open_cam1(self):
        # Create a new thread for opening cam1
        cam1_thread = threading.Thread(target=self.open_cam1_thread)
        cam1_thread.start()

    def open_cam1_thread(self):
        cam1_window = CamWindow1(self.cam1_url, self.device)
        self.cam_windows.append(cam1_window)

    def open_cam2(self):
        # Create a new thread for opening cam2
        cam2_thread = threading.Thread(target=self.open_cam2_thread)
        cam2_thread.start()

    def open_cam2_thread(self):
        cam2_window = CamWindow2(self.cam2_url, self.device)
        self.cam_windows.append(cam2_window)

    def open_cam3(self):
        # Create a new thread for opening cam3
        cam3_thread = threading.Thread(target=self.open_cam3_thread)
        cam3_thread.start()

    def open_cam3_thread(self):
        cam3_window = CamWindow3(self.cam3_url, self.device)
        self.cam_windows.append(cam3_window)
    
    def close_all(self):
        # Close all camera windows
        for cam_window in self.cam_windows:
            cam_window.close()
        
        # Close the main window
        self.window.destroy()
    

if __name__ == '__main__':
    # Create the main application window
    root = tk.Tk()
    root.geometry('330x60')  # Adjusted width to accommodate the new button
    app = App(root, "Main Window")
    root.mainloop()
