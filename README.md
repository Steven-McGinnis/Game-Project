# Zombie Survival Game 🎮

This repository contains a **Zombie Survival Game**, developed as part of a school elective for game design using Python. It’s a simple but functional game inspired by classic zombie survival mechanics. While it’s not graphically intense, this project demonstrates my understanding of game logic, object behaviors, and Python programming in a game development context. I am particularly proud of the time and effort I put into designing object behaviors, gameplay elements, and a secret level with moving platforms.

---

## About This Game

In this game, the player survives rounds of zombie attacks while managing ammo and collecting random pickups. The game uses Python to generate zombies as moving cubes with textures applied. The primary mechanics include zombie AI, pickups, and round-based gameplay.

### Key Features:

- **Round-Based Gameplay**: Each round spawns more zombies that relentlessly move toward the player.
- **Zombie AI**: Zombies are represented as cubes with textures, which continuously move toward the player's position.
- **Random Pickups**: Zombies occasionally drop random pickups such as ammo or health.
- **Behavioral Systems**: Objects in the game have modular behaviors, such as movement, collision detection, shooting, and power-ups.
- **Secret Level**: A bonus level includes moving platforms to demonstrate my knowledge of platform mechanics and dynamic environments.

---

## Gameplay Mechanics

1. **Player Objectives**:

   - Survive as many rounds as possible by avoiding or eliminating zombies.
   - Manage resources like ammo, health, and pickups.

2. **Zombies**:

   - Spawn randomly on the map during each round.
   - Move toward the player with simple AI logic.
   - Drop pickups upon defeat.

3. **Pickups**:

   - Randomly spawned by defeated zombies.
   - Include items like additional ammo, health packs, or power-ups.

4. **Secret Level**:
   - Features dynamic moving platforms to challenge the player.
   - Designed as an additional showcase of gameplay mechanics.

---

## Code Features

- **Modular Design**: The game uses a modular structure, with behaviors applied to objects such as zombies, pickups, and platforms.
- **Behavior Files**: Each game behavior (e.g., `behavior_gravity.py`, `behavior_shoot.py`, etc.) is designed to be reusable and easily assignable to game objects.
- **Game Loop**:
  - The game logic (`GameLogic`) handles the main gameplay loop, tracking rounds, spawning objects, and handling player interactions.
  - Sounds, movies, and animations are updated with each tick of the loop.

```python
while True:
    GameLogic.tick()
    Sounds.tick()
    Movies.tick()
```

## Python-Driven Logic

The game leverages Python classes and methods to manage all aspects of gameplay, including:

- **Object Spawning**: Using `GameLogic.load_world()` to dynamically load levels from JSON files.
- **Collision Detection**: Implemented through a modular `collision.json` file for efficient object interactions.
- **Customizable Behaviors**: Modular behavior scripts (e.g., `behavior_gravity.py`, `behavior_shoot.py`) that are applied to objects dynamically during runtime.

### Key Code Snippets

**Game Loop**:
The primary game loop manages the ticking of all game systems (logic, sounds, movies) and ensures smooth gameplay progression:

```python
while True:
    GameLogic.tick()
    Sounds.tick()
    Movies.tick()

    for instance in self.instances:
        instance.tick()

    if GameLogic.get_property("quit"):
        break
```

## Behaviors

The game uses a modular behavior system to manage object interactions and gameplay mechanics. Each behavior is defined in its own Python file, allowing for reusable and customizable logic that can be dynamically assigned to game objects.

### Key Behaviors:

- **`behavior_gravity.py`**: Applies gravitational force to objects, causing them to fall unless grounded.
- **`behavior_shoot.py`**: Enables shooting mechanics, allowing the player to fire projectiles at zombies.
- **`behavior_collision.py`**: Handles collision detection between objects, such as zombies and bullets.
- **`behavior_spawn_power_up.py`**: Randomly spawns power-ups when certain conditions are met, such as defeating a zombie.
- **`behavior_platform.py`**: Implements moving platform mechanics, showcased in the secret level.

Each behavior operates independently and can be attached to any object in the game. For example, a zombie object may have `behavior_gravity`, `behavior_collision`, and `behavior_highlight` assigned to it for movement, interactions, and effects.

### Example Usage:

```python
# Assigning behaviors to a game object
zombie = GameLogic.create_object("Zombie")
zombie.add_behavior(BehaviorGravity())
zombie.add_behavior(BehaviorCollision())
zombie.add_behavior(BehaviorShoot())
```

## File Structure

The project is organized into a modular structure to separate functionality and make the game easier to manage and extend. Below is an overview of the key directories and files:

- **`textures/`**: Contains image assets used for game objects such as zombies and platforms. For example:

  - `zombie.png`: The texture applied to zombie cubes.
  - `platform.png`: The texture for moving platforms.

- **`sounds/`**: Includes audio effects and background music for the game, such as:

  - Zombie growls
  - Gunfire sounds
  - Background ambiance

- **`videos/`**: Stores cinematic sequences or animations for transitions between game states (e.g., start screen or end screen).

- **`behavior_*.py`**: Modular Python scripts that define specific object behaviors, such as:

  - `behavior_gravity.py`: Applies gravity to objects.
  - `behavior_collision.py`: Manages object collisions.
  - `behavior_shoot.py`: Implements shooting mechanics.
  - `behavior_platform.py`: Adds moving platform functionality.

- **`collision.json`**: A configuration file that defines collision rules and properties for game objects.

- **`main.py`**: The entry point for the game, handling the main gameplay loop and transitions between the start screen, game logic, and end screen.

- **`game_logic.py`**: Core logic for managing game states, spawning objects, and handling player interactions.

- **`start_screen.py`**: Displays the game's start screen before gameplay begins.

- **`end_screen.py`**: Manages the end-of-game screen when the player quits or loses.

- **`level1.json`, `level2.json`**: Level files that define the layout, zombie spawn points, and object placements for each level.

- **`player_view.py`**: Handles the player's perspective, including camera movement and interactions with the environment.

- **`localize.py`**: Manages text and language localizations for game prompts and messages.

---

## How to Run

To run the game locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/zombie-survival-game.git
   ```

2. Navigate to the project folder:

```bash
cd zombie-survival-game
```

3. Run the main script:

```bash
python main.py
```

4. Enjoy the game!

## Future Enhancements

- **Improved Graphics**: Upgrade from basic cubes to detailed 3D models or sprites for zombies and objects.
- **Enhanced AI**: Introduce advanced pathfinding algorithms to make zombies smarter and more challenging.
- **New Pickups**: Add unique power-ups, such as shields, speed boosts, or explosive ammo.
- **Multiplayer Mode**: Implement cooperative or competitive multiplayer functionality.
- **Scoring System**: Include a scoreboard to track player performance and achievements.
- **Level Editor**: Provide a user-friendly interface to design custom levels with moving platforms and unique challenges.

---

## Acknowledgments

This project was developed as part of a school elective for game design. A special thanks to my instructor and advisor, **Jay Shaffstall**, for being an excellent teacher and for allowing me to take this project as an independent study when he didn’t have to. His guidance and encouragement made this project possible.

---

Feel free to explore the code, play the game, and share any feedback or suggestions!
