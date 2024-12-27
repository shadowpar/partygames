import tkinter as tk
from tkinter import messagebox
import random
import cv2
import time
from PIL import Image, ImageTk
import pygame
import random, io
from pprint import pprint

globalImageMap = {}

def on_close():
    """Handle the close button event."""
    # Ask the user to choose between two actions
    result = messagebox.askyesnocancel(
        "Exit Program",
        "Do you want to:\n\n"
        "Yes: Close the program\n"
        "No: Calculate the next step\n"
        "Cancel: Stay on this screen"
    )

    if result is True:  # User clicked 'Yes'
        print("Program closed.")
        root.destroy()
    elif result is False:  # User clicked 'No'
        print("Calculate function called.")
        calculate_next_step()  # Call your custom function
    else:  # User clicked 'Cancel' or closed the prompt
        print("Close action canceled. Back to program.")

def calculate_next_step():
    pprint(usedButtons)
    final_winner_id = random.choice(usedButtons)
    #idx = random.randint(0,len(usedButtons))
    #final_winner_id = idx
    print("the winner is {}".format(final_winner_id+1))


    thinkingMessages = ['Hmm','Maybe','Is this the winner?','I don\'t know','I am not sure','Probably...','Unlikely...',
                        'It could be your lucky day','Not your lucky day']
    """Simulate the computer thinking and highlight used buttons."""

    # Create a list of buttons that have been pressed (disabled buttons)
    selected_buttons = [i for i in usedButtons]
    
    # Verify that there are used buttons to highlight
    if not selected_buttons:
        messagebox.showinfo("No Selection", "No buttons have been selected yet.")
        return

    # Keep track of the current index in the list of selected buttons
    current_index = 0
    
    # Number of random "thinking" cycles
    lowerbound = int(round((len(usedButtons)/4)))+1
    upperbound = int(round(len(usedButtons)/2))+1
    num_cycles = random.randint(lowerbound, upperbound)  # Randomly decide how many highlights to show
    #-------------------------
    popup_window = None  # Global reference for the popup window

    def highlight_next_button(count):
        global popup_window
        nonlocal current_index

        # Remove highlight and close popup for the previous button
        if count > 0:
            previous_button = buttons[selected_buttons[current_index]]
            previous_button.config(bg="black", fg=random.choice(text_colors), relief="flat", borderwidth=1)
            if popup_window:  # Close the popup window if it exists
                popup_window.destroy()

        # Move to the next button
        current_index = (current_index + 1) % len(selected_buttons)
        current_button = buttons[selected_buttons[current_index]]

        # Highlight the current button with vibrant yellow and a bold border
        current_button.config(bg="yellow", fg="black", relief="solid", borderwidth=5)

        # Open a popup window to show the image stored in this button
        show_image_popup(current_button)

        # If we haven't reached the final number of cycles, continue highlighting
        if count < num_cycles:
            root.after(1500, lambda: highlight_next_button(count + 1))  # Delay of 150 ms
        else:
            # Stop the "thinking" animation and highlight the final winner button
            stop_on_winner(final_winner_id)
            playerPostWinnerSounds()
#----------show image popup----------------------
    def show_image_popup(button):
        global popup_window
        nonlocal thinkingMessages
        # Check if the button has an image
        if hasattr(button, "image") and button.image:
            # Create a new Toplevel window
            popup_window = tk.Toplevel(root)
            popup_window.title("Preview Image")

            # Set window size
            popup_width = 800
            popup_height = 800
            popup_window.geometry(f"{popup_width}x{popup_height}")
            popup_window.configure(bg="black")
#----------------------adding banner to pop up window----------------------------
            # Create the banner label
            banner = tk.Label(popup_window, 
                            text=random.choice(thinkingMessages), 
                            bg="blue",          # Background color
                            fg="white",         # Text color
                            font=("Helvetica", 20, "bold"),  # Font style and size
                            height=2)           # Height in rows (increases thickness)

            # Place the banner at the top of the window
            banner.pack(side="top", fill="x")  # Fill horizontally across the window

            # # Add other widgets below the banner
            # content_label = tk.Label(popup_window, text="Should I chose this person??", font=("Arial", 40))
            # content_label.pack(pady=20)  # Add some spacing
