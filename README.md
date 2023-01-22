# Sasuke-Advanture Game
This game is developed in Python. The simple AI for NPC characters and hand gesture recognition (Mediapipe) are also embedded into the game.

Features: 
- An AI for NPC to chase and attack the player
- An AI to detect the user's handsigns via webcam to control Sasuke
- Music + Visuals + Score Tracker system 
- Health and Mana bars 

How to use:
- Open the game '.exe' file
- Start the game
- Use W, A, S, D to control Sasuke's movements
- Press E for Sasuke to wing
- When there's enough mana, the player can activate Sharingan by pressing R
  Sharingan helps slow down enemies' movements at the cost of reducing mana overtime
- To perform a sequence of 4 handsign:
  - Press C and show 4 handsigns. 
  - For each handsign, show your hand to the laptop's camera for at least 2 seconds before showing a new sign
  - If a valid sequence of handsigns is detected, Sasuke will perform Jutsu (Katon or Chidori)
  - If the sequence is invalid, the screen will display an 'X' symbol
  - If you want to abandone the sequence midway, click C to delete the sequence. Then click C again to show new sequence of handsigns.
