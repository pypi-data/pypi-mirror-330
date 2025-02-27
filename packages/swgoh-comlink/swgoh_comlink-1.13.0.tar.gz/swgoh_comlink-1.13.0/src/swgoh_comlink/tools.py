"""
Collection of tools to help with common data mining and organization
"""

from __future__ import absolute_import, annotations

from typing import Any, Tuple, Dict, List, Union


class BattleEffects(dict):

    def __getitem__(self, key):
        return super().get(key, [])


def get_playable_units(game_data: Union[Dict[Any, Any], List[dict]]) -> Tuple[List[dict], List[dict]]:
    """Return tuple of lists containing the playable characters and ships from game data

        Args
            game_data: Either the full dictionary of game data collections or list of game_data['units'] collection

        Returns
            tuple of lists containing playable characters and ships. (chars, ships)

        Raises
            ValueError if game_data is not type dict or list
    """
    units = []
    if isinstance(game_data, dict):
        if 'units' in game_data:
            units = game_data['units']
    elif isinstance(game_data, list):
        units = game_data
    else:
        raise ValueError(f"'game_data' must be either type: dict or type: list, not type: {type(game_data)}")

    playable_chars = [unit for unit in units if unit['obtainable'] and unit['rarity'] == 7 and unit['obtainableTime'] == '0' and unit['combatType'] == 1]
    playable_ships = [unit for unit in units if unit['obtainable'] and unit['rarity'] == 7 and unit['obtainableTime'] == '0' and unit['combatType'] == 2]

    return playable_chars, playable_ships

def tag_ability_game_mode(abilities: list, effects: list) -> tuple:
    """Parse unit abilities and tag those that are only available in specific game modes. Return a dictionary
    with game mode keys and values of lists of ability IDs
    """
    query_battle_effects = BattleEffects()

    for effect in effects:
        if 'query_battle_type' in effect['id']:
            query_battle_effects[effect['id']] = []

    ability_ids = []
    seen_abilities = set()

    def track_ability(ability_id: str, effect_id: str):
        if ability_id not in seen_abilities:
            seen_abilities.add(ability_id)
            ability_ids.append(ability_id)
            query_battle_effects[effect_id].append(ability_id)

    for ability in abilities:
        if ('effectReference' in ability and
                isinstance(ability['effectReference'], list) and
                len(ability['effectReference']) > 0):
            for effect_ref in ability['effectReference']:
                if 'query_battle_effect' in effect_ref['id']:
                    track_ability(ability['id'], effect_ref['id'])
        if ('tier' in ability and
                isinstance(ability['tier'], list) and
                len(ability['tier']) > 0):
            for tier in ability['tier']:
                if ('effectReference' in tier and
                        isinstance(tier['effectReference'], list) and
                        len(tier['effectReference']) > 0):
                    for effect_ref in tier['effectReference']:
                        if 'query_battle_type' in effect_ref['id']:
                            # Track tier['descKey'] ?
                            track_ability(ability['id'], effect_ref['id'])

    return ability_ids, query_battle_effects
