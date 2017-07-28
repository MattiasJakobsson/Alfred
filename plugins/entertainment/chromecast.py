from plugins.plugin_base import PluginBase
import pychromecast
import uuid


def get_available_settings():
    return ['name']


def get_type():
    return ChromecastDevice


def auto_detect(current_plugins):
    current_names = [device.get_setting('name') for device in current_plugins]

    chromecasts = pychromecast.get_chromecasts()

    new_casts = [cast for cast in chromecasts if
                 len([name for name in current_names if name == cast.device.friendly_name]) < 1]

    return [{'settings': {'name': cast.device.friendly_name}, 'title': 'Chromecast %s' % cast.device.friendly_name}
            for cast in new_casts]


class ChromecastDevice(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager, default_state={'current_states': {'is_playing': False}})

        self.cast = None

    def _update_state(self, new_status):
        is_playing = new_status.player_is_playing() or new_status.player_is_paused()
        name = self._get_setting('name')

        if is_playing != self._state['current_states']['is_playing']:
            if is_playing:
                self._apply('cast_started_casting', {'name': name})
            else:
                self._apply('cast_stopped_casting', {'name': name})

    def _get_cast(self):
        if self.cast is not None:
            return self.cast

        chromecasts = pychromecast.get_chromecasts()

        name = self._get_setting('name')

        self.cast = next(cc for cc in chromecasts if cc.device.friendly_name == name)

        self.cast.wait()

        return self.cast

    def pause(self):
        self._get_cast().media_controller.pause()

    def play(self):
        self._get_cast().media_controller.play()

    def play_media(self, media, media_type):
        self._get_cast().media_controller.play_media(media, media_type)

    def setup_status_listener(self):
        cast = self._get_cast()

        cast.media_controller.register_status_listener(self._update_state)

    def get_automations(self):
        self.setup_status_listener()

        return [{
            'definition': {'initial_step': {
                'id': str(uuid.uuid4()),
                'type': '.workflows.steps.execute_plugin_command',
                'plugin_id': self._plugin_id,
                'command': 'setup_status_listener',
                'parameters': {}
            }},
            'triggers': [{'type': '.workflows.triggers.event_listener_trigger', 'subscribe_to': 'workflows_started'}]
        }]

    def _on_cast_started_casting(self, event_data):
        self._state['current_states']['is_playing'] = True

    def _on_cast_stopped_casting(self, event_data):
        self._state['current_states']['is_playing'] = False
