import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivy.utils import platform

# Simulate secure storage for demo purposes
class SecureStore:
    def __init__(self):
        self.store = JsonStore('secure_data.json')

    def put(self, key, value):
        self.store.put(key, value=value)

    def get(self, key):
        if self.store.exists(key):
            return self.store.get(key)['value']
        return None

    def delete(self, key):
        if self.store.exists(key):
            self.store.delete(key)

# Screens
class LoginScreen(Screen):
    username = StringProperty('')
    password = StringProperty('')
    remember_me = BooleanProperty(False)
    message = StringProperty('')

    def login(self):
        # Simulate API call
        if self.username == 'admin' and self.password == 'adminpassword':
            # In a real app, we would get a token from the API
            token = 'fake_jwt_token'
            store = SecureStore()
            store.put('auth_token', token)
            if self.remember_me:
                store.put('remember_me', 'true')
            else:
                store.delete('remember_me')
            self.manager.current = 'dashboard'
            self.message = ''
        else:
            self.message = 'Invalid credentials'

class DashboardScreen(Screen):
    status = StringProperty('Stopped')
    is_running = BooleanProperty(False)

    def on_enter(self):
        # Check if bot is running (simulate)
        self.is_running = False
        self.status = 'Stopped'

    def toggle_bot(self):
        if self.is_running:
            self.stop_bot()
        else:
            self.start_bot()

    def start_bot(self):
        # In a real app, we would send a start command to the server via API
        self.is_running = True
        self.status = 'Running'

    def stop_bot(self):
        # In a real app, we would send a stop command to the server via API
        self.is_running = False
        self.status = 'Stopped'

    def view_logs(self):
        self.manager.current = 'logs'

class LogsScreen(Screen):
    logs = StringProperty('')

    def on_enter(self):
        # Simulate fetching logs
        self.logs = '''[INFO] Bot started
[INFO] Connected to Telegram
[INFO] Waiting for commands
[INFO] Received command: /start
[INFO] Processing command...
[INFO] Command processed
[INFO] Waiting for commands
'''

class SettingsScreen(Screen):
    server_url = StringProperty('http://localhost:8000')
    theme = StringProperty('Dark')

    def save_settings(self):
        # Simulate saving settings
        self.manager.current = 'dashboard'

class ScreenManagement(ScreenManager):
    pass

# Load the KV string
kv = '''
#:kivy 2.0.0

<LoginScreen>:
    username: username_input.text
    password: password_input.text
    remember_me: remember_me.active

    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)

        Label:
            text: 'IT Bot Remote Control'
            font_size: dp(24)
            size_hint_y: None
            height: dp(40)

        Label:
            text: 'Login to your server'
            size_hint_y: None
            height: dp(30)

        TextInput:
            id: username_input
            hint_text: 'Username'
            multiline: False

        TextInput:
            id: password_input
            hint_text: 'Password'
            password: True
            multiline: False

        BoxLayout:
            size_hint_y: None
            height: dp(40)
            spacing: dp(10)

            CheckBox:
                id: remember_me
                size_hint_x: None
                width: dp(40)
            Label:
                text: 'Remember me'
                size_hint_x: None
                width: dp(100)

        Label:
            text: root.message
            color: 1, 0, 0, 1
            size_hint_y: None
            height: dp(30)

        Button:
            text: 'Sign in'
            on_release: root.login()
            size_hint_y: None
            height: dp(50)

        Label:
            text: 'Version 1.0.0'
            size_hint_y: None
            height: dp(20)
            halign: 'center'

<DashboardScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)

        Label:
            text: 'Bot Control'
            font_size: dp(24)
            size_hint_y: None
            height: dp(40)

        Label:
            text: 'Status:'
            size_hint_y: None
            height: dp(30)

        Label:
            text: root.status
            color: 0, 1, 0, 1 if root.is_running else 1, 0, 0, 1
            font_size: dp(20)
            bold: True
            size_hint_y: None
            height: dp(40)

        Button:
            text: 'Start Bot' if not root.is_running else 'Stop Bot'
            on_release: root.toggle_bot()
            size_hint_y: None
            height: dp(50)
            background_color: 0, 0.6, 0, 1 if not root.is_running else 0.8, 0, 0, 1

        Button:
            text: 'View Logs'
            on_release: root.view_logs()
            size_hint_y: None
            height: dp(50)

        Button:
            text: 'Settings'
            on_release: root.manager.current = 'settings'
            size_hint_y: None
            height: dp(50)

<LogsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)

        Label:
            text: 'Bot Logs'
            font_size: dp(24)
            size_hint_y: None
            height: dp(40)

        TextInput:
            text: root.logs
            readonly: True
            multiline: True

        Button:
            text: 'Back to Dashboard'
            on_release: root.manager.current = 'dashboard'
            size_hint_y: None
            height: dp(50)

<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(10)

        Label:
            text: 'Settings'
            font_size: dp(24)
            size_hint_y: None
            height: dp(40)

        Label:
            text: 'Server URL'
            size_hint_y: None
            height: dp(30)

        TextInput:
            text: root.server_url
            multiline: False

        Label:
            text: 'Theme'
            size_hint_y: None
            height: dp(30)

        Spinner:
            text: root.theme
            values: ['Dark', 'Light']
            size_hint_y: None
            height: dp(40)
            on_text: root.theme = self.value

        Button:
            text: 'Save'
            on_release: root.save_settings()
            size_hint_y: None
            height: dp(50)

        Button:
            text: 'Back to Dashboard'
            on_release: root.manager.current = 'dashboard'
            size_hint_y: None
            height: dp(50)
'''

class ITBotRemoteApp(App):
    def build(self):
        self.title = 'IT Bot Remote Control'
        Builder.load_string(kv)
        return ScreenManagement()

if __name__ == '__main__':
    ITBotRemoteApp().run()