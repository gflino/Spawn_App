import kivy
kivy.require('2.1.0')

import os
import json
from pathlib import Path
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen

# A importação da nossa lógica de jogo
from spawner_logic import GameSession

# --- WIDGETS CUSTOMIZADOS ---
class ImageButton(ButtonBehavior, Image):
    pass

class ClickableFloatLayout(ButtonBehavior, FloatLayout):
    pass

class DangerSelector(BoxLayout):
    pass

# --- TELAS DA APLICAÇÃO ---
class ThemeSelectScreen(Screen):
    pass

class BaseGameSelectScreen(Screen):
    def on_enter(self):
        self.load_games()

    def load_games(self):
        self.ids.options_grid.clear_widgets()
        app = App.get_running_app()
        
        json_folder = Path(__file__).parent / 'sources'
        
        available_files = [
            p for p in json_folder.glob('*.json')
            if app.get_json_metadata(p).get('theme', '').lower() == app.selected_theme.lower()
            and app.get_json_metadata(p).get('is_base_game', False)
        ]
        
        if not available_files:
            self.ids.options_grid.add_widget(Label(text=f"Nenhum jogo base encontrado para o tema '{app.selected_theme}'"))
            self.ids.next_button.disabled = True
            return

        for file_path in available_files:
            game_name = app.get_json_metadata(file_path).get('game_version', file_path.stem)
            container = BoxLayout(orientation='horizontal', size_hint_y=None, height='30dp')
            checkbox = CheckBox(size_hint_x=None, width='30dp')
            checkbox.bind(active=lambda instance, value, path=str(file_path): app.toggle_selection(path))
            label = Label(text=game_name)
            container.add_widget(checkbox)
            container.add_widget(label)
            self.ids.options_grid.add_widget(container)

class ExpansionSelectScreen(Screen):
    def on_enter(self):
        self.load_expansions()
    
    def load_expansions(self):
        self.ids.options_grid.clear_widgets()
        app = App.get_running_app()
        
        json_folder = Path(__file__).parent / 'sources'

        available_files = [
            p for p in json_folder.glob('*.json')
            if app.get_json_metadata(p).get('theme', '').lower() == app.selected_theme.lower()
            and not app.get_json_metadata(p).get('is_base_game', False)
        ]

        if not available_files:
            self.ids.options_grid.add_widget(Label(text="Nenhuma expansão encontrada."))
            return

        for file_path in available_files:
            game_name = app.get_json_metadata(file_path).get('game_version', file_path.stem)
            container = BoxLayout(orientation='horizontal', size_hint_y=None, height='30dp')
            checkbox = CheckBox(size_hint_x=None, width='30dp')
            checkbox.bind(active=lambda instance, value, path=str(file_path): app.toggle_selection(path))
            label = Label(text=game_name)
            container.add_widget(checkbox)
            container.add_widget(label)
            self.ids.options_grid.add_widget(container)

class MainGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_session = None
        self.spawn_count = 0
        
        self.base_dir = Path(__file__).parent
        self.images_path = self.base_dir / 'images'
        self.placeholder_image = self.images_path / 'placeholder.jpeg'

    def setup_game_session(self, selected_files):
        try:
            self.game_session = GameSession(selected_files)
            game_names = [Path(p).stem.replace('_', ' ').title() for p in selected_files]
            self.ids.result_label.text = f"{' + '.join(game_names)} READY!"
            print("SUCCESS: GameSession loaded.")
            self.ids.spawn_image_button.disabled = False
            self.setup_danger_selectors()
        except Exception as e:
            self.ids.result_label.text = "ERROR: FAILED TO LOAD DATA."
            print(f"ERROR LOADING GameSession: {e}")

    def draw_spawn(self):
        if not self.game_session: return

        result = self.game_session.draw_spawn()
        print(f"Draw Result: {result}")

        self.spawn_count += 1
        self.ids.spawn_counter_label.text = f'Spawn: {self.spawn_count}'
        image_to_show = str(self.placeholder_image)
        overlay_text = ""

        result_type = result.get('type')
        result_data = result.get('data')

        if result_type == 'NORMAL_SPAWN':
            enemy_name_raw = result_data['name']
            quantity = result_data['quantity']
            display_name = enemy_name_raw.replace('_', ' ').title()
            self.ids.result_label.text = f'{display_name.upper()} X{quantity}'
            image_path = self.images_path / f"{enemy_name_raw}.jpeg"
            if os.path.exists(image_path):
                image_to_show = str(image_path)
            else:
                overlay_text = display_name.upper()
                print(f"Warning: Image not found: '{image_path}'")
        
        elif result_type in ['ABOMINATION', 'NECROMANCER']:
            display_name = result_data['display_name']
            file_name = result_data['file_name']
            self.ids.result_label.text = f"{display_name.upper()}!"
            threat_image = self.images_path / f'{file_name}.jpeg'
            if os.path.exists(threat_image):
                image_to_show = str(threat_image)
            else:
                overlay_text = display_name.upper()
                print(f"Warning: Threat image not found. Expected: '{threat_image}'")
        
        elif result_type == 'EXTRA_ACTIVATION':
            self.ids.result_label.text = f"EXTRA ACTIVATION: {result_data}"
            overlay_text = f"EXTRA\nACTIVATION:\n{result_data}"
            event_image_path = self.images_path / 'extra_activation.jpeg'
            if os.path.exists(event_image_path):
                image_to_show = str(event_image_path)
            else:
                print(f"Warning: Generic event image not found: '{event_image_path}'")

        elif result_type == 'EVENT':
            event_name = result_data.replace('_', ' ').upper()
            self.ids.result_label.text = event_name
            overlay_text = event_name
            event_image_path = self.images_path / 'event.jpeg'
            if os.path.exists(event_image_path):
                image_to_show = str(event_image_path)
            else:
                print(f"Warning: Generic event image not found: '{event_image_path}'")
        
        self.ids.spawn_image.source = image_to_show
        self.ids.overlay_label.text = overlay_text

    def set_danger_level(self, level: str):
        if self.game_session:
            self.game_session.danger_level = level
            print(f"Danger level changed to: {level}")
            
    def setup_danger_selectors(self):
        danger_levels = {'Blue': 'blue', 'Yellow': 'yellow', 'Orange': 'orange', 'Red': 'red'}
        container = self.ids.danger_selectors_container
        container.clear_widgets()
        for text, value in danger_levels.items():
            item = DangerSelector()
            checkbox = CheckBox(group='danger_level', active=(value == 'blue'), size_hint_x=None, width=24)
            checkbox.bind(active=lambda instance, is_active, lvl=value: self.set_danger_level(lvl) if is_active else None)
            label = Label(text=text)
            item.add_widget(checkbox)
            item.add_widget(label)
            container.add_widget(item)

    def reset_game(self):
        self.game_session = None
        self.spawn_count = 0
        self.ids.spawn_counter_label.text = 'Spawn: 0'
        self.ids.result_label.text = 'Select theme to start...'
        self.ids.spawn_image.source = str(self.placeholder_image)
        self.ids.overlay_label.text = ''
        self.ids.spawn_image_button.disabled = True
        self.ids.danger_selectors_container.clear_widgets()
        print("Game session reset.")

class SpawnerApp(App):
    def build(self):
        Window.clearcolor = (0.1, 0.1, 0.1, 1)
        # O ScreenManager é o widget raiz
        self.sm = ScreenManager()
        self.sm.add_widget(ThemeSelectScreen(name='theme_select'))
        self.sm.add_widget(BaseGameSelectScreen(name='base_game_select'))
        self.sm.add_widget(ExpansionSelectScreen(name='expansion_select'))
        self.sm.add_widget(MainGameScreen(name='main_game'))
        return self.sm

    def on_start(self):
        self.selected_theme = ""
        self.selected_files = []
    
    def go_to_theme_select(self):
        self.sm.get_screen('main_game').reset_game()
        self.sm.current = 'theme_select'
    
    def select_theme(self, theme):
        self.selected_theme = theme
        self.selected_files = []
        self.sm.get_screen('base_game_select').ids.next_button.disabled = True
        self.sm.current = 'base_game_select'
        print(f"Theme selected: {theme}")
    
    def get_json_metadata(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Erro ao ler metadados do ficheiro {file_path.name}: {e}")
            return {}

    def toggle_selection(self, path):
        if path in self.selected_files:
            self.selected_files.remove(path)
        else:
            self.selected_files.append(path)
        
        if self.sm.current == 'base_game_select':
            self.sm.get_screen('base_game_select').ids.next_button.disabled = not self.selected_files
        print(f"Selected files: {self.selected_files}")
    
    def start_game(self):
        main_screen = self.sm.get_screen('main_game')
        main_screen.reset_game()
        main_screen.setup_game_session(self.selected_files)
        self.sm.current = 'main_game'

if __name__ == '__main__':
    Config.set('graphics', 'width', '360')
    Config.set('graphics', 'height', '780')
    SpawnerApp().run()

