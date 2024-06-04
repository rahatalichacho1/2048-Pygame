import pygame  # Importing the Pygame library for game development
import random  # Importing the random module for generating random numbers
import math    # Importing the math module for mathematical operations

pygame.init()  # Initializing Pygame

Fps = 60  # Frames per second
Width, Height = 800, 600  # Setting up the window size
Rows = 4  # Number of rows in the grid
Cols = 4  # Number of columns in the grid
Rect_Height = Height // Rows  # Height of each grid rectangle
Rect_Width = Width // Cols  # Width of each grid rectangle
outline_color = (187, 173, 160)  # Color for grid outlines
outline_thickness = 10  # Thickness of grid outlines
background_color = (205, 192, 180)  # Background color of the game window
font_color = (119, 110, 101)  # Color for text displayed on tiles
font = pygame.font.SysFont("comicsans", 60, bold=True)  # Font settings for text on tiles

move_vel = 20  # Velocity of tile movement
window = pygame.display.set_mode((Width, Height))  # Creating the game window
pygame.display.set_caption("2048")  # Setting the window title

class Tile:  # Class representing a single tile on the grid
    colors = [  # List of colors for different tile values
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):  # Constructor for Tile class
        self.value = value  # Value of the tile
        self.row = row  # Row index of the tile
        self.col = col  # Column index of the tile
        self.x = col * Rect_Width  # x-coordinate of the tile's position
        self.y = row * Rect_Height  # y-coordinate of the tile's position

    def get_color(self):  # Method to get the color of the tile based on its value
        color_index = int(math.log2(self.value)) - 1  # Calculate color index based on value
        color = self.colors[color_index]  # Get color from the predefined list
        return color  # Return the color

    def draw(self, window):  # Method to draw the tile on the game window
        color = self.get_color()  # Get color of the tile
        pygame.draw.rect(window, color, (self.x, self.y, Rect_Width, Rect_Height))  # Draw rectangle representing the tile
        text = font.render(str(self.value), 1, font_color)  # Render text with tile value
        window.blit(  # Blit (draw) the text onto the game window
            text,
            (
                self.x + (Rect_Width / 2 - text.get_width() / 2),
                self.y + (Rect_Height / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):  # Method to set the position of the tile on the grid
        if ceil:  # If ceil flag is True
            self.row = math.ceil(self.y / Rect_Height)  # Round up the row index
            self.col = math.ceil(self.x / Rect_Width)   # Round up the column index
        else:  # If ceil flag is False
            self.row = math.floor(self.y / Rect_Height)  # Round down the row index
            self.col = math.floor(self.x / Rect_Width)   # Round down the column index

    def move(self, delta):  # Method to move the tile by a given delta (change in position)
        self.x += delta[0]  # Update x-coordinate based on delta in x direction
        self.y += delta[1]  # Update y-coordinate based on delta in y direction

def draw_grid(window):  # Function to draw the grid lines on the game window
    for row in range(1, Rows):  # Iterate through each row (except the first one)
        y = row * Rect_Height  # Calculate y-coordinate of the grid line
        pygame.draw.line(window, outline_color, (0, y), (Width, y), outline_thickness)  # Draw horizontal grid line

    for col in range(1, Cols):  # Iterate through each column (except the first one)
        x = col * Rect_Width  # Calculate x-coordinate of the grid line
        pygame.draw.line(window, outline_color, (x, 0), (x, Height), outline_thickness)  # Draw vertical grid line

    pygame.draw.rect(window, outline_color, (0, 0, Width, Height), outline_thickness)  # Draw outline around the entire grid

def draw(window, tiles):  # Function to draw the game window
    window.fill(background_color)  # Fill the window with background color

    for tile in tiles.values():  # Iterate through each tile in the dictionary of tiles
        tile.draw(window)  # Draw the tile on the window

    draw_grid(window)  # Draw the grid lines on the window

    pygame.display.update()  # Update the display to show the changes

def get_random_position(tiles):  # Function to get a random position for a new tile
    while True:  # Keep looping until a valid position is found
        row = random.randrange(0, Rows)  # Generate a random row index
        col = random.randrange(0, Cols)  # Generate a random column index
        if f"{row},{col}" not in tiles:  # Check if the position is not already occupied by a tile
            break  # If the position is valid, break out of the loop

    return row, col  # Return the randomly generated row and column indices

def generate_tiles():  # Function to generate initial tiles on the grid
    tiles = {}  # Dictionary to store tiles
    for _ in range(2):  # Generate two initial tiles
        row, col = get_random_position(tiles)  # Get a random position for the new tile
        tiles[f"{row},{col}"] = Tile(2, row, col)  # Create a new tile with value 2 at the random position

    return tiles  # Return the dictionary of initial tiles

def move_tile(window, tiles, clock, direction):  # Function to handle tile movement
    update = True  # Flag to indicate whether an update is needed
    blocks = set()  # Set to keep track of tiles that have already merged

    if direction == "left":  # If the direction is left
        sort_function = lambda x: x.col  # Sort function for tiles based on column index
        reverse = False  # Direction of sorting
        delta = (-move_vel, 0)  # Delta for moving tiles left
        boundary_check = lambda tile: tile.col == 0  # Function to check if a tile is at the left boundary
        get_next_tile = lambda tile: tiles.get(f"{tile.row},{tile.col-1}")  # Function to get the tile to the left
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + move_vel  # Function to check if tiles can merge
        move_check = lambda tile, next_tile: tile.x > next_tile.x + Rect_Width + move_vel  # Function to check if tiles can move
        ceil = True  # Flag to indicate rounding up while setting position

    elif direction == "right":  # If the direction is right
        sort_function = lambda x: x.col  # Sort function for tiles based on column index
        reverse = True  # Direction of sorting
        delta = (move_vel, 0)  # Delta for moving tiles right
        boundary_check = lambda tile: tile.col == Cols - 1  # Function to check if a tile is at the right boundary
        get_next_tile = lambda tile: tiles.get(f"{tile.row},{tile.col + 1}")  # Function to get the tile to the right
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - move_vel  # Function to check if tiles can merge
        move_check = lambda tile, next_tile: tile.x + Rect_Width + move_vel < next_tile.x  # Function to check if tiles can move
        ceil = False  # Flag to indicate rounding down while setting position

    elif direction == "up":  # If the direction is up
        sort_function = lambda x: x.row  # Sort function for tiles based on row index
        reverse = False  # Direction of sorting
        delta = (0, -move_vel)  # Delta for moving tiles up
        boundary_check = lambda tile: tile.row == 0  # Function to check if a tile is at the top boundary
        get_next_tile = lambda tile: tiles.get(f"{tile.row-1},{tile.col}")  # Function to get the tile above
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + move_vel  # Function to check if tiles can merge
        move_check = lambda tile, next_tile: tile.y > next_tile.y + Rect_Height + move_vel  # Function to check if tiles can move
        ceil = True  # Flag to indicate rounding up while setting position

    elif direction == "down":  # If the direction is down
        sort_function = lambda x: x.row  # Sort function for tiles based on row index
        reverse = True  # Direction of sorting
        delta = (0, move_vel)  # Delta for moving tiles down
        boundary_check = lambda tile: tile.row == Rows - 1  # Function to check if a tile is at the bottom boundary
        get_next_tile = lambda tile: tiles.get(f"{tile.row+1},{tile.col}")  # Function to get the tile below
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - move_vel  # Function to check if tiles can merge
        move_check = lambda tile, next_tile: tile.y + Rect_Height + move_vel < next_tile.y  # Function to check if tiles can move
        ceil = False  # Flag to indicate rounding down while setting position

    while update:  # Continue looping until no further updates are needed
        clock.tick(Fps)  # Limit the frame rate
        update = False  # Reset the update flag
        sorted_tiles = sorted(tiles.values(), key=sort_function, reverse=reverse)  # Sort the tiles based on the chosen direction

        for i, tile in enumerate(sorted_tiles):  # Iterate through each tile in the sorted list
            if boundary_check(tile):  # If the tile is at the boundary in the chosen direction
                continue  # Skip this tile and move to the next one

            next_tile = get_next_tile(tile)  # Get the tile in the direction of movement
            if not next_tile:  # If there's no tile in the direction of movement
                tile.move(delta)  # Move the current tile in that direction
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:  # If the values of the two tiles are equal and they haven't already merged
                if merge_check(tile, next_tile):  # If the tiles are far enough apart to merge
                    tile.move(delta)  # Move the current tile towards the next tile
                else:  # If the tiles are close enough to merge
                    next_tile.value += tile.value  # Merge the tiles by adding their values
                    sorted_tiles.pop(i)  # Remove the current tile from the list of tiles
                    blocks.add(next_tile)  # Add the next tile to the set of merged tiles
            elif move_check(tile, next_tile):  # If there's enough space between the tiles to move
                tile.move(delta)  # Move the current tile towards the next tile
            else:  # If none of the above conditions are met
                continue  # Skip this tile and move to the next one

            tile.set_pos(ceil)  # Set the position of the tile on the grid
            update = True  # Set the update flag to True

        update_tiles(window, tiles, sorted_tiles)  # Update the tiles on the game window

    end_move(tiles)  # Perform end-of-move actions and check for game over

def end_move(tiles):  # Function to handle actions at the end of a move
    if len(tiles) == 16:  # If the grid is fully occupied
        return "lost"  # Return "lost" to indicate game over

    row, col = get_random_position(tiles)  # Get a random position for a new tile
    tiles[f"{row},{col}"] = Tile(random.choice([2, 4]), row, col)  # Create a new tile with either value 2 or 4 at the random position
    return "continue"  # Return "continue" to indicate the game can continue

def update_tiles(window, tiles, sorted_tiles):  # Function to update the tiles on the game window
    tiles.clear()  # Clear the dictionary of tiles
    for tile in sorted_tiles:  # Iterate through each sorted tile
        tiles[f"{tile.row},{tile.col}"] = tile  # Add the tile to the dictionary of tiles
    draw(window, tiles)  # Draw the updated tiles on the game window

def main(window):  # Main function to run the game
    clock = pygame.time.Clock()  # Create a Pygame clock object
    run = True  # Flag to indicate whether the game is running
    tiles = generate_tiles()  # Generate initial tiles on the grid
    while run:  # Main game loop
        clock.tick(Fps)  # Limit the frame rate
        for event in pygame.event.get():  # Iterate through each Pygame event
            if event.type == pygame.QUIT:  # If the user quits the game
                run = False  # Exit the game loop
                break  # Exit the event loop
            if event.type == pygame.KEYDOWN:  # If a key is pressed
                if event.key == pygame.K_LEFT:  # If the left arrow key is pressed
                    move_tile(window, tiles, clock, "left")  # Move tiles left
                if event.key == pygame.K_RIGHT:  # If the right arrow key is pressed
                    move_tile(window, tiles, clock, "right")  # Move tiles right
                if event.key == pygame.K_UP:  # If the up arrow key is pressed
                    move_tile(window, tiles, clock, "up")  # Move tiles up
                if event.key == pygame.K_DOWN:  # If the down arrow key is pressed
                    move_tile(window, tiles, clock, "down")  # Move tiles down

        draw(window, tiles)  # Draw the game window

    pygame.quit()  # Quit Pygame when the game loop ends

if __name__ == "__main__":  # Check if the script is executed directly
    main(window)  # Run the main function to start the game
