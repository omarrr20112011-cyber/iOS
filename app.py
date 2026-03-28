import ui
import time
import urllib.parse
import webbrowser
import console 
import clipboard 
import json
import os

# --- НАСТРОЙКИ ---
BG_COLOR = '#090a0f'          
TABBAR_BG = '#050508'         
SEARCH_BG = (1, 1, 1, 0.08)    
TEXT_COLOR = '#ffffff'
SUBTEXT_COLOR = '#8a8d9e'

SUPPORT_EMAIL = 'tvoya.pochta@gmail.com' 
LOGO_IMAGE_NAME = 'logo.png' 
SAVE_FILE = 'my_library.json' # Файл для локального сохранения библиотеки

# СТРОГИЕ НЕОНОВЫЕ ЦВЕТА
BLUE_NEON = '#00e5ff'   # Для IPA
GREEN_NEON = '#00ff66'  # Для APK
RED_NEON = '#ff2a2a'    # Для OTHER

MAX_PROFILE_PHOTOS = 3 

# БАЗА ПРИЛОЖЕНИЙ
ALL_FILES = [
    {
        'name': 'Free Slot', 'file_name': 'free', 'color': 'white', 
        'avatar': 'empty.png', 'type': 'Остальное', 'category': 'Остальное', 'sub_category': 'Остальное', 'version': 'v0 (beta)',
        'developer': 'you', 'size': '1488 MB',
        'description': 'Бесплатный слот для вашего приложения',
        'screenshots': [],
        'link': ''
    },
    {
        'name': 'Free Slot', 'file_name': 'free', 'color': 'white', 
        'avatar': 'empty.png', 'type': 'Остальное', 'category': 'Остальное', 'sub_category': 'Остальное', 'version': 'v0 (beta)',
        'developer': 'you', 'size': '1488 MB',
        'description': 'Бесплатный слот для вашего приложения',
        'screenshots': [],
        'link': ''
    },
    {
        'name': 'Free Slot', 'file_name': 'free', 'color': 'white', 
        'avatar': 'empty.png', 'type': 'Остальное', 'category': 'Остальное', 'sub_category': 'Остальное', 'version': 'v0 (beta)',
        'developer': 'you', 'size': '1488 MB',
        'description': 'Бесплатный слот для вашего приложения',
        'screenshots': [],
        'link': ''
    },
    {
        'name': 'Free Slot', 'file_name': 'free', 'color': 'white', 
        'avatar': 'empty.png', 'type': 'Остальное', 'category': 'Остальное', 'sub_category': 'Остальное', 'version': 'v0 (beta)',
        'developer': 'you', 'size': '1488 MB',
        'description': 'Бесплатный слот для вашего приложения',
        'screenshots': [],
        'link': ''
    },
    {
        'name': 'Free Slot', 'file_name': 'free', 'color': 'white', 
        'avatar': 'empty.png', 'type': 'Остальное', 'category': 'Остальное', 'sub_category': 'Остальное', 'version': 'v0 (beta)',
        'developer': 'you', 'size': '1488 MB',
        'description': 'Бесплатный слот для вашего приложения',
        'screenshots': [],
        'link': ''
    },
    {
        'name': 'Free Slot', 'file_name': 'free', 'color': 'white', 
        'avatar': 'empty.png', 'type': 'Остальное', 'category': 'Остальное', 'sub_category': 'Остальное', 'version': 'v0 (beta)',
        'developer': 'you', 'size': '1488 MB',
        'description': 'Бесплатный слот для вашего приложения',
        'screenshots': [],
        'link': ''
    },
    {
        'name': 'Free Slot', 'file_name': 'free', 'color': 'white', 
        'avatar': 'empty.png', 'type': 'Остальное', 'category': 'Остальное', 'sub_category': 'Остальное', 'version': 'v0 (beta)',
        'developer': 'you', 'size': '1488 MB',
        'description': 'Бесплатный слот для вашего приложения',
        'screenshots': [],
        'link': ''
    },
    {
        'name': 'Free Slot', 'file_name': 'free', 'color': 'white', 
        'avatar': 'empty.png', 'type': 'Остальное', 'category': 'Остальное', 'sub_category': 'Остальное', 'version': 'v0 (beta)',
        'developer': 'you', 'size': '1488 MB',
        'description': 'Бесплатный слот для вашего приложения',
        'screenshots': [],
        'link': ''
    },
    {
        'name': 'Free Slot', 'file_name': 'free', 'color': 'white', 
        'avatar': 'empty.png', 'type': 'Остальное', 'category': 'Остальное', 'sub_category': 'Остальное', 'version': 'v0 (beta)',
        'developer': 'you', 'size': '1488 MB',
        'description': 'Бесплатный слот для вашего приложения',
        'screenshots': [],
        'link': ''
    },
    {
        'name': 'Free Slot', 'file_name': 'free', 'color': 'white', 
        'avatar': 'empty.png', 'type': 'Остальное', 'category': 'Остальное', 'sub_category': 'Остальное', 'version': 'v0 (beta)',
        'developer': 'you', 'size': '1488 MB',
        'description': 'Бесплатный слот для вашего приложения',
        'screenshots': [],
        'link': ''
    }
]

