import tkinter as tk
import math
import time
from random import randint
import pygame

class WheelOfFortune:
    def __init__(self, root, prizes):# Initialize pygame mixer
        pygame.mixer.init()
        self.sounds = {'tink':pygame.mixer.Sound("shorttink.wav"),
                       'wheelSpin':None}
        self.root = root
        self.prizes = prizes
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.pinlocations = []
        self.drawFlagPointPos = (0,0)

        self.set_dimensions()  # Set initial dimensions based on window size
        self.segments = len(prizes)
        self.angle_per_segment = 360 / self.segments
        self.current_angle = 0

        self.deceleration = 0.05
        self.speed = 0

        self.start_time = 0
        self.end_time = 0
        self.start_angle = 0

        self.canvas.bind("<ButtonPress-1>", self.start_spin)
        self.canvas.bind("<B1-Motion>", self.record_spin)
        self.canvas.bind("<ButtonRelease-1>", self.release_spin)

        self.root.bind("<Configure>", self.on_resize)  # Bind resizing event to scale elements
        self.draw_wheel()

    def set_dimensions(self):
        # Set the dimensions of the wheel based on the window size
        self.window_width = self.root.winfo_width()
        self.window_height = self.root.winfo_height()
        self.radius = min(self.window_width, self.window_height) // 3  # Dynamic radius
        self.center = (self.window_width // 2, self.window_height // 2)

    def on_resize(self, event):
        # Update the wheel's dimensions when the window is resized
        self.set_dimensions()
        self.draw_wheel()

    def draw_wheel(self):
        self.canvas.delete("all")
        for i, prize in enumerate(self.prizes):
            start_angle = i * self.angle_per_segment
            end_angle = (i + 1) * self.angle_per_segment
            color = "#%06x" % randint(0, 0xFFFFFF)

            self.canvas.create_arc(
                self.center[0] - self.radius,
                self.center[1] - self.radius,
                self.center[0] + self.radius,
                self.center[1] + self.radius,
                start=start_angle + self.current_angle,
                extent=self.angle_per_segment,
                fill=color,
                outline="black",
            )

            mid_angle = math.radians(start_angle + self.angle_per_segment / 2 + self.current_angle)
            x = self.center[0] + math.cos(mid_angle) * self.radius * 0.6
            y = self.center[1] - math.sin(mid_angle) * self.radius * 0.6

            # Rotate the text to follow the radius
            angle_text = start_angle + self.angle_per_segment / 2 + self.current_angle
            self.canvas.create_text(x, y, text=prize, font=("Arial", 10, "bold"), fill="black", angle=angle_text)

        self.canvas.create_oval(
            self.center[0] - 20,
            self.center[1] - 20,
            self.center[0] + 20,
            self.center[1] + 20,
            fill="black",
        )

        self.draw_flag()  # Draw the flag
        self.draw_pins()  # Draw the pins

    def start_spin(self, event):
        self.start_time = time.time()
        self.start_angle = math.atan2(event.y - self.center[1], event.x - self.center[0])

    def record_spin(self, event):
        current_angle = math.atan2(event.y - self.center[1], event.x - self.center[0])
        self.speed = (current_angle - self.start_angle) * (180 / math.pi)  # Angular speed
        self.start_angle = current_angle
        self.start_time = time.time()

    def release_spin(self, event):
        self.end_time = time.time()
        self.spin_wheel()
    
    def findClosestPin(self):
        # Find the coordinate with the highest y value
        max_y_coordinate = max(self.pinlocations, key=lambda coord: coord[1])
        return max_y_coordinate

    def spin_wheel(self):
        if abs(self.speed) < 0.1:
            self.speed = randint(10, 20)  # Ensure minimum spin
        print("speed is {}".format(self.speed))
        self.deceleration = abs(self.speed/225)

        while abs(self.speed) > 0:
            self.current_angle = (self.current_angle + self.speed) % 360
            deltaX = abs(self.drawFlagPointPos[0] - self.findClosestPin()[0])
            print(deltaX)
            if deltaX < 5:
                self.sounds['tink'].play()
            if abs(self.speed) > abs(self.deceleration):
                if self.speed < 0:
                    self.speed += self.deceleration
                else:
                    self.speed -= self.deceleration
            elif deltaX < 5:
                if self.speed < 0:
                    self.speed -= self.deceleration/2
                else:
                    self.speed += self.deceleration/2
            else:
                self.speed = 0
            self.draw_wheel()
            self.root.update()
            # print(self.speed)
            time.sleep(0.01)

        self.determine_winner()

    def determine_winner(self):
        normalized_angle = self.current_angle % 360
        selected_index = int(normalized_angle / self.angle_per_segment)
        selected_prize = self.prizes[selected_index]

    def draw_flag(self):
        flag_base_x = self.center[0]
        flag_base_y = self.center[1] - self.radius - 10  # Keep this position the same
        flag_width = 20
        flag_height = 30

        self.canvas.create_polygon(
            flag_base_x, flag_base_y,
            flag_base_x - flag_width // 2, flag_base_y - flag_height,  # Inverted Y-coordinate
            flag_base_x + flag_width // 2, flag_base_y - flag_height,  # Inverted Y-coordinate
            fill="red",
            outline="black"
        )
        self.drawFlagPointPos = (flag_base_x, flag_base_y)

    def draw_pins(self):
        self.pinlocations.clear()
        pin_radius = 10  # Size of the pins
        pin_distance = self.radius + 10  # Place just outside the wheel

        for i in range(self.segments):
            angle = math.radians(i * self.angle_per_segment + self.current_angle)
            pin_x = self.center[0] + math.cos(angle) * pin_distance
            pin_y = self.center[1] - math.sin(angle) * pin_distance
            self.pinlocations.append((pin_x, pin_y))

            # Draw the pin (circle)
            self.canvas.create_oval(
                pin_x - pin_radius, pin_y - pin_radius,
                pin_x + pin_radius, pin_y + pin_radius,
                fill="blue",
                outline="black"
            )

            # Draw the black vertical line through the pin circle
            line_start_x = self.center[0] + math.cos(angle) * (pin_distance - pin_radius)
            line_start_y = self.center[1] - math.sin(angle) * (pin_distance - pin_radius)
            line_end_x = self.center[0] + math.cos(angle) * (pin_distance + pin_radius)
            line_end_y = self.center[1] - math.sin(angle) * (pin_distance + pin_radius)

            self.canvas.create_line(
                line_start_x, line_start_y,
                line_end_x, line_end_y,
                fill="black",
                width=2
            )


if __name__ == "__main__":

    prizes = ["20 PHP","50 PHP","20 PHP","50 PHP","100 PHP","20 PHP","50 PHP","20 PHP","50 PHP","100 PHP"]

    root = tk.Tk()
    root.title("Wheel of Fortune")

    wheel = WheelOfFortune(root, list(prizes))
    
    # Set the window to full screen
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))  # Allows exit from fullscreen with Escape key
    root.mainloop()
