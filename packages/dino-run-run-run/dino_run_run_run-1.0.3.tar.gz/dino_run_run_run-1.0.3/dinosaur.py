#!/usr/bin/env python3

import curses
import time
import random

# Constants
GROUND_Y = 15  # The ground level
OBJECT_Y = 9
DINO_X = 10    # Fixed X position of dino
JUMP_HEIGHT = 6  # Max jump height
OBSTACLE_CHARS = ["""
   +
   A_
  /\-\\
 _||"|_
~^~^~^~^
""", 
"""
 /\ /\ /\ 
//\\\\/\\\\/\\\\
//\\\\/\\\\/\\\\  
 || || || 
 ~^~^~^~^
"""]
DINO_CHAR = """
               __
              / _)
     _.----._/ /
    /         /
 __/ (  | (  |
/__.-'|_|--|_|
"""



def game(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(100) # Controls game speed

    dino_y = OBJECT_Y
    jumping = False
    jump_count = 0
    obstacles = []
    score = 0
    pause = 0

    while True:
        stdscr.clear()

        # Draw the ground
        stdscr.addstr(GROUND_Y + 1, 0, "_" * 50)

        # Draw the dino
        stdscr.addstr(dino_y, DINO_X, DINO_CHAR)

        # Handle jumping
        if jumping:
            if jump_count == JUMP_HEIGHT:
                if pause < 7:  # Pause for 5 frames
                    pause += 1
                else:
                    jump_count += 1
            elif jump_count < JUMP_HEIGHT:
                dino_y -= 1
                jump_count += 1
            else:
                dino_y += 1
                jump_count += 1
            if jump_count >= JUMP_HEIGHT * 2:  # Full jump cycle
                jumping = False
                jump_count = 0
                pause = 0

        # Handle obstacles
        if random.randint(1, 1000) > 960:  # Random obstacle generation
            obs = random.randint(0,1)
            obstacles.append((50, OBSTACLE_CHARS[obs]))

        new_obstacles = []
        if obstacles:
            for obs_x, obs_char in obstacles:
                obs_x -= 1
                if obs_x > 0:
                    new_obstacles.append((obs_x, obs_char))

                    per_line = obs_char.split("\n")
                    for i, line in enumerate(per_line):
                        try:
                            stdscr.addstr(OBJECT_Y + 1 + i, obs_x, line)
                        except curses.error:
                            pass

        
        obstacles = new_obstacles

        # Check collision
        if DINO_X in [obs_x for obs_x, _ in obstacles] and dino_y == OBJECT_Y:
            stdscr.addstr(5, 20, "GAME OVER!")
            stdscr.refresh()
            time.sleep(2)
            break

        # Display score
        score += 1
        stdscr.addstr(0, 0, f"Score: {score}")

        # Handle input
        key = stdscr.getch()
        if key == ord(" "):  # Space to jump
            if not jumping:
                jumping = True
        elif key == ord("q"):  # Quit
            break

        stdscr.refresh()
        time.sleep(0.05)

def main():
    curses.wrapper(game)

if __name__ == "__main__":
    main()