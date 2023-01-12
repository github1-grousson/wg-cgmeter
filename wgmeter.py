'''
 # @ Author: Wilfried Grousson
 # @ Created: 2023-01-12
 # @ License: MIT
 # @ Description: This is the main application entry point
 '''


''' Personal imports '''
from gui.cgmainapp import CGMainApp


if __name__ == "__main__":
    # Create the main window
    app = CGMainApp()
    app.run()