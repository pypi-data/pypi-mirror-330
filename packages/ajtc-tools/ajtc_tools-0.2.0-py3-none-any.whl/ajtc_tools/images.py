import numpy as np
from PIL import Image, ImageTk
import tkinter as tk

class ArrayImageViewer:
   """
    A class that converts a 2D array into an image and displays it using either a Tkinter window 
    or the default image viewer.

    Attributes:
        root (tk.Tk): The Tkinter root window for displaying images.
        canvas (tk.Canvas): The Tkinter canvas for displaying images within the window.

    Methods:
        array_to_image(data, mode='gradient', color_map=None, show_in_window=False):
            Converts the given 2D array into an image and displays it in either a Tkinter window 
            or the default image viewer.
    """
    def __init__(self):
        """Initialize the ArrayImageViewer with a Tkinter window and canvas."""
        self.root = tk.Tk()
        self.root.title("Array Image Viewer")
        self.canvas = tk.Canvas(self.root, width=500, height=500)
        self.canvas.pack()

    def array_to_image(self, data, mode='gradient', color_map=None, show_in_window=False):
        """
        Converts a 2D array into an image and displays it based on the selected option.
        
        Parameters:
            data (2D array): The array to be converted into an image.
            mode (str): Either 'gradient' or 'lookup'. Determines how colors are applied.
            color_map (dict): A dictionary mapping cell values to specific colors, only used in 'lookup' mode.
            show_in_window (bool): Whether to show the image in a Tkinter window. If False, it uses img.show().
        """
        # Convert the 2D array into a numpy array
        arr = np.array(data)

        # Handle 'gradient' mode
        if mode == 'gradient':
            # Normalize the array to 0-255 for image creation
            min_val, max_val = np.min(arr), np.max(arr)
            gradient = (arr - min_val) / (max_val - min_val) * 255  # Normalize to 0-255
            gradient = gradient.astype(np.uint8)

            # Create a color image
            color_img = np.zeros((arr.shape[0], arr.shape[1], 3), dtype=np.uint8)
            for i in range(arr.shape[0]):
                for j in range(arr.shape[1]):
                    val = gradient[i, j]
                    if val < 128:
                        color_img[i, j] = [255, int(val*2), int(val*2)]  # Color from min (redish)
                    elif val > 128:
                        color_img[i, j] = [int((255-val)*2), int((255-val)*2), 255]  # Color to max (bluish)
                    else:
                        color_img[i, j] = [255, 255, 255]  # Middle is white

        # Handle 'lookup' mode
        elif mode == 'lookup' and color_map:
            color_img = np.zeros((arr.shape[0], arr.shape[1], 3), dtype=np.uint8)
            for i in range(arr.shape[0]):
                for j in range(arr.shape[1]):
                    cell_value = arr[i, j]
                    color_img[i, j] = color_map.get(cell_value, [0, 0, 0])  # Default to black if value not found
        else:
            raise ValueError("Invalid mode or missing color_map for lookup mode.")

        # Create the image object
        img = Image.fromarray(color_img)

        if show_in_window:
            # Convert the image to a format that Tkinter can display
            img_tk = ImageTk.PhotoImage(img)

            # Display the image in the Tkinter canvas
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img_tk)
            self.canvas.image = img_tk  # Keep a reference to avoid garbage collection

            # Start the Tkinter main loop (if it hasn't started already)
            self.root.update_idletasks()  # Update the canvas
            self.root.update()  # Handle any GUI events
        else:
            # Show the image using img.show() (default image viewer)
            img.show()

