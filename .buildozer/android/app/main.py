import time 


from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.behaviors import ButtonBehavior

class ColoredBox(BoxLayout):
    def __init__(self, color, base_frequency, app, **kwargs):
        super(ColoredBox, self).__init__(**kwargs)
        self.base_frequency = base_frequency
        self.target_duration = 1.0 / (2 * self.base_frequency)  # Duration of each state in seconds
        self.state_duration = 0
        self.elapsed_time = 0
        self.state_changes = []  # List to store timestamps of state changes
        self.flicker_state = 1
        self.app = app

        with self.canvas.before:
            Color(*color)
            self.rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(size=self.update_rect_size, pos=self.update_rect_pos)

        # Add frequency label
        self.frequency_label = Label(text=f"Frequency: {self.base_frequency}", size_hint=(1, 0.2))
        self.add_widget(self.frequency_label)

    def update_rect_size(self, instance, value):
        self.rect.size = value

    def update_rect_pos(self, instance, value):
        self.rect.pos = value

    def update(self, dt):
        if self.app and self.app.is_running:
            self.elapsed_time += dt
            self.state_duration += dt

            # Check if it's time to change the flicker state
            if self.state_duration >= self.target_duration:
                self.flicker_state = 1 - self.flicker_state  # Toggle flicker state
                self.state_duration = 0  # Reset state duration

            # Set opacity based on flicker state
            self.opacity = int(self.state_duration < self.target_duration and self.flicker_state == 1)

            # Reset elapsed time after a full second
            if self.elapsed_time >= 1.0:
                self.elapsed_time -= 1.0

            # Update frequency label
            self.frequency_label.text = f"Frequency: {self.base_frequency}"

class ResponseBox(ButtonBehavior, ColoredBox):
    def __init__(self, color, base_frequency, app, index, **kwargs):
        super(ResponseBox, self).__init__(color=color, base_frequency=base_frequency, app=app, orientation="vertical", **kwargs)
        self.index = index

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Save the response with timestamp
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            response = f"User attended to Box {self.index+1} at {timestamp}"
            print(response)  # Replace with your desired storage or processing logic

class FlickeringBoxesApp(App):
    def build(self):
        self.layout = GridLayout(cols=2, spacing=10)
        words = ["Banana", "Apple", "Orange", "Cucumber"]
        frequencies = [6, 12, 20, 4]
        self.response_boxes = []

        for i, word in enumerate(words):
            base_frequency = frequencies[i]
            response_box = ResponseBox(color=(0.8, 0.8, 0.8, 1), base_frequency=base_frequency, app=self, index=i)
            label = Label(text=word, font_size=30)
            response_box.add_widget(label)

            self.layout.add_widget(response_box)
            self.response_boxes.append(response_box)

            Clock.schedule_interval(response_box.update, 1.0 / 10000)

        toggle_button = Button(text="Start", on_press=self.toggle_clock)
        settings_button = Button(text="Settings", on_press=self.show_settings_popup)

        button_layout = BoxLayout(size_hint_y=None, height=50)
        button_layout.add_widget(toggle_button)
        button_layout.add_widget(settings_button)  # Add the settings button

        root_layout = BoxLayout(orientation='vertical')
        root_layout.add_widget(self.layout)
        root_layout.add_widget(button_layout)

        self.is_running = False  # Initialize is_running attribute
        self.settings_popup = None  # Initialize settings_popup attribute

        return root_layout
    
    def show_settings_popup(self, instance):
        if not self.settings_popup:
            self.settings_popup = SettingsPopup(self)
        self.settings_popup.open()
    
    def toggle_clock(self, instance):
        self.is_running = not self.is_running
        instance.text = "Stop" if self.is_running else "Start"

    def show_settings_popup(self, instance):
        popup_content = BoxLayout(orientation='vertical', spacing=10, size=(400, 300))  # Adjust size here

        for i, box in enumerate(self.response_boxes):
            current_word = box.children[0].text
            current_frequency = str(box.base_frequency)

            word_input = TextInput(multiline=False, size=(200, 30))  # Adjust size here
            frequency_input = TextInput(multiline=False, size=(80, 30))  # Adjust size here

            # Assigning ids to the TextInput widgets
            setattr(popup_content.ids, f"word_input_{i}", word_input)
            setattr(popup_content.ids, f"frequency_input_{i}", frequency_input)

            word_input.text = current_word
            frequency_input.text = current_frequency

            box_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=30)
            box_layout.add_widget(Label(text=f"Word {i + 1}:"))
            box_layout.add_widget(word_input)
            box_layout.add_widget(Label(text=f"Frequency {i + 1}:"))
            box_layout.add_widget(frequency_input)

            popup_content.add_widget(box_layout)

        save_button = Button(text="Save", on_press=lambda *args: self.save_settings(popup_content), size_hint=(None, None), size=(100, 30))  # Adjust size here

        popup_content.add_widget(save_button)

        self.settings_popup = Popup(title='Settings', content=popup_content, size=(400, 300))
        self.settings_popup.open()

    def save_settings(self, popup_content):
        for i, box in enumerate(self.response_boxes):
            word_input = getattr(popup_content.ids, f"word_input_{i}")
            frequency_input = getattr(popup_content.ids, f"frequency_input_{i}")

            # Update each box with the new settings
            box.children[0].text = word_input.text  # Update label text
            box.base_frequency = int(frequency_input.text)  # Update base frequency
            box.target_duration = 1.0 / (2 * box.base_frequency)  # Update target duration

            # Update the frequency label in real-time
            box.frequency_label.text = f"Frequency: {box.base_frequency}"

        # Close the popup
        self.settings_popup.dismiss()

    def update_boxes(self, dt):
        for box in self.response_boxes:
            box.update(dt)

class SettingsPopup(Popup):
    def __init__(self, app, **kwargs):
        super(SettingsPopup, self).__init__(**kwargs)
        self.app = app

if __name__ == '__main__':
    FlickeringBoxesApp().run()