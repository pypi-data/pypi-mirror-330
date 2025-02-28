import math
from typing import Dict, List, Literal

import jax
import jax.numpy as jnp
import numpy as np
from craftax.craftax.constants import *
from craftax.craftax.craftax_state import EnvState
from craftax.craftax_classic.renderer import render_craftax_pixels
from craftax.craftax_env import make_craftax_env_from_name

from craftaxlm.classic.metadata import (
    CRAFTAX_CLASSIC_ACHIEVEMENTS,
    CRAFTAX_CLASSIC_ACTION_MAPPING,
)
from craftaxlm.classic.state import (
    CraftaxClassicState,
    CraftaxRecorder,
    mob_id_to_name,
    player_chars,
    render_craftax_classic_text_custom,
)
from craftaxlm.shared import CraftaxBaseACI


class CraftaxClassicACI(CraftaxBaseACI):
    formatting: Literal["md", "xml"] = "md"
    map_format: Literal["full", "compact"] = "full"
    vantage: int = 3

    def __init__(
        self, formatting="md", map_format="full", vantage=3, verbose=False, seed=None
    ):
        self.formatting = formatting
        self.map_format = map_format
        self.vantage = vantage
        self.verbose = verbose
        self.achievement_deltas = []
        super().__init__(seed=seed)

    def make_env(self):
        return make_craftax_env_from_name(
            "Craftax-Classic-Symbolic-v1", auto_reset=False
        )

    def create_starting_obs(self):
        step_info = self.create_step_info(self.state, 0.0, False)
        return {
            "state_image": step_info["state_image"],
            "state_text": step_info["state_text"],
            "reward": 0.0,
            "done": False,
        }

    def map_action_string_to_int(self, action_string: str) -> int:
        return CRAFTAX_CLASSIC_ACTION_MAPPING.get(action_string.lower(), 0)

    def get_achievements(self, state):
        return {
            "achievements": {
                k: state.achievements[i]
                for i, k in CRAFTAX_CLASSIC_ACHIEVEMENTS.items()
            }
        }

    def get_achievement_delta(self, achievements):
        """
        Calculate which achievements have been newly unlocked.

        Args:
            achievements: Dictionary of current achievements

        Returns:
            Dictionary of newly unlocked achievements or None if no new achievements
        """
        if not hasattr(self, "last_achievements"):
            self.last_achievements = {
                "achievements": {k: 0 for k in achievements["achievements"].keys()}
            }
            return None

        # Find new achievements (changed from 0 to 1)
        delta = {}
        for k, v in achievements["achievements"].items():
            if v > 0 and self.last_achievements["achievements"].get(k, 0) == 0:
                delta[k] = v

        # Update last_achievements
        self.last_achievements = achievements

        # Return None if no new achievements
        if not delta:
            return None

        return {"new_achievements": delta}

    def create_step_info(self, state, reward, done):
        craftaxlm_state = render_craftax_classic_text_custom(
            state, vantage=self.vantage
        )
        return {
            "state_image": craftaxlm_state.image,
            "state_text": craftaxlm_state.render_to_text_simple(
                verbose=self.verbose,
                formatting=self.formatting,
                map_format=self.map_format,
            ),
            "reward": float(reward),
            "done": bool(done),
        }

    def accept_tool_call(self, tool_call):
        """
        Accepts an OpenAI SDK-like tool call and executes the corresponding action.

        Args:
            tool_call: A dictionary with the structure similar to OpenAI tool calls:
                {
                    "type": "function",
                    "function": {
                        "name": "take_action",
                        "arguments": {
                            "action": "up" | "down" | "left" | "right" | etc.
                        }
                    },
                    "id": "call_abc123" # optional tool call ID
                }

        Returns:
            Dictionary formatted as an OpenAI tool message response:
            {
                "role": "tool",
                "content": JSON string with state information,
                "tool_call_id": The ID of the tool call being responded to
            }
        """
        state_before = self.state

        # Extract action from tool call
        action = None
        tool_call_id = None

        if isinstance(tool_call, str):
            # Handle legacy string action format
            action = tool_call
        elif isinstance(tool_call, dict):
            # Extract action from OpenAI SDK-like tool call format
            if "id" in tool_call:
                tool_call_id = tool_call["id"]

            if "function" in tool_call:
                function_data = tool_call["function"]
                if "arguments" in function_data:
                    arguments = function_data["arguments"]
                    # Handle both string and dict arguments
                    if isinstance(arguments, str):
                        import json

                        try:
                            arguments = json.loads(arguments)
                        except json.JSONDecodeError:
                            action = arguments

                    if isinstance(arguments, dict) and "action" in arguments:
                        action = arguments["action"]

        if action is None:
            raise ValueError(f"Could not extract action from tool call: {tool_call}")

        # Map action string to integer and execute
        action_int = self.map_action_string_to_int(action)
        _, state, reward, done, info = self.env.step(
            self.rngs[2], state_before, action_int, self.env_params
        )
        self.state = state

        # Calculate achievement deltas
        achievements = self.get_achievements(state)
        achievement_delta = self.get_achievement_delta(achievements)

        # Store achievement deltas if the attribute exists
        if hasattr(self, "achievement_deltas"):
            self.achievement_deltas.append(achievement_delta)

        # Print if verbose mode is enabled
        if achievement_delta and hasattr(self, "verbose") and self.verbose:
            print(achievement_delta)

        step_info = self.create_step_info(state, reward, done)
        updates, expectation = get_action_result_vs_expectation(
            state_before, state, action
        )

        # Format response as an OpenAI tool message
        import base64
        import io
        import json

        import numpy as np
        from PIL import Image

        # Convert numpy array to base64 for OpenAI compatibility
        state_image = step_info.pop("state_image")  # Remove image from step_info

        # Convert numpy array to PIL Image and then to bytes
        pil_image = Image.fromarray(state_image)
        buffer = io.BytesIO()
        pil_image.save(buffer, format="PNG")

        # Get base64 encoded string
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Format as OpenAI compatible image object
        image_obj = {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{img_str}"},
        }

        response_content = {
            "direct_results": updates,
            "expected_results": expectation,
            "state": step_info,
            "state_image": image_obj,
        }

        # Include achievement delta if available
        if achievement_delta:
            response_content["achievement_delta"] = achievement_delta

        response = {
            "role": "tool",
            "content": json.dumps(response_content),
        }

        # Add tool_call_id if it was provided
        if tool_call_id:
            response["tool_call_id"] = tool_call_id

        return response

    def step_action(self, action_string, tool_call_id=None):
        """
        Helper method to perform an action using the OpenAI tool call format.

        Args:
            action_string: String representation of the action to take
            tool_call_id: Optional ID for the tool call

        Returns:
            Dictionary formatted as an OpenAI tool message response
        """
        # Create a tool call in OpenAI format
        tool_call = {
            "type": "function",
            "function": {"name": "take_action", "arguments": {"action": action_string}},
        }

        # Add tool_call_id if provided
        if tool_call_id:
            tool_call["id"] = tool_call_id

        # Process the tool call
        return self.accept_tool_call(tool_call)


