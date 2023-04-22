import math
import random

class Light:
    def __init__(self, x, y, intensity, range):
        self.x = x
        self.y = y
        self.intensity = intensity
        self.range = range

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.identity_brightness = 0
        self.is_light_tile = False

def create_tile_grid(width, height):
    return [[Tile(x, y) for y in range(height)] for x in range(width)]

def update_tile_brightness(tile_grid, lights):
    for light in lights:
        # Calculate the range of tiles affected by the light
        minX = max(math.floor(light.x - light.range), 0)
        maxX = min(math.ceil(light.x + light.range), len(tile_grid) - 1)
        minY = max(math.floor(light.y - light.range), 0)
        maxY = min(math.ceil(light.y + light.range), len(tile_grid[0]) - 1)

        # Loop through all the affected tiles and update their brightness
        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                # Check if the tile is within the light's range
                distance = math.sqrt((light.x - x) ** 2 + (light.y - y) ** 2)
                if distance <= light.range:
                    # Calculate the brightness for this tile based on the light's properties
                    if distance > 0:
                        brightness = light.intensity / distance ** 2
                    else:
                        brightness = 0

                    # Update the brightness of the tile in the tile_grid
                    tile_grid[x][y].identity_brightness += brightness

                    # Mark this tile as a light source so we can render it differently
                    tile_grid[x][y].is_light_tile = True

def print_tile_grid(tile_grid):
    """
    Prints the tile grid to the console, with light tiles indicated by white squares
    and grayscale squares for other tiles, based on their brightness.
    """
    for y in range(len(tile_grid[0])):
        for x in range(len(tile_grid)):
            tile = tile_grid[x][y]
            # Check if the tile is a light tile
            if any((x == light.x and y == light.y) for light in lights):
                # Print a white square for light tiles
                print("\033[48;2;255;211;67m  \033[m", end="")
            else:
                # Print a grayscale square based on the brightness
                brightness = tile.identity_brightness
                gray_value = round(255 * brightness)
                if gray_value < 0:
                    gray_value = 0
                elif gray_value > 255:
                    gray_value = 255
                gray_code = "\033[48;2;{0};{0};{0}m  \033[m".format(gray_value)
                print(gray_code, end="")
        print("")

samples_question = input("Enter a number of samples: ")
intensity_question = input("Enter light intensity (0->1): ")
range_question = input("Enter light range (1->9): ")
samples = int(samples_question)
light_intensity = float(intensity_question)
light_range = int(range_question)

max_lights = 2
lights_amount = 0

for i in range(samples):
    print("SAMPLE #" + str(i+1) + "")
    # Example usage
    tile_grid = create_tile_grid(10, 10)

    lights = []

    for x in range(10):
        for y in range(10):
            if lights_amount <= max_lights:
                light_probability = random.randrange(0,60)

                if light_probability > 58:
                    lights.append(Light(x,y,light_intensity,light_range))
                    light_intensity += 1

    update_tile_brightness(tile_grid, lights)
    print(print_tile_grid(tile_grid))

print("YELLOW: Light point (Random range & intensity)")