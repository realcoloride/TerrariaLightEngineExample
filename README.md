# Terraria Light Engine Example
Example Terraria Light Engine in Python for ease of testing and prototyping, as well in PSEUDO-CODE to implement in any type of engine or programming language.

# Introduction
## Getting the brightness
I have been for weeks digging in my head a reliable way of retrieving the light values of my tiles in the Terraria engine like game. 
I have tried many techniques and algorithms, but they weren't as really as performant as I would have wanted.

**However, after a long long time of trying and failing, I have found a way of calculating light using a math formula! 🥳**

## How it works

### Theory
#### The formula used is based on the **Inverse Square Law**, which states that the intensity of a physical quantity, such as light, sound, or radiation, decreases inversely with the square of the distance from the source.

In this case, this law is used to calculate the brightness of a tile based on its distance from a light source. The formula used is:
> brightness = light.intensity / distance^2

Where:

"brightness" is the resulting brightness value of the tile.
"light.intensity" is the intensity of the light source.
"distance" is the distance between the light source and the tile.
The formula is derived from the Inverse Square Law, where the intensity of the light source decreases proportionally to the square of the distance between the source and the tile. This means that the further away a tile is from the light source, the dimmer it will be.

By using this formula to calculate the brightness of each tile in the affected area, the  formula is able to accurately simulate the lighting effects in the game world, giving it a more realistic and immersive feel.

### Implementation
Now that we know how it works in theory, we can finally approach the code side of it:

- Calculate the range of tiles that will be affected by the light. This is determined by finding the minimum and maximum x and y values that are within the range of the light source.
- Loop through all the tiles within the range of the light source, and for each tile, do the following:
- a. Calculate the distance between the light source and the tile using the Pythagorean theorem.
- b. Check if the tile is within the range of the light source by comparing the distance to the range of the light source.
- c. Calculate the brightness of the tile based on the intensity of the light source and its distance from the tile, using the inverse square law.
- d. Update the brightness of the tile in the tile grid by adding the calculated brightness to the current brightness of the tile.
- e. Mark the tile as a light source so it can be rendered differently.

Once all the light sources have been processed, the tile grid will have updated brightness values and light sources marked.

### The code
In python, we can calculate the brightness this way:
```py
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
```
And for the pseudo code, here is a more beginner friendly and flexible approach:
```py
for each light in lights:
    # Calculate the range of tiles affected by the light
    minX = maximum(floor(light.x - light.range), 0)
    maxX = minimum(ceil(light.x + light.range), len(tile_grid) - 1)
    minY = maximum(floor(light.y - light.range), 0)
    maxY = minimum(ceil(light.y + light.range), len(tile_grid[0]) - 1)
    # Loop through all the affected tiles and update their brightness
    for x from minX to maxX:
        for y from minY to maxY:
            # Check if the tile is within the light's range
            distance = square_root((light.x - x)^2 + (light.y - y)^2)
            if distance <= light.range:
                # Calculate the brightness for this tile based on the light's properties
                if distance > 0:
                    brightness = light.intensity / distance ^ 2
                else:
                    brightness = 0

                # Update the brightness of the tile in the tile_grid
                tile_grid[x][y].identity_brightness += brightness

                # Mark this tile as a light source so we can render it differently
                tile_grid[x][y].is_light_tile = true
```

### The results
![Code_yZBu2nCARu](https://user-images.githubusercontent.com/108619637/233785334-a46999d0-a6f4-4fa9-bf59-2d89cc916dec.png)
![Code_z0HojrT6Q3](https://user-images.githubusercontent.com/108619637/233785339-4ac63848-be1c-4fdf-ac3c-00e0bb92a13b.png)

*The yellow tiles are where the lights were randomly placed.*
The example is available in the source code.

## Lightmasks
In games like terraria or starbound, once we have this result, we call this a Lightmap. This lightmap is used to be multiplied in order to mix and blend colors. Kind of like if you did it in photoshop.


### How, why?
#### We just multiply colors?
Both Terraria and Starbound use lightmaps to simulate lighting effects in their 2D environments. In both games, each tile has a "light" value that represents the amount of light it emits, and this light value is stored in the lightmap.
When a light source is placed in the world, the game updates the lightmap by calculating the range of tiles affected by the light and then updating their light values, as we did above.

The updated lightmap is then used during rendering to calculate the color of each pixel on the screen. This involves multiplying the color of each pixel by the corresponding light value in the lightmap. This results in the appearance of shadows and other lighting effects, creating a more immersive and dynamic environment.

##### Implementing
Implementing is only a matter of how you do it. There's plenty of ways:
- Shaders
- Render buffer
...

But it all goes down to what is called **deferred rendering**.
![image](https://user-images.githubusercontent.com/108619637/233785864-5fc244da-7b00-4f01-8309-a8a7e8a57ad8.png)

In short, just means that you go through processes before rendering your actual frame.
So lets say you store a texture of your tiles, and then of your lightmap. Multiply, and boom! magic.

Now here is an example (not representive of the engine above):
In those examples, the lightmap needs to represent a pixel per tile, then its resized.

Here is our tiles sample:
![image](https://user-images.githubusercontent.com/108619637/233785700-9c01e5a8-fd1a-406a-9ecf-78945fdfb1ef.png)

Here is out lightmap:
![image](https://user-images.githubusercontent.com/108619637/233785710-a90630ef-dcf8-4e36-ab49-0568fffbbb24.png)

Now multiplicating, we get this:
![image](https://user-images.githubusercontent.com/108619637/233785714-b5412b95-f379-4f58-9b66-060a1b64047b.png)

After using bilinear sampling instead of a nearest neighbour sampling (pixel-perfect one):
![image](https://user-images.githubusercontent.com/108619637/233785726-2ed1684a-3c93-450e-98ea-c690379d68ff.png)

We get something that could look like how starbound handles the lighting or terraria does.
However, Vanilla Terraria lighting doesnt go through the process of blurring the lightmap.

# Found this useful?
I'm glad it helped. If someone ever needs helps or kind of useful resource, please send this little page.
If you wish, use the code everywhere you want, in any kind of project, as its licensed MIT.

⭐ If you want to support me, just credit me & leave a little star :)

# Upcoming
- [ ] Lighting with color