#-------------------------------------------------------------------------------

            # Retrieve the original image (stored in the button)
            original_image = button.image

            # Resize the image to fit the popup window
            resized_image = original_image._PhotoImage__photo.zoom(4,4)  # Create a copy to manipulate

            # Display the resized image in the popup window
            label = tk.Label(popup_window, image=resized_image, bg="black")
            label.pack(expand=True, fill="both")
            label.image = resized_image  # Keep a reference to prevent garbage collection

            # Ensure the window closes automatically after some time
            popup_window.after(1000, popup_window.destroy)

#----------end of show image popup---------------

    def stop_on_winner(winner_id):
        print("stop on winner received {}".format(winner_id))
        """Highlight the final winner and end the process."""
        # Remove highlights from all previously highlighted buttons
        for button_id in selected_buttons:
            buttons[button_id].config(bg="black", fg=random.choice(text_colors))
        
        # Highlight the winner button
        winner_button = buttons[winner_id]
        # Resize the image with proper resampling (ANTIALIAS is a good choice for high-quality resampling)
        # Get the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # resized_image = button.image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        #resized_image = globalImageMap[button_id+1].resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        resized_image = globalImageMap[winner_id+1].resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        # victorySound.play()
        # time.sleep(victorySound.get_length())
        winningSound.play()
        time.sleep(winningSound.get_length())
        # pygame.mixer.pause()
        # pygame.time.wait(winningSound.get_length())
        # input("check 1")
        popup_window = tk.Toplevel(root)
        # input("check 2")
        popup_window.title("and the Winner is number {}".format(winner_id+1))
        img_tk = ImageTk.PhotoImage(resized_image)
        # Set window size
        popup_width = screen_width
        popup_height = screen_height
        # input("check 3")
        popup_window.geometry(f"{popup_width}x{popup_height}")
        popup_window.configure(bg="black")
        winner_button.config(bg="green", fg="white")
        # input("check 4")
        # Display the resized image in the popup window
        label = tk.Label(popup_window, image=img_tk, bg="black")
        label.pack(expand=True, fill="both")
        # input("check 5")
        label.image = img_tk  # Keep a reference to prevent garbage collection
        popup_window.attributes("-topmost", True)  # Ensure the window is in front
        #------------------------------
    
    def playerPostWinnerSounds():
        def play_crowd_cheering():
            pygame.mixer.music.unload()
            pygame.mixer.music.load("crowdcheering.mp3")
            pygame.mixer.music.play()
        
        def play_congratulations():
            pygame.mixer.music.unload()
            pygame.mixer.music.load("congratulations.mp3")
            pygame.mixer.music.play()
            # Schedule the next sound after the current one finishes
            root.after(int(pygame.mixer.Sound("congratulations.mp3").get_length() * 1000), play_crowd_cheering)
        
        # Start playing the first sound after the window appears
        root.after(500, play_congratulations)  # Adjust the delay as necessary


    # Start the highlighting process
    highlight_next_button(0)



# Function that is called when a button is clicked
def button_pressed(button_id):
    # This function will deactivate the button when pressed
    button = buttons[button_id]
    button.config(state=tk.DISABLED)
    usedButtons.append(button_id)
    # Inform the user of the button pressed
    print(f"Button {button_id + 1} pressed.")
    # messagebox.showinfo("Button Pressed", f"You pressed button {button_id + 1}!")

    # Open the camera preview in a new pop-out window
    open_camera_preview(button_id + 1, button)

# Function to open the camera preview in a pop-out window
def open_camera_preview(button_number, button):
    # Create a new Toplevel window for the camera preview
    preview_window = tk.Toplevel(root)
    preview_window.title(f"Camera Preview for Button {button_number}")

    # Create a label to display the camera preview
    camera_label = tk.Label(preview_window)
    camera_label.pack()

    # Add a label to show the countdown
    countdown_label = tk.Label(preview_window, text="3", font=("Helvetica", 36))
    countdown_label.pack()

    # Start the countdown from 3
    countdown_from_3(preview_window, camera_label, countdown_label, button_number, button)