def render_craftax_text(state):
    """Renders the CraftAX Classic state as text representation."""
    obs_dim_array = jnp.array([OBS_DIM[0], OBS_DIM[1]], dtype=jnp.int32)

    # Map
    padded_grid = jnp.pad(
        state.map,
        (MAX_OBS_DIM + 2, MAX_OBS_DIM + 2),
        constant_values=BlockType.OUT_OF_BOUNDS.value,
    )

    tl_corner = state.player_position - obs_dim_array // 2 + MAX_OBS_DIM + 2
    map_view = jax.lax.dynamic_slice(padded_grid, tl_corner, OBS_DIM)

    # Convert blocks to text representation
    block_chars = {
        BlockType.INVALID.value: ".",
        BlockType.OUT_OF_BOUNDS.value: "#",
        BlockType.GRASS.value: "G",
        BlockType.WATER.value: "~",
        BlockType.STONE.value: "S",
        BlockType.TREE.value: "T",
        BlockType.WOOD.value: "W",
        BlockType.PATH.value: "P",
        BlockType.COAL.value: "C",
        BlockType.IRON.value: "I",
        BlockType.DIAMOND.value: "D",
        BlockType.CRAFTING_TABLE.value: "B",  # B for crafting Bench
        BlockType.FURNACE.value: "F",
        BlockType.SAND.value: "_",
        BlockType.LAVA.value: "L",
        BlockType.PLANT.value: "p",
        BlockType.RIPE_PLANT.value: "r",
        BlockType.WALL.value: "X",
        BlockType.DARKNESS.value: " ",
        BlockType.WALL_MOSS.value: "M",
        BlockType.STALAGMITE.value: "^",
        BlockType.SAPPHIRE.value: "$",
        BlockType.RUBY.value: "R",
        BlockType.CHEST.value: "H",
        BlockType.FOUNTAIN.value: "O",
        BlockType.FIRE_GRASS.value: "f",
        BlockType.ICE_GRASS.value: "i",
        BlockType.GRAVEL.value: "g",
        BlockType.FIRE_TREE.value: "t",
        BlockType.ICE_SHRUB.value: "s",
        BlockType.ENCHANTMENT_TABLE_FIRE.value: "E",
        BlockType.ENCHANTMENT_TABLE_ICE.value: "e",
        BlockType.NECROMANCER.value: "N",
        BlockType.GRAVE.value: "v",
        BlockType.GRAVE2.value: "V",
        BlockType.GRAVE3.value: "u",
        BlockType.NECROMANCER_VULNERABLE.value: "n",
    }

    # Create text grid - swap x and y to match game coordinates
    height, width = map_view.shape
    text_grid = []
    for y in range(height):
        row = []
        for x in range(width):
            block_value = int(map_view[y, x])
            row.append(block_chars.get(block_value, "?"))
        text_grid.append(row)

    # Add player at center
    center_y, center_x = obs_dim_array // 2
    player_direction = int(state.player_direction)
    # print("Player direction: ", player_direction)
    text_grid[center_y][center_x] = player_chars.get(player_direction, "P")

    # print("Player char: ", text_grid[center_y][center_x])
    # Add mobs - ensure coordinates are properly aligned
    def add_mob_to_grid(mob_positions, mob_masks, symbol):
        for pos, mask in zip(mob_positions, mob_masks):
            if not mask:
                continue
            # Calculate local position relative to player
            local_pos = pos - state.player_position + obs_dim_array // 2
            # Check if mob is within visible area
            if (local_pos >= 0).all() and (local_pos < obs_dim_array).all():
                y, x = int(local_pos[0]), int(local_pos[1])
                text_grid[y][x] = symbol

    add_mob_to_grid(state.zombies.position, state.zombies.mask, "Z")
    add_mob_to_grid(state.cows.position, state.cows.mask, "c")
    add_mob_to_grid(state.skeletons.position, state.skeletons.mask, "K")
    add_mob_to_grid(state.arrows.position, state.arrows.mask, "a")

    # Convert to string - join rows in correct order
    text_map = "\n".join("".join(row) for row in text_grid)

    return text_map