# --- ЛОКАЛЬНОЕ СОХРАНЕНИЕ БИБЛИОТЕКИ ---
def load_library():
    if not os.path.exists(SAVE_FILE):
        return []
    try:
        with open(SAVE_FILE, 'r') as f:
            saved_filenames = json.load(f)
        # Восстанавливаем библиотеку на основе сохраненных имен файлов
        return [app for app in ALL_FILES if app['file_name'] in saved_filenames]
    except Exception as e:
        return []

def save_library():
    try:
        # Сохраняем только имена файлов, чтобы не дублировать массивы данных
        saved_filenames = [app['file_name'] for app in USER_LIBRARY]
        with open(SAVE_FILE, 'w') as f:
            json.dump(saved_filenames, f)
    except Exception as e:
        console.hud_alert('Error saving library', 'error')

USER_LIBRARY = load_library()

# --- УТИЛИТЫ ---
def parse_rgba(hex_color, alpha):
    r, g, b, _ = ui.parse_color(hex_color)
    return (r, g, b, alpha)

def CustomButton(title, bg_color, action_func):
    btn = ui.Button(title=title, tint_color='white', font=('<system-bold>', 16), action=action_func)
    btn.background_color = parse_rgba(bg_color, 0.15)
    btn.border_color = parse_rgba(bg_color, 0.8)
    btn.border_width = 1.5
    btn.corner_radius = 18
    return btn

def GlassView(hex_color, radius=20):
    v = ui.View()
    v.background_color = parse_rgba(hex_color, 0.05)
    v.border_color = parse_rgba(hex_color, 0.3)
    v.border_width = 1
    v.corner_radius = radius
    return v

# --- ЭКРАН ЗАГРУЗКИ ---
class LoadingScreen(ui.View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = BG_COLOR
        
        self.logo_bg = ui.View(background_color='#11131a')
        self.add_subview(self.logo_bg)
        
        self.logo = ui.ImageView(content_mode=ui.CONTENT_SCALE_ASPECT_FILL, clips_to_bounds=True)
        img = ui.Image.named(LOGO_IMAGE_NAME)
        self.logo.image = img if img else ui.Image.named('ionicons-ionic-256')
        self.add_subview(self.logo)
        
        self.status_label = ui.Label(text="Запуск лаунчера...", text_color=TEXT_COLOR, alignment=ui.ALIGN_CENTER, font=('<system-bold>', 14), alpha=0.0)
        self.add_subview(self.status_label)

    def layout(self):
        sz = 120
        logo_y = (self.height - sz) / 2 - 30
        
        self.logo_bg.frame = ((self.width - sz) / 2, logo_y, sz, sz)
        self.logo_bg.corner_radius = sz / 2
        
        self.logo.frame = ((self.width - sz) / 2, logo_y, sz, sz)
        self.logo.corner_radius = sz / 2
        
        self.status_label.frame = (0, logo_y + sz + 30, self.width, 30)

    def start_animation(self):
        ui.animate(lambda: setattr(self.status_label, 'alpha', 0.7), 0.3)
        
        def finish():
            def fade():
                self.alpha = 0.0 
            def safe_remove():
                if self.superview:
                    self.superview.remove_subview(self)
            ui.animate(fade, 0.4, completion=safe_remove)
            
        ui.delay(finish, 1.5) 

# --- АНИМИРОВАННЫЙ ОВЕРЛЕЙ ---
class AnimatedOverlay(ui.View):
    def present_anim(self):
        self.alpha = 0.0
        self.transform = ui.Transform.scale(0.95, 0.95)
        def anim():
            self.alpha = 1.0
            self.transform = ui.Transform.scale(1.0, 1.0)
        ui.animate(anim, 0.15) 

    def dismiss_anim(self, completion=None):
        def anim():
            self.alpha = 0.0
            self.transform = ui.Transform.scale(0.95, 0.95)
        def comp():
            if self.superview:
                self.superview.remove_subview(self)
            if completion: completion()
        ui.animate(anim, 0.15, completion=comp)

# --- НЕПРОЗРАЧНЫЕ ЭКРАНЫ ---
class SupportView(AnimatedOverlay):
    def __init__(self, close_cb, **kwargs):
        super().__init__(**kwargs)
        self.background_color = BG_COLOR 
        self.close_cb = close_cb
        self.title = ui.Label(text='Tech Support', text_color=TEXT_COLOR, font=('<system-bold>', 26), alignment=ui.ALIGN_CENTER)
        self.add_subview(self.title)
        self.tv = ui.TextView(bg_color=SEARCH_BG, text_color=TEXT_COLOR, font=('<system>', 16), corner_radius=15)
        self.add_subview(self.tv)
        self.send_btn = CustomButton('SEND EMAIL', BLUE_NEON, lambda s: [webbrowser.open(f"mailto:{SUPPORT_EMAIL}?subject=Support&body={urllib.parse.quote(self.tv.text)}"), self.dismiss_anim(self.close_cb)])
        self.add_subview(self.send_btn)
        self.back_btn = ui.Button(title='✕ BACK', tint_color=SUBTEXT_COLOR, font=('<system-bold>', 16), action=lambda s: self.dismiss_anim(self.close_cb))
        self.add_subview(self.back_btn)

    def layout(self):
        m = 20
        self.back_btn.frame = (m, 40, 100, 40)
        self.title.frame = (0, 100, self.width, 30)
        self.tv.frame = (m, 160, self.width-m*2, 200)
        self.send_btn.frame = (m, 390, self.width-m*2, 55)

class AppProfileView(AnimatedOverlay):
    def __init__(self, file_data, close_callback, refresh_main_list, **kwargs):
        super().__init__(**kwargs)
        self.background_color = BG_COLOR 
        self.file_data = file_data
        self.close_callback = close_callback
        self.refresh_main_list = refresh_main_list
        self.setup_ui()
        
    def setup_ui(self):
        fd = self.file_data
        color = fd['color']
        self.scroll = ui.ScrollView()
        self.add_subview(self.scroll)
        self.back_btn = ui.Button(title='✕ Назад', tint_color=SUBTEXT_COLOR, font=('<system-bold>', 16), action=lambda s: self.dismiss_anim(self.close_callback))
        self.add_subview(self.back_btn) 
        
        self.avatar = ui.ImageView(content_mode=ui.CONTENT_SCALE_ASPECT_FILL, corner_radius=25, clips_to_bounds=True, background_color=SEARCH_BG)
        img = ui.Image.named(fd['avatar'])
        if img: self.avatar.image = img
        self.scroll.add_subview(self.avatar)
        
        self.title_lbl = ui.Label(text=fd['name'], text_color=TEXT_COLOR, font=('<system-bold>', 26))
        self.scroll.add_subview(self.title_lbl)
        self.dev_lbl = ui.Label(text=f"{fd['developer']} • {fd['size']}", text_color=SUBTEXT_COLOR, font=('<system>', 14))
        self.scroll.add_subview(self.dev_lbl)
        
        self.dl_btn = CustomButton(f"Скачать", color, self.handle_download)
        self.scroll.add_subview(self.dl_btn)
        
        self.is_in_lib = fd in USER_LIBRARY
        lib_text = "➖ Удалить" if self.is_in_lib else "➕ Добавить"
        lib_color = RED_NEON if self.is_in_lib else '#ffffff'
        self.lib_btn = CustomButton(lib_text, lib_color, self.toggle_library)
        self.scroll.add_subview(self.lib_btn)
        
        self.gallery_scroll = ui.ScrollView(shows_horizontal_scroll_indicator=False)
        self.scroll.add_subview(self.gallery_scroll)
        
        self.screenshots = []
        for shot_name in fd['screenshots'][:MAX_PROFILE_PHOTOS]:
            sv = ui.ImageView(content_mode=ui.CONTENT_SCALE_ASPECT_FILL, corner_radius=15, clips_to_bounds=True, background_color=SEARCH_BG)
            s_img = ui.Image.named(shot_name)
            if s_img: sv.image = s_img
            self.gallery_scroll.add_subview(sv)
            self.screenshots.append(sv)
            
        self.desc_lbl = ui.Label(text=fd['description'], text_color=SUBTEXT_COLOR, font=('<system>', 16), number_of_lines=0)
        self.scroll.add_subview(self.desc_lbl)

    @ui.in_background
    def handle_download(self, sender):
        try:
            choice = console.alert('Download', f'Нажмите на Copy Link что бы скопировать ссылку на скачивание {self.file_data["name"]} и вставьте эту ссылку в любой браузер', 'Copy Link')
            link = self.file_data.get('link', 'https://google.com')
            if choice == 1: 
                # Эта команда вызовет открытие браузера (в iOS это Safari по умолчанию)
                webbrowser.open(link)
            elif choice == 2:
                clipboard.set(link)
                console.hud_alert('Link copied!', 'success')
        except KeyboardInterrupt: pass

    def toggle_library(self, sender):
        if self.file_data in USER_LIBRARY:
            USER_LIBRARY.remove(self.file_data)
            self.lib_btn.title = "➕ Добавить"
            self.lib_btn.background_color, self.lib_btn.border_color = parse_rgba('#ffffff', 0.1), parse_rgba('#ffffff', 0.5)
            console.hud_alert('Удалено')
        else:
            USER_LIBRARY.append(self.file_data)
            self.lib_btn.title = "➖ Удалить"
            self.lib_btn.background_color, self.lib_btn.border_color = parse_rgba(RED_NEON, 0.1), parse_rgba(RED_NEON, 0.5)
            console.hud_alert('Добавлено', 'success')
        
        # Сохраняем локально при каждом изменении!
        save_library()
        self.refresh_main_list()

    def layout(self):
        m = 20
        self.back_btn.frame = (m, 40, 100, 40)
        self.scroll.frame = (0, 90, self.width, self.height - 90)
        self.avatar.frame = (m, 10, 110, 110) 
        tx = m + 130                     
        tw = self.width - tx - m         
        
        self.title_lbl.frame = (tx, 15, tw, 35)
        self.dev_lbl.frame = (tx, 50, tw, 20)
        
        self.dl_btn.frame = (tx, 80, 85, 40)
        self.lib_btn.frame = (tx + 95, 80, 115, 40)
        
        gy = 150
        self.gallery_scroll.frame = (0, gy, self.width, 240)
        
        sw, sh, gx = 150, 240, m
        for shot in self.screenshots:
            shot.frame = (gx, 0, sw, sh)
            gx += sw + 15
        self.gallery_scroll.content_size = (gx, sh)
        
        dy = gy + sh + 30 if self.screenshots else gy + 20
        self.desc_lbl.frame = (m, dy, self.width - m*2, 0)
        self.desc_lbl.size_to_fit()
        self.scroll.content_size = (self.width, self.desc_lbl.frame[1] + self.desc_lbl.height + 50)


# --- ОСНОВНОЙ ЛАУНЧЕР ---
class LauncherApp(ui.View):
    def __init__(self):
        self.background_color = BG_COLOR
        self.current_filter = None 
        self.current_sub_filter = None  
        self.current_tab = 'GAMES' 
        self.list_item_views = []
        
        self.setup_ui()
        self.refresh_list() 
        self.loading_screen = LoadingScreen()
        self.add_subview(self.loading_screen)
        
    def setup_ui(self):
        self.search_bar = ui.TextField(placeholder='Поиск...')
        self.search_bar.background_color, self.search_bar.text_color, self.search_bar.tint_color = 'white', 'black', 'black'
        self.search_bar.corner_radius, self.search_bar.clear_button_mode, self.search_bar.alignment = 20, 'while_editing', ui.ALIGN_CENTER
        self.search_bar.font, self.search_bar.delegate, self.search_bar.action = ('<system-bold>', 16), self, lambda s: s.end_editing()
        self.add_subview(self.search_bar)
        
        # Кнопка профиля удалена
        
        self.cards = []
        for title, emoji, color in [('.ipa', '', BLUE_NEON), ('.apk', '📦', GREEN_NEON), ('Остальное', '📁', RED_NEON)]:
            card = self.create_glass_card(title, emoji, color)
            self.add_subview(card)
            self.cards.append(card)
            
        self.sub_cards = []
        for title, color in [('Приложения', BLUE_NEON), ('Игры', GREEN_NEON), ('Остальное', RED_NEON)]:
            btn = CustomButton(title, color, self.on_sub_tapped)
            btn.font = ('<system-bold>', 13)
            btn.border_width = 1
            btn.sub_category, btn.neon_color, btn.is_selected = title, color, False
            self.add_subview(btn)
            self.sub_cards.append(btn)
            
        self.recent_title = ui.Label(text='Магазин', text_color=TEXT_COLOR, font=('<system-bold>', 26))
        self.add_subview(self.recent_title)
        
        self.scroll = ui.ScrollView()
        self.add_subview(self.scroll)
        
        self.tab_bar = ui.View(background_color=parse_rgba(TABBAR_BG, 0.9))
        self.tab_bar.add_subview(ui.View(frame=(0,0,1000,1), background_color=(1,1,1,0.05), flex='W'))
        
        self.tab_games = ui.Button(title='🎮 Игры', tint_color='white', font=('<system-bold>', 16), action=self.switch_tab)
        self.tab_games.tab_id, self.tab_games.background_color, self.tab_games.corner_radius = 'GAMES', SEARCH_BG, 18
        self.tab_bar.add_subview(self.tab_games)
        
        self.tab_lib = ui.Button(title='📚 Библиотека', tint_color=SUBTEXT_COLOR, font=('<system-bold>', 16), action=self.switch_tab)
        self.tab_lib.tab_id, self.tab_lib.corner_radius = 'LIBRARY', 18
        self.tab_bar.add_subview(self.tab_lib)
        self.add_subview(self.tab_bar)

    def switch_tab(self, sender):
        self.current_tab = sender.tab_id
        if self.current_tab == 'GAMES':
            self.tab_games.background_color, self.tab_games.tint_color = SEARCH_BG, 'white'
            self.tab_lib.background_color, self.tab_lib.tint_color = 'clear', SUBTEXT_COLOR
            self.recent_title.text = 'Основное'
        else:
            self.tab_lib.background_color, self.tab_lib.tint_color = SEARCH_BG, 'white'
            self.tab_games.background_color, self.tab_games.tint_color = 'clear', SUBTEXT_COLOR
            self.recent_title.text = 'Моя библиотека'
        self.refresh_list()

    def create_glass_card(self, title, emoji, color):
        v = GlassView(color, 24)
        v.file_category, v.is_selected, v.neon_color = title, False, color
        v.add_subview(ui.Label(text=emoji, alignment=ui.ALIGN_CENTER, font=('<system>', 40), frame=(0,15,100,50)))
        v.add_subview(ui.Label(text=title, text_color=color, alignment=ui.ALIGN_CENTER, font=('<system-bold>', 17), frame=(0,75,100,30)))
        
        press_overlay = ui.View(background_color='black', alpha=0.0, corner_radius=24)
        v.add_subview(press_overlay)
        v.press_overlay = press_overlay
        
        btn = ui.Button(frame=(0,0,100,100), action=self.on_card_tapped)
        btn.card_ref = v
        v.add_subview(btn)
        return v

    def open_support(self):
        self.overlay = SupportView(self.close_overlay)
        self.show_overlay()

    def open_app_profile(self, file_data):
        self.search_bar.end_editing()
        self.overlay = AppProfileView(file_data, self.close_overlay, self.refresh_list)
        self.show_overlay()

    def show_overlay(self):
        self.overlay.frame = self.bounds
        self.overlay.flex = 'WH'
        self.add_subview(self.overlay)
        self.overlay.present_anim()

    def close_overlay(self):
        self.overlay = None

    def textfield_did_change(self, textfield): self.refresh_list()

    def on_card_tapped(self, sender):
        card = sender.card_ref
        self.search_bar.end_editing()
        
        # Затемнение карточки
        card.press_overlay.alpha = 0.4
        ui.animate(lambda: setattr(card.press_overlay, 'alpha', 0.0), 0.2)

        if self.current_filter == card.file_category:
            self.current_filter, card.is_selected = None, False
        else:
            for c in self.cards: c.is_selected = False
            self.current_filter, card.is_selected = card.file_category, True
            
        for c in self.cards:
            c.background_color = parse_rgba(c.neon_color, 0.15 if c.is_selected else 0.05)
            c.border_width = 2.5 if c.is_selected else 1
            c.border_color = parse_rgba(c.neon_color, 0.8 if c.is_selected else 0.3)
        self.refresh_list()
        
    def on_sub_tapped(self, btn):
        self.search_bar.end_editing()
        if self.current_sub_filter == btn.sub_category:
            self.current_sub_filter, btn.is_selected = None, False
        else:
            for b in self.sub_cards: b.is_selected = False
            self.current_sub_filter, btn.is_selected = btn.sub_category, True
            
        for b in self.sub_cards:
            b.background_color = parse_rgba(b.neon_color, 0.3 if b.is_selected else 0.1)
            b.border_width = 2.0 if b.is_selected else 1.0
        self.refresh_list()

    def refresh_list(self):
        for sub in list(self.scroll.subviews):
            self.scroll.remove_subview(sub)
        self.list_item_views.clear()
        
        search_query = self.search_bar.text.lower()
        source_data = ALL_FILES if self.current_tab == 'GAMES' else USER_LIBRARY
        
        for fd in source_data:
            if self.current_filter and fd.get('category') != self.current_filter: continue
            if self.current_sub_filter and fd.get('sub_category') != self.current_sub_filter: continue
            if search_query and search_query not in fd['name'].lower() and search_query not in fd['file_name'].lower(): continue
                
            item = GlassView(fd['color'], 20)
            item.background_color = parse_rgba(fd['color'], 0.03)
            item.add_subview(ui.View(background_color=fd['color'], corner_radius=2, frame=(10, 15, 4, 45)))
            
            avatar = ui.ImageView(frame=(25, 10, 55, 55), content_mode=ui.CONTENT_SCALE_ASPECT_FILL, corner_radius=14, clips_to_bounds=True, background_color=SEARCH_BG)
            img = ui.Image.named(fd['avatar'])
            if img: avatar.image = img
            item.add_subview(avatar)
            
            item.add_subview(ui.Label(text=fd['name'], text_color=TEXT_COLOR, font=('<system-bold>', 17)))
            item.add_subview(ui.Label(text=f"{fd['file_name']} • {fd['size']}", text_color=SUBTEXT_COLOR, font=('<system>', 13)))
            btn = ui.Button(action=lambda s, f=fd: self.open_app_profile(f))
            item.add_subview(btn)
            
            self.scroll.add_subview(item)
            self.list_item_views.append((item, item.subviews[-3], item.subviews[-2], btn))
            
        self.layout_list()
        
        self.scroll.alpha = 0
        ui.animate(lambda: setattr(self.scroll, 'alpha', 1.0), 0.15)

    def layout_list(self):
        y = 0
        for container, ln, ls, btn in self.list_item_views:
            container.frame = (0, y, self.scroll.width, 75)
            ln.frame = (95, 12, container.width - 110, 25) 
            ls.frame = (95, 40, container.width - 110, 20)
            btn.frame = (0, 0, container.width, container.height)
            y += 90 
        self.scroll.content_size = (self.scroll.width, y + 20)

    def layout(self):
        m = 20
        # Строка поиска теперь занимает всю ширину
        search_w = self.width - m*2
        self.search_bar.frame = (m, 50, search_w, 45)
        
        card_w = (self.width - m*4) / 3
        card_h = card_w * 1.25 
        
        for i, card in enumerate(self.cards):
            x_pos = m + i * (card_w + m)
            card.frame = (x_pos, 115, card_w, card_h)
            card.subviews[0].frame = (0, 15, card_w, 50) 
            card.subviews[1].frame = (0, card_h - 40, card_w, 30) 
            card.press_overlay.frame = (0, 0, card_w, card_h) 
            card.subviews[-1].frame = (0, 0, card_w, card_h) 
            
            sub_btn = self.sub_cards[i]
            sub_w = card_w * 0.9 
            sub_x = x_pos + (card_w - sub_w) / 2
            sub_btn.frame = (sub_x, 115 + card_h + 15, sub_w, 32)
            
        recent_y = 115 + card_h + 15 + 32 + 25 
        self.recent_title.frame = (m, recent_y, self.width - m*2, 35)
        
        tab_h = 90
        self.scroll.frame = (m, recent_y + 45, self.width - m*2, self.height - recent_y - 45 - tab_h)
        self.layout_list()
        
        self.tab_bar.frame = (0, self.height - tab_h, self.width, tab_h)
        btn_w = (self.width - m*3) / 2
        self.tab_games.frame = (m, 15, btn_w, 50)
        self.tab_lib.frame = (m*2 + btn_w, 15, btn_w, 50)

        if self.loading_screen.superview:
            self.loading_screen.frame = self.bounds

    def present_and_animate(self):
        self.present('fullscreen', title_bar_color=BG_COLOR, hide_title_bar=True)
        ui.delay(self.loading_screen.start_animation, 0.2)

if __name__ == '__main__':
    v = LauncherApp()
    v.present_and_animate()
    "GET"