# Function to countdown from 3, then capture the image
def countdown_from_3(preview_window, camera_label, countdown_label, button_number, button):
    count = 3

    sounds = [sound1,sound2,sound3]
    def playCountSound():
        nonlocal count
        nonlocal sounds
        sounds.pop().play()
        pygame.time.wait(500)
        # engine.say(count+1)
        # # Wait for the speech to finish
        # engine.runAndWait()
        update_countdown()
    def update_countdown():
        nonlocal count
        countdown_label.config(text=str(count))
        count -= 1
        if count >= 0:
            preview_window.after(1000, playCountSound)  # Update every 1 second
        else:
            # After countdown ends, capture the image
            shutterSound.play()
            capture_and_replace_button(button_number, button)
            # Play the MP3 file
            
            preview_window.destroy()  # Close the camera preview window
    
    update_countdown()

    # Start the camera preview in this window
    update_frame(camera_label)


# Function to capture the image and replace the button with the picture
def capture_and_replace_button(button_number, button):
    # Capture the current frame from the camera
    ret, frame = cap.read()
    if ret:
        # Convert the frame to a PIL image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        globalImageMap[button_number] = image
        # Resize image to fit the button
        image = image.copy().resize((button.winfo_width(), button.winfo_height()))

        # Convert the image to a format Tkinter can use (ImageTk.PhotoImage)
        img_tk = ImageTk.PhotoImage(image)

        # Replace the button's text with the image
        button.config(image=img_tk, text="")
        button.image = img_tk  # Keep a reference to the image

        print(f"Image saved for button {button_number}.")
    else:
        print("Failed to capture image")

# Function to update the camera preview in the Tkinter window
def update_frame(camera_label):
    ret, frame = cap.read()
    if ret:
        # Convert the frame to an ImageTk object for Tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Update the label with the new image
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)

    # Continue the frame update
    camera_label.after(10, lambda: update_frame(camera_label))


# Initialize pygame mixer
pygame.mixer.init()
# victorySound = pygame.mixer.Sound("baseballVictory.mp3")
winningSound = pygame.mixer.Sound("winsound2.mp3")
# crowdcheering = pygame.mixer.Sound("crowdcheering.mp3")
# congratulations = pygame.mixer.Sound("congratulations.mp3")
sound3 = pygame.mixer.Sound("3.wav")
sound2 = pygame.mixer.Sound("2.wav")
sound1 = pygame.mixer.Sound("1.wav")
shutterSound = pygame.mixer.Sound("camera-shutter.wav")
usedButtons = []


# Create the main Tkinter window
root = tk.Tk()
root.title("Button Grid with Camera")

# Maximize the window
root.state('zoomed')  # This will maximize the window on startup

# Get the window width and height after maximizing
window_width = root.winfo_screenwidth()
window_height = root.winfo_screenheight()

# Define the number of rows and columns for buttons
rows = 10  # Number of rows
cols = 10  # Number of columns (limit to 100 buttons)

# Calculate the button width and height based on screen size and grid size
button_width = window_width // cols
button_height = window_height // rows

# Store button references in a list for easy access
buttons = []

# Define a list of colors for the text
text_colors = ["green", "blue", "orange", "red", "white"]

# Create a grid of 100 buttons (10 rows x 10 columns)
for i in range(100):
    row = i // cols  # Determine the row position
    col = i % cols   # Determine the column position

    # Choose a random text color from the list
    text_color = random.choice(text_colors)

    # Create the button with a random text color and black background
    button = tk.Button(root, text=str(i + 1), width=button_width, height=button_height, 
                       command=lambda i=i: button_pressed(i), fg=text_color, bg="black", font=("Helvetica", 48))
    button.grid(row=row, column=col, padx=1, pady=1, sticky="nsew")

    # Store the button to easily access and deactivate it later
    buttons.append(button)

# Configure grid to resize the buttons when the window is resized
for r in range(rows):
    root.grid_rowconfigure(r, weight=1, uniform="equal")
for c in range(cols):
    root.grid_columnconfigure(c, weight=1, uniform="equal")

# Try opening the front camera (secondary camera)
cap = cv2.VideoCapture(1)  # Try 1 for the front camera, 0 is for the default (rear) camera

# Check if the camera is opened correctly
if not cap.isOpened():
    print("Error: Camera not found!")
    exit()



# Override the close button
root.protocol("WM_DELETE_WINDOW", on_close)

# Run the Tkinter event loop
root.mainloop()

# Release the camera when done
cap.release()
cv2.destroyAllWindows()