compact_map_translation_full = {
    # Basic blocks
    "G": "Grass",
    "~": "Water",
    "S": "Stone",
    "T": "Tree",
    "W": "Wood",
    "P": "Path",
    "C": "Coal",
    "I": "Iron",
    "D": "Diamond",
    "B": "Crafting Bench",
    "F": "Furnace",
    "E": "Enchantment Table Fire",
    "e": "Enchantment Table Ice",
    # Additional blocks
    "_": "Sand",
    "L": "Lava",
    "p": "Plant",
    "r": "Ripe Plant",
    "X": "Wall",
    " ": "Darkness",
    "M": "Wall Moss",
    "^": "Stalagmite",
    "$": "Sapphire",
    "R": "Ruby",
    "H": "Chest",
    "O": "Fountain",
    # Special terrain
    "f": "Fire Grass",
    "i": "Ice Grass",
    "g": "Gravel",
    "t": "Fire Tree",
    "s": "Ice Shrub",
    # Necromancer and graves
    "N": "Necromancer",
    "n": "Necromancer Vulnerable",
    "v": "Grave",
    "V": "Grave2",
    "u": "Grave3",
    # Mobs
    "Z": "Zombie",
    "c": "Cow",
    "K": "Skeleton",
    "a": "Arrow",
    # Boundaries
    ".": "Invalid",
    "#": "Out of Bounds",
}

compact_map_translation_classic = {
    # Basic blocks
    "G": "Grass",
    "~": "Water",
    "S": "Stone",
    "T": "Tree",
    "W": "Wood",
    "P": "Path",
    "C": "Coal",
    "I": "Iron",
    "D": "Diamond",
    "B": "Crafting Bench",
    "F": "Furnace",
    "E": "Enchantment Table Fire",
    "e": "Enchantment Table Ice",
    # Additional blocks
    "_": "Sand",
    "L": "Lava",
    "p": "Plant",
    "r": "Ripe Plant",
    "X": "Wall",
    # Mobs
    "Z": "Zombie",
    "c": "Cow",
    "K": "Skeleton",
    "a": "Arrow",
    # Boundaries
    ".": "Invalid",
    "#": "Out of Bounds",
}


def render_craftax_classic_text_exp(
    state: EnvState, enable_recording=False, vantage=3
) -> CraftaxClassicState:
    print("Exp")
    map_data = []
    for x in range(state.map.shape[0]):
        for y in range(state.map.shape[1]):
            if (
                not max(
                    abs(x - state.player_position[0]), abs(y - state.player_position[1])
                )
                <= 4
            ):
                continue
            tile = {
                "position": {
                    "x": x - state.player_position[0],
                    "y": y - state.player_position[1],
                },
                "visible": max(
                    abs(x - state.player_position[0]), abs(y - state.player_position[1])
                )
                <= 4,
                "block": BlockType(state.map[x, y]).name.lower(),
            }
            if state.mob_map[x, y].max() > 0.5:
                tile["mob"] = mob_id_to_name(state.mob_map[x, y].argmax())
            map_data.append(tile)
    text_map = render_craftax_text(state)

    inventory_data = {
        "resources": {
            "wood": int(state.inventory.wood),
            "stone": int(state.inventory.stone),
            "coal": int(state.inventory.coal),
            "iron": int(state.inventory.iron),
            "diamond": int(state.inventory.diamond),
            "sapling": int(state.inventory.sapling),
        },
        "tools": {},
    }

    inventory_data["tools"]["pickaxe"] = {
        "wood": int(state.inventory.wood_pickaxe),
        "stone": int(state.inventory.stone_pickaxe),
        "iron": int(state.inventory.iron_pickaxe),
    }

    inventory_data["tools"]["sword"] = {
        "wood": int(state.inventory.wood_sword),
        "stone": int(state.inventory.stone_sword),
        "iron": int(state.inventory.iron_sword),
    }

    player_data = {
        "health": int(state.player_health),
        "food": int(state.player_food),
        "drink": int(state.player_drink),
        "energy": int(state.player_energy),
        "direction_facing": Action(state.player_direction).name.lower(),
    }

    environment_data = {
        "light_level": float(state.light_level),
        "is_sleeping": bool(state.is_sleeping),
        "floor": 0,  # Hardcode to 0 since player_level isn't in EnvState
    }

    def to_json_friendly(data):
        if isinstance(data, dict):
            return {key: to_json_friendly(value) for key, value in data.items()}
        elif isinstance(data, (list, tuple)):
            return [to_json_friendly(item) for item in data]
        elif isinstance(data, (jnp.ndarray, np.ndarray)):
            if data.ndim == 0:
                return data.item()
            return [to_json_friendly(item) for item in data]
        elif isinstance(data, (jnp.bool_, np.bool_)):
            return bool(data)
        elif isinstance(data, (jnp.integer, np.integer)):
            return int(data)
        elif isinstance(data, (jnp.floating, np.floating)):
            return float(data)
        else:
            return data

    pixels = render_craftax_pixels(state, BLOCK_PIXEL_SIZE_HUMAN)
    # Convert from JAX array to numpy and ensure uint8 format
    frame = np.array(pixels).astype(np.uint8)

    craftax_state = CraftaxClassicState(
        map_full=to_json_friendly(map_data),
        map_compact=text_map,
        inventory=to_json_friendly(inventory_data),
        player=to_json_friendly(player_data),
        environment=to_json_friendly(environment_data),
        image=frame,
        recorder=None if not enable_recording else CraftaxRecorder(),
        vantage=vantage,
    )

    # Record frame if recording is enabled
    if enable_recording:
        craftax_state.recorder.record_frame(state)

    return craftax_state


