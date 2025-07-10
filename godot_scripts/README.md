# Godot Scripts

This directory contains GDScript files that can be used with the Light-Speed-Mod tool for Godot Engine projects.

## Weapons

### sword_wieldable.gd

A complete sword weapon system that extends CogitoWieldable. Features include:

- **Multiplayer Support**: Network-aware damage system with RPC calls
- **Stamina System**: Optional stamina consumption for attacks
- **Animation Integration**: Responds to player animation events
- **Sound Effects**: Configurable swing sounds with delay
- **Damage System**: Supports both camera collision and physics-based collision detection
- **Weapon Types**: Configurable weapon and damage types

#### Key Features:

- **Network Authority**: Automatically detects multiplayer authority
- **Animation Events**: Connects to player animation signals for responsive feedback
- **Collision Detection**: Two modes - camera-based or physics raycast
- **Damage Prevention**: Prevents self-damage and validates targets
- **Sound Management**: Delayed sound playback with RPC synchronization

#### Export Variables:

- `weapon_type`: WeaponType enum (default: BRASS_KNUCKLES)
- `damage_type`: DamageType enum (default: PROJECTILE)
- `damage_area`: Area3D node for collision detection
- `uses_stamina`: Whether to consume stamina on attack
- `stamina_cost`: Amount of stamina consumed per attack
- `use_camera_collision`: Use camera collision vs physics raycast
- `base_damage`: Base damage amount
- `swing_sound`: AudioStream for swing sound effect
- `sound_delay`: Delay in seconds before playing sound

#### Usage:

This script should be attached to a sword weapon node in your Godot project. Make sure to:

1. Set up the required Area3D for damage detection
2. Configure the weapon and damage types
3. Assign appropriate swing sounds
4. Connect to the player's animation system

#### Dependencies:

- CogitoWieldable (parent class)
- CogitoAttribute (for stamina system)
- CogitoSceneManager (for player reference)
- InventoryItemPD (for item reference)

#### Example Scene:

The `sword_wieldable.tscn` file provides a basic scene setup with:

- SwordWieldable node with script attached
- MeshInstance3D for the sword visual
- DamageArea (Area3D) for collision detection
- CollisionShape3D for the damage area
- AudioStreamPlayer3D for sound effects
- AnimationPlayer for weapon animations

The scene is pre-configured with sensible defaults and can be customized as needed.