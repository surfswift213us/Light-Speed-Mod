extends CogitoWieldable

@export var weapon_type: WeaponType = WeaponType.BRASS_KNUCKLES
@export var damage_type: DamageType = DamageType.PROJECTILE

@export_group("Sword Settings")
@export var damage_area: Area3D
@export var uses_stamina: bool = false
@export var stamina_cost: int = 4
@export var use_camera_collision: bool
@export var base_damage: float = 10.0

@export_group("Audio")
@export var swing_sound: AudioStream
@export var sound_delay: float = 0.0  # Delay in seconds before playing the sound

var trigger_has_been_pressed: bool = false
var player_stamina: CogitoAttribute = null
var network_authority: bool = false
var last_anim = ""

func _ready():
	if wieldable_mesh:
		wieldable_mesh.show()
		
	damage_area.body_entered.connect(_on_body_entered)

	if uses_stamina:
		player_stamina = grab_player_stamina_attribute()
		
	# Set up network authority
	network_authority = is_multiplayer_authority()
	print("[Sword] Ready on peer: ", multiplayer.get_unique_id())
	print("[Sword] Network authority: ", network_authority)

	# Connect to player's animation event signal
	if player_interaction_component:
		var player = player_interaction_component.get_parent()
		if player:
			player.animation_event.connect(_on_animation_event)
			print("[Sword] Connected to player animation events")

func _process(_delta):
	if not player_interaction_component:
		return
		
	var player = player_interaction_component.get_parent()
	if not player or not player.anim_player:
		return
		
	var current_anim = player.anim_player.current_animation
	if current_anim != last_anim:  # Only check when animation changes
		if current_anim == "Sword/Block" or \
		   current_anim == "Sword/RBlock" or \
		   current_anim == "Sword/BasicAttack" or \
		   current_anim == "Sword/CenterAttack" or \
		   current_anim == "Sword/LHook" or \
		   current_anim == "Sword/RHook" or \
		   current_anim == "Sword/MMAKick":
			play_swing_sound.rpc()
			print("[Sword] Playing swing sound for: ", current_anim)
		last_anim = current_anim

func _on_animation_event(event_name: String, event_data: Dictionary):
	if event_name == "Sword/Block" or \
	   event_name == "Sword/RBlock" or \
	   event_name == "Sword/BasicAttack" or \
	   event_name == "Sword/CenterAttack" or \
	   event_name == "Sword/LHook" or \
	   event_name == "Sword/RHook" or \
	   event_name == "Sword/MMAKick":
		play_swing_sound.rpc()
		print("[Sword] Playing swing sound for animation event: ", event_name)

func grab_player_stamina_attribute() -> CogitoAttribute:
	if CogitoSceneManager._current_player_node.stamina_attribute:
		return CogitoSceneManager._current_player_node.stamina_attribute
	else:
		print("Wieldable: No player stamina attribute found.")
		return null

func action_primary(_passed_item_reference:InventoryItemPD, _is_released: bool):
	if wieldable_mesh:
		wieldable_mesh.show()
		
	if _is_released:
		return
	
	if animation_player.is_playing():
		return

	if uses_stamina:
		if player_stamina.value_current < stamina_cost:
			print("Wieldable: Not enough stamina!")
			return
		else:
			player_stamina.subtract(stamina_cost)
	
	animation_player.play(anim_action_primary)
	play_swing_sound.rpc()

@rpc("any_peer", "call_local")
func play_swing_sound():
	if audio_stream_player_3d and swing_sound:
		if sound_delay > 0:
			await get_tree().create_timer(sound_delay).timeout
		audio_stream_player_3d.stream = swing_sound
		audio_stream_player_3d.play()

func _on_body_entered(collider):
	print("[Sword] Collision on peer:", multiplayer.get_unique_id(), "Collider:", collider.name)
	
	# Check if the collider is a valid target
	if not collider.has_signal("damage_received"):
		print("[Sword] Not a valid target")
		return
		
	var player = player_interaction_component.get_parent()
	
	# Prevent self-damage
	if collider == player:
		print("[Sword] Prevented self-damage!")
		return

	# Simulate attack hitting
	var hit_position: Vector3
	var hit_direction: Vector3

	if use_camera_collision:
		hit_position = player_interaction_component.Get_Camera_Collision()
		hit_direction = (hit_position - player.get_global_transform().origin).normalized()
	else:
		var space_state = damage_area.get_world_3d().direct_space_state
		var hitbox_origin = damage_area.global_transform.origin
		var ray_params = PhysicsRayQueryParameters3D.new()
		ray_params.from = hitbox_origin
		ray_params.to = collider.global_transform.origin
		var result = space_state.intersect_ray(ray_params)
		if result.size() > 0:
			hit_position = result.position
			hit_direction = (hit_position - hitbox_origin).normalized()

	# Force the RPC call
	print("[Sword] 🔥 FORCING DAMAGE RPC from peer:", multiplayer.get_unique_id())
	send_damage.rpc(base_damage, hit_direction, hit_position, collider.get_path())

@rpc("any_peer", "call_local")
func send_damage(damage: float, direction: Vector3, position: Vector3, target_path: String):
	var target = get_node_or_null(target_path)
	if not target:
		print("[Sword] Target not found")
		return
		
	print("[Sword] Processing damage on peer:", multiplayer.get_unique_id())
	
	# If target has the damage_received signal, emit it.
	if target.has_signal("damage_received"):
		print("[Sword] Emitting damage signal")
		target.damage_received.emit(damage, direction, position)
	
	# Traverse upward until we find a node that actually implements receive_damage.
	var player_node = target
	while player_node and not player_node.has_method("receive_damage"):
		player_node = player_node.get_parent()
	
	if player_node and player_node.has_method("receive_damage"):
		print("[Sword] Sending RPC to target for damage")
		# Using rpc here so that the target processes its own damage.
		player_node.rpc("receive_damage", damage)
	else:
		print("[Sword] No node with receive_damage found in hierarchy!")