def canonical_crafter_score_classic(achievements_by_run: List[Dict]):
    assert all(
        isinstance(achievements, dict)
        and all(
            k in achievements
            for k in [
                "Collect Wood",
                "Place Table",
                "Eat Cow",
                "Collect Sapling",
                "Collect Drink",
                "Make Wood Pickaxe",
                "Make Wood Sword",
                "Place Plant",
                "Defeat Zombie",
                "Collect Stone",
                "Place Stone",
                "Eat Plant",
                "Defeat Skeleton",
                "Make Stone Pickaxe",
                "Make Stone Sword",
                "Wake Up",
                "Place Furnace",
                "Collect Coal",
                "Collect Iron",
                "Collect Diamond",
                "Make Iron Pickaxe",
                "Make Iron Sword",
            ]
        )
        and all(isinstance(v, int) for v in achievements.values())
        for achievements in achievements_by_run
    )
    successes_by_achievement = {
        achievement: sum(1 for run in achievements_by_run if run[achievement] > 0)
        for achievement in achievements_by_run[0].keys()
    }
    success_rates = [
        count / len(achievements_by_run) for count in successes_by_achievement.values()
    ]

    # Compute the Crafter score: S = exp((1/N)*sum(ln(1 + s_i))) - 1, where s_i is the success rate for achievement i.
    N = len(success_rates)
    return math.exp(sum(math.log(1 + s) for s in success_rates) / N) - 1


CRAFTAX_CLASSIC_ACTION_MAPPING = {
    "noop": 0,
    "left": 1,
    "right": 2,
    "up": 3,
    "down": 4,
    "do": 5,
    "sleep": 6,
    "place_stone": 7,
    "place_table": 8,
    "place_furnace": 9,
    "place_plant": 10,
    "make_wood_pickaxe": 11,
    "make_stone_pickaxe": 12,
    "make_iron_pickaxe": 13,
    "make_wood_sword": 14,
    "make_stone_sword": 15,
    "make_iron_sword": 16,
}


