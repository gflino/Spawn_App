import json
import random
from pathlib import Path

class GameSession:
    """
    Representa uma sessão de jogo de Zombicide.
    Esta classe carrega os dados de um ou mais arquivos de análise,
    guarda o estado atual do jogo (nível de perigo, probabilidades) e
    realiza os sorteios de inimigos.
    """

    def __init__(self, json_paths: list):
        """
        Construtor da sessão de jogo.
        """
        self.danger_level = "blue"
        self.abomination_probability = 0.03
        self.necromancer_probability = 0.06
        
        self.abomination_types = []
        self.necromancer_types = []
        self.game_data = {}
        self.game_version_name = "Unknown" 

        self._load_and_merge_data(json_paths)
        
        if json_paths:
            try:
                with open(json_paths[0], 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.game_version_name = data.get('game_version', 'Unknown')
            except (FileNotFoundError, json.JSONDecodeError):
                pass

    def _load_and_merge_data(self, json_paths: list):
        print(f"Loading data from files: {json_paths}")
        loaded_abom_files = set()
        loaded_necro_files = set()

        for path in json_paths:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                spawn_data = data.get('spawn_data', {})
                for danger_level, enemies in spawn_data.items():
                    if danger_level not in self.game_data:
                        self.game_data[danger_level] = {}
                    for enemy_name, enemy_data in enemies.items():
                        if enemy_name not in self.game_data[danger_level]:
                            self.game_data[danger_level][enemy_name] = enemy_data.copy()
                        else:
                            self.game_data[danger_level][enemy_name]['total_cards'] += enemy_data['total_cards']
                            source_dist = enemy_data['qty_distribution']
                            target_dist = self.game_data[danger_level][enemy_name]['qty_distribution']
                            for qty, count in source_dist.items():
                                target_dist[qty] = target_dist.get(qty, 0) + count
                
                special_spawns = data.get('special_spawns', {})
                for abom in special_spawns.get('abominations', []):
                    if abom.get('file_name') not in loaded_abom_files:
                        self.abomination_types.append(abom)
                        loaded_abom_files.add(abom.get('file_name'))
                for necro in special_spawns.get('necromancers', []):
                    if necro.get('file_name') not in loaded_necro_files:
                        self.necromancer_types.append(necro)
                        loaded_necro_files.add(necro.get('file_name'))

            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"WARNING: Could not process file {path}. Error: {e}")
    
    def draw_spawn(self):
        """Realiza o sorteio e retorna um dicionário com os dados brutos."""
        
        if self.abomination_types and random.random() < self.abomination_probability:
            self.abomination_probability = 0.04
            chosen_abom = random.choice(self.abomination_types)
            return {'type': 'ABOMINATION', 'data': chosen_abom}

        elif self.necromancer_types and random.random() < self.necromancer_probability:
            self.necromancer_probability = 0.06
            chosen_necro = random.choice(self.necromancer_types)
            return {'type': 'NECROMANCER', 'data': chosen_necro}
        
        else:
            current_level_data = self.game_data.get(self.danger_level)
            if not current_level_data:
                return {'type': 'ERROR', 'data': f"No spawn data for level '{self.danger_level}'."}

            enemy_types = list(current_level_data.keys())
            enemy_weights = [data['total_cards'] for data in current_level_data.values()]
            chosen_enemy_type = random.choices(enemy_types, weights=enemy_weights, k=1)[0]
            
            # Aumento de probabilidade acontece sempre nos spawns normais/eventos
            increments = {
                'yellow': {'abomination': 0.005, 'necromancer': 0.015},
                'orange': {'abomination': 0.010, 'necromancer': 0.025},
                'red':    {'abomination': 0.020, 'necromancer': 0.040}
            }
            if self.danger_level in increments:
                level_increments = increments[self.danger_level]
                self.abomination_probability += level_increments['abomination']
                self.necromancer_probability += level_increments['necromancer']

            # Verifica o tipo de spawn ANTES de retornar
            if chosen_enemy_type.startswith("extra_"):
                zombie_name = chosen_enemy_type.split('_')[1]
                return {'type': 'EXTRA_ACTIVATION', 'data': zombie_name.upper()}
            else:
                qty_data = current_level_data[chosen_enemy_type]['qty_distribution']
                quantities = [int(q) for q in qty_data.keys()]
                qty_weights = list(qty_data.values())
                chosen_quantity = random.choices(quantities, weights=qty_weights, k=1)[0]
                
                # CORREÇÃO: Lógica genérica para eventos
                if chosen_quantity == 0:
                    return {'type': 'EVENT', 'data': chosen_enemy_type}
                else:
                    return {'type': 'NORMAL_SPAWN', 'data': {'name': chosen_enemy_type, 'quantity': chosen_quantity}}

