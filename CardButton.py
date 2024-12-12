from tkinter import Button, PhotoImage
from resources import resource_path, BACKGROUND_COLOR

class CardButton(Button):
    def __init__(self, window, image, active_image, command):
        super().__init__(
            master=window,
            command=command,
            borderwidth=0,
            bg=BACKGROUND_COLOR,
            activebackground=BACKGROUND_COLOR
        )
        self.image = PhotoImage(file=resource_path(image))
        self.active_image = PhotoImage(file=resource_path(active_image))
        self.config(image=self.image)

        self.bind("<Enter>",lambda event: on_hover(event=event, hover_image=self.active_image))
        self.bind("<Leave>",lambda event: on_leave(event=event, default_image=self.image))

        def on_hover(event, hover_image):
            self.config(image=hover_image)

        def on_leave(event, default_image):
            self.config(image=default_image)