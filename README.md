# Magikal-Lands

This is a woking concept for a game I have in mind.

Currently, the game loads the player and a randomly generated tile map onto the screen.

There are elemental orbs located at specific positions in the world. These orbs modify the environmental conditions(temperature and humidity) of its surroundings.
As time passes, these physical properties diffuse to its suroundings until an equilibrium is achieved.

Different environmental conditions can lead to different tile types. Currently they are the plains(lightgreen), swampy(darkgreen), snow(white), desert(orange) and cursed(brown).

For efficiency during runtime, the entire world map has been divided into chunks and each chunk has particular environmental conditions(temperature and humidity). The environmental conditions of any tile is then calculated from the chunk it is in and the surrounding chunks, with a weight function dependant on the distance of that tile from the center of the chunks.


# Running the program

To run the program, first clone this repository to a local directory.

Then run the following command in a terminal opened from this directory to install all required dependencies:

```
pip install -r requirements.txt
```

Finally run main.py from the same terminal.

```
python main.py
```

# Interaction with the game

Use arrow keys to move around the world.

The following keys are mapped to the following actions:

1 -> Diffuses physical properties.

2 -> Updates entities.

3 -> Toggles live diffusion.

4 -> Runs diffusion and updation for 100 frames.

     Caution: I do not recommend leaving DEBUG = True for the below two actions.

5 -> Runs diffusion and updation for 1000 frames.

6 -> Runs diffusion and updation for 10000 frames.
     
7 -> Slows down player movement speed.

8 -> Speeds up player movement speed.

m -> Toggles world map.

q -> Closes the game.


# Known issues


# Credits

Brainstorming for ideas: Agamdeep Singh(https://github.com/jnash10)

Assets(images): Pixel-Boy(https://pixel-boy.itch.io/ninja-adventure-asset-pack)(https://www.patreon.com/pixelarchipel)