def get_action_expectations():
    """
    Returns a dictionary containing the required and optional expected results
    for each valid action in CraftAx Classic, using parametric inventory format.
    """
    expectations = {
        "noop": {"required": [], "optional": []},
        "left": {"required": ["move_left"], "optional": ["turn_left"]},
        "right": {"required": ["move_right"], "optional": ["turn_right"]},
        "up": {"required": ["move_up"], "optional": ["turn_up"]},
        "down": {"required": ["move_down"], "optional": ["turn_down"]},
        "do": {
            "required": [],
            "optional": [
                "stone_k->[k+1]",
                "wood_k->[k+1]",
                "coal_k->[k+1]",
                "iron_k->[k+1]",
                "diamond_k->[k+1]",
                "stone_removed",
                "tree_removed",
                "coal_removed",
                "iron_removed",
                "diamond_removed",
                "zombie_removed",
                "skeleton_removed",
            ],
        },
        "sleep": {"required": [], "optional": ["time_night->day", "health_low->full"]},
        "place_stone": {"required": ["stone_k->[k-1]", "stone_added"], "optional": []},
        "place_table": {
            "required": ["wood_k->[k-2]", "crafting_table_added"],
            "optional": [],
        },
        "place_furnace": {
            "required": ["stone_k->[k-8]", "furnace_added"],
            "optional": [],
        },
        "place_plant": {"required": ["plant_k->[k-1]", "plant_added"], "optional": []},
        "make_wood_pickaxe": {
            "required": ["wood_k->[k-3]", "stick_k->[k-2]", "wood_pickaxe_k->[k+1]"],
            "optional": [],
        },
        "make_stone_pickaxe": {
            "required": ["stone_k->[k-3]", "stick_k->[k-2]", "stone_pickaxe_k->[k+1]"],
            "optional": [],
        },
        "make_iron_pickaxe": {
            "required": ["iron_k->[k-3]", "stick_k->[k-2]", "iron_pickaxe_k->[k+1]"],
            "optional": [],
        },
        "make_wood_sword": {
            "required": ["wood_k->[k-2]", "stick_k->[k-1]", "wood_sword_k->[k+1]"],
            "optional": [],
        },
        "make_stone_sword": {
            "required": ["stone_k->[k-2]", "stick_k->[k-1]", "stone_sword_k->[k+1]"],
            "optional": [],
        },
        "make_iron_sword": {
            "required": ["iron_k->[k-2]", "stick_k->[k-1]", "iron_sword_k->[k+1]"],
            "optional": [],
        },
    }

    return expectations


def get_action_expectation(action):
    """
    Returns the expected results for a specific action.

    Args:
        action: String name or integer ID of the action

    Returns:
        Dictionary with 'required' and 'optional' effects
    """
    expectations = get_action_expectations()

    # Handle case where action is passed as an integer ID
    if isinstance(action, int):
        for name, id in CRAFTAX_CLASSIC_ACTION_MAPPING.items():
            if id == action:
                action = name
                break

    if action in expectations:
        return expectations[action]
    else:
        return {"required": [], "optional": []}


def get_action_result(state_before, state_after):
    # updates = {}

    # Position
    updates = []
    player_position_before = state_before.player_position
    player_position_after = state_after.player_position
    print("Player position before: ", player_position_before)
    print("Player position after: ", player_position_after)
    if not all(player_position_before[i] == player_position_after[i] for i in range(2)):
        if player_position_before[0] < player_position_after[0]:
            updates.append("move_down")
        elif player_position_before[0] > player_position_after[0]:
            updates.append("move_up")
        elif player_position_before[1] < player_position_after[1]:
            updates.append("move_right")
        elif player_position_before[1] > player_position_after[1]:
            updates.append("move_left")
    else:
        print("Player position is the same")

    # Direction
    direction_dict = {
        3: "up",
        4: "down",
        1: "left",
        2: "right",
    }
    player_direction_before = state_before.player_direction
    player_direction_after = state_after.player_direction
    if player_direction_before != player_direction_after:
        print(player_direction_after)
        updates.append("turn_" + direction_dict[int(player_direction_after)])

    # Inventory
    craftax_state_before = render_craftax_classic_text_custom(state_before, vantage=3)
    craftax_state_after = render_craftax_classic_text_custom(state_after, vantage=3)
    for k in craftax_state_before.inventory.keys():
        if craftax_state_before.inventory[k] != craftax_state_after.inventory[k]:
            updates.append(
                k
                + "_"
                + str(state_after.inventory[k])
                + "->"
                + str(state_after.inventory[k])
            )

    # Map
    # If these are removed, show it: stone, tree, coal, iron, diamond, zombie, skeleton
    # If these are added, show it: crafting_table, furnace
    if all(player_position_before[i] == player_position_after[i] for i in range(2)):
        for tile in craftax_state_before.map_full:
            if tile["block"] in [
                "stone",
                "tree",
                "coal",
                "iron",
                "diamond",
                "zombie",
                "skeleton",
            ]:
                if tile not in craftax_state_after.map_full:
                    updates.append(tile["block"] + "_removed")
            if tile["block"] in ["crafting_table", "furnace"]:
                if tile not in craftax_state_after.map_full:
                    updates.append(tile["block"] + "_added")
    return updates


