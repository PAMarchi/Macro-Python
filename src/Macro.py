""" Program made by Pedro Arthur Marchi to work like a macro for mouse and keyboard input """

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator
import keyboard
import mouse
import threading
import time

class App(QtWidgets.QWidget):

  def __init__(self):

    super().__init__()
    self.initUI()
    self.settings()
    self.initialize_components()
    self.initialize_flags()
  
  """ Method to start the programs interface """
  def initUI(self):

    # UI elements objects
    self.setkeybutton     = QtWidgets.QPushButton("Click to set the key")
    self.label_interval   = QtWidgets.QLabel("Interval between presses (s)")
    self.input_interval   = QtWidgets.QLineEdit()
    self.label_startdelay = QtWidgets.QLabel("Delay to start (s)")
    self.input_startdelay = QtWidgets.QLineEdit()
    self.startbutton      = QtWidgets.QPushButton("Start")

    self.input_interval.setValidator(QIntValidator())
    self.input_startdelay.setValidator(QIntValidator())

    # Layout parent
    self.master_layout = QtWidgets.QHBoxLayout()

    col1 = QtWidgets.QVBoxLayout()
    col2 = QtWidgets.QVBoxLayout()

    # Collumn 1
    col1.addWidget(self.setkeybutton)

    # Collumn 2
    col2.addWidget(self.label_interval)
    col2.addWidget(self.input_interval)
    col2.addWidget(self.label_startdelay)
    col2.addWidget(self.input_startdelay)
    col2.addWidget(self.startbutton)

    # Adjusting widgets sizes
    self.setkeybutton.setMinimumSize(150, 130)

    # Adding the sub layouts to the main one
    self.master_layout.addLayout(col1, 50)
    self.master_layout.addLayout(col2, 50)

    self.setLayout(self.master_layout)

  """ Method to set the programs settings """
  def settings(self):

    self.setWindowTitle("Macro by Arthur Marchi")
    self.setGeometry(250, 250, 320, 100)
    self.setFixedSize(320, 150)

  """ Method to initialize the components """
  def initialize_components(self):

    # Components setup
    self.startbutton.setEnabled(False) # Button to start the program starts disabled

    # Sets which methods are executed when the programs buttons are pressed
    self.setkeybutton.clicked.connect(self.register_key)
    self.startbutton.clicked.connect(self.start_stop_button)

  """ Method to initialize the flags """
  def initialize_flags(self):

    # Flags setup
    self.stopflag = False # Flag to stop the start thread starts in False state
    self.switch = True # Flag for the start/stop state of the button starts in True state, which represents the waiting to start state of the button

  """ Method that is called when the register key button is pressed """
  def register_key(self):

    # After the button to register key is pressed it goes off until the key has been gotten
    self.setkeybutton.setEnabled(False)

    # Flag representing whether the key has been gotten or not
    self.keygot_flag = False

    # Starts a thread to listen for a  mouse click and other listening to the keyboard
    threading.Thread(target=self.mouse_click_thread).start()
    threading.Thread(target=self.keyboard_press_thread).start()

  """ Method to thread, it listen and gets the mouse input when the user is trying to register a key press """
  def mouse_click_thread(self):

    mouse.on_click(callback=self.left_click_callback) # If the left mouse is clicked the specific function is executed
    mouse.on_right_click(callback=self.right_click_callback) # If the right mouse is clicked the specific function is executed
    mouse.on_middle_click(callback=self.middle_click_callback) # If the middle mouse is clicked the specific function is executed
    
  """ Method that executes when the left mouse key is clicked """
  def left_click_callback(self):

    # If the key press hasn't already been gotten
    if(not self.keygot_flag):
      self.keygot_flag = True # Key has been gotten
      self.startbutton.setEnabled(True) # Enables the programs start button
      self.keypressed = "left mouse click" # Register the key
      self.setkeybutton.setText("'left mouse' selected") # Changes the setkeybutton to the selected key

    self.setkeybutton.setEnabled(True) # Re-enables the set key button
    return

  """ Method that executes when the right mouse key is clicked """
  def right_click_callback(self):

    # If the key press hasn't already been gotten
    if(not self.keygot_flag):
      self.keygot_flag = True # Key has been gotten
      self.startbutton.setEnabled(True) # Enables the programs start button
      self.keypressed = "right mouse click" # Register the key
      self.setkeybutton.setText("'right mouse' selected") # Changes the setkeybutton to the selected key
    
    self.setkeybutton.setEnabled(True) # Re-enables the set key button
    return
  
  """ Method that executes when the middle mouse key is clicked """
  def middle_click_callback(self):
    
    # If the key press hasn't already been gotten
    if(not self.keygot_flag):
      self.keygot_flag = True # Key has been gotten
      self.startbutton.setEnabled(True) # Enables the programs start button
      self.keypressed = "middle mouse click" # Register the key
      self.setkeybutton.setText("'middle mouse' selected") # Changes the setkeybutton to the selected key
    
    self.setkeybutton.setEnabled(True) # Re-enables the set key button
    return

  """ Method to thread, it listen and gets the keyboard input when the user is trying to register a key press """
  def keyboard_press_thread(self):
    
    keypressed = keyboard.read_key() # Waits for a keyboard key press
    
    # If the key has not already been gotten
    if(not self.keygot_flag):

      self.keygot_flag = True # Key has been gotten
      self.startbutton.setEnabled(True) # Enables the programs start button
      self.keypressed = keypressed # Register the key
      self.setkeybutton.setText(f"\'{keypressed}\' selected") # Changes the setkeybutton to the selected key
        
    self.setkeybutton.setEnabled(True) # Re-enables the set key button
    return
  
  """ Method to get and assign the interval between presses """
  def get_interval(self):

    self.interval = self.input_interval.text() # Reads the input to get the interval

  """ Method to get and assign the delay to start the presses """
  def get_delay(self):
    
    self.delay = self.input_startdelay.text() # Reads the input to get the delay

  """ Method to manage the start/stop button """
  def start_stop_button(self):

    # Fetches the inputs to get the parameters
    self.get_interval()
    self.get_delay()

    # If the switch is in the waiting to start state
    if(self.switch):

      self.startbutton.setText("Stop") # After the click it changes to Stop text
      threading.Thread(target=self.start).start() # Starts the start thread
      self.switch = False # Switch is now on the stop state

    # If the switch is in the waiting to stop state
    elif(not self.switch):

      self.startbutton.setText("Start") # After the click it changes to Start text again
      threading.Thread(target=self.stop).start() # Starts the stop thread
      self.switch = True # Switch is now on the start state again

  """ Method to thread, it manages what the program do when it's told to start """
  def start(self):

    # Flag to stop is set to False
    self.stopflag = False

    time.sleep(int(self.delay)) # Delay to start

    # While the flag to stop is not set to True
    while(not self.stopflag):

      # If the input was from the mouse
      if(self.keypressed == "left mouse click"):
        mouse.click("left")
      elif(self.keypressed == "right mouse click"):
        mouse.click("right")
      elif(self.keypressed == "middle mouse click"):
        mouse.click("middle")

      # If the input was from the keyboard
      else:
        keyboard.press(self.keypressed)

      time.sleep(int(self.interval)) # Interval between presses

  """ Method to thread, it manages what the program do when it's told to stop"""
  def stop(self):

    self.stopflag = True # Turn on the flag to stop the start thread execution
    self.setkeybutton.setText("Click to set the key") # Restart the text from setkeybutton


def main():

  app_instance = QtWidgets.QApplication([])

  app_window = App()
  app_window.show()

  app_instance.setApplicationName("Macro by Arthur Marchi")
  app_instance.exec()


if __name__ == "__main__":

  main()