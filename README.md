# Magikal-Lands

This is a woking concept for a game I have in mind.

Currently, the game loads the player and a randomly generated tile map onto the screen.

There are elemental orbs located at specific positions in the world. These orbs modify the environmental conditions(temperature and humidity) of its surroundings.
As time passes, these physical properties diffuse to its suroundings until an equilibrium is achieved.

Different environmental conditions can lead to different tile types. Currently they are the plains(lightgreen), swampy(darkgreen), snow(white), desert(orange) and cursed(brown).

For efficiency during runtime, the entire world map has been divided into chunks and each chunk has particular environmental conditions(temperature and humidity). The environmental conditions of any tile is then calculated from the chunk it is in and the surrounding chunks, with a weight function dependant on the distance of that tile from the center of the chunks.

Also, the temperature and humidity are measured in a scale of 1 to 100.  
Temperature of 1: Very cold.  
Temperature of 100: Very hot.  
Humidity of 1: Very dry.  
Humidity of 100: Very humid.  


# Screenshots

Plains.
![Plains](https://github.com/monopolize-all/Magikal-Lands/blob/master/Screenshots/Plains.png)

Plains to snow transition.
![Snow transition](https://github.com/monopolize-all/Magikal-Lands/blob/master/Screenshots/Snow%20transition.png)

Plains to swamp transition.
![Swamp transition](https://github.com/monopolize-all/Magikal-Lands/blob/master/Screenshots/Swampy%20transition.png)

Plains to desert transition.
![Desert transition](https://github.com/monopolize-all/Magikal-Lands/blob/master/Screenshots/Desert%20transition.png)

Plains to wasteland transition.
![Wasteland transition](https://github.com/monopolize-all/Magikal-Lands/blob/master/Screenshots/Wasteland%20transition.png)

Cold orb. Reduces temperature of surroundings.
![Cold orb](https://github.com/monopolize-all/Magikal-Lands/blob/master/Screenshots/Cold%20orb.png)

Map view.
![Map view](https://github.com/monopolize-all/Magikal-Lands/blob/master/Screenshots/Map%20before%20diffusion.png)

Map during start of diffusion.
![Diffusion start](https://github.com/monopolize-all/Magikal-Lands/blob/master/Screenshots/Map%20during%20start%20of%20diffusion.png)

Map after diffusion reaches equilibrium.
![Diffusion end](https://github.com/monopolize-all/Magikal-Lands/blob/master/Screenshots/map%20after%20diffusion%20equilibrium.png)


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