def get_action_result_vs_expectation(state_before, state_after, action):
    updates = get_action_result(state_before, state_after)
    expectation = get_action_expectation(action)
    return updates, expectation


if __name__ == "__main__":
    import json
    craftax_aci = CraftaxClassicACI(
        formatting="md", map_format="full", verbose=True, seed=0
    )
    craftax_aci.reset()

    # Example 1: Using direct step calls (old way)
    print("EXAMPLE 1: Using direct step calls")
    state_before = craftax_aci.state
    action_int = craftax_aci.map_action_string_to_int("down")
    print("Action int: ", action_int)
    _, state, reward, done, info = craftax_aci.env.step(
        craftax_aci.rngs[2], state_before, action_int, craftax_aci.env_params
    )
    updates, expected_updates = get_action_result_vs_expectation(
        state_before, state, action_int
    )
    craftax_aci.state = state  # Make sure to update the state
    print("Updates:", updates)
    print("Expected:", expected_updates)

    # Example 2: Using the new step_action method
    print("\nEXAMPLE 2: Using step_action method")
    response = craftax_aci.step_action("down", tool_call_id="action_123")
    print("Tool Role:", response["role"])
    print("Tool Call ID:", response.get("tool_call_id"))

    content = json.loads(response["content"])
    print("Achievement Delta:", content.get("achievement_delta"))

    # Let's try to trigger an achievement
    print("\nTrying to trigger an achievement...")

    # Find a tree and try to collect wood (multiple steps to demonstrate)
    # First, look around for a tree
    directions = ["up", "right", "down", "left"]
    for direction in directions:
        print(f"\nChecking {direction} direction...")
        response = craftax_aci.step_action(direction)
        content = json.loads(response["content"])

        # See if we're facing a tree
        state_text = content["state"]["state_text"]
        if "Tree" in state_text and "Object_you_are_facing" in state_text:
            print(f"Found a tree! Attempting to collect wood...")
            # Use the 'do' action to collect wood
            response = craftax_aci.step_action("do")
            content = json.loads(response["content"])
            print("Action results:", content["direct_results"])

            # Check if we got an achievement
            if content.get("achievement_delta"):
                print("Achievement unlocked:", content["achievement_delta"])
            break

    # Example 3: Using accept_tool_call with OpenAI format
    print("\nEXAMPLE 3: Using accept_tool_call with OpenAI format")
    tool_call = {
        "type": "function",
        "function": {"name": "take_action", "arguments": {"action": "up"}},
        "id": "call_abc123",
    }
    response = craftax_aci.accept_tool_call(tool_call)
    print("Tool Role:", response["role"])
    print("Tool Call ID:", response.get("tool_call_id"))

    # Parse and display content for better readability
    import json

    content = json.loads(response["content"])
    print("\nResults:")
    print("Direct Results:", content["direct_results"])
    print("Expected Results:", content["expected_results"])
    print("Achievement Delta:", content.get("achievement_delta"))

    # Verify image format is correct
    image_data = content["state_image"]
    print("\nImage Data Format:")
    print(f"Type: {image_data['type']}")
    print(f"URL prefix: {image_data['image_url']['url'][:30]}...")

    # Optional: Save the image to a file to verify it works
    import base64

    try:
        # Extract base64 data
        base64_data = image_data["image_url"]["url"].split(",")[1]
        # Decode and save
        with open("test_output_image.png", "wb") as f:
            f.write(base64.b64decode(base64_data))
        print("\nImage saved to test_output_image.png")
    except Exception as e:
        print(f"Error saving image: {e}")

    # Show all accumulated achievement deltas
    print("\nAll Achievement Deltas:")
    for i, delta in enumerate(craftax_aci.achievement_deltas):
        if delta:
            print(f"Step {i+1}:", delta)
