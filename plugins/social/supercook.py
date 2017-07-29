from plugins.plugin_base import PluginBase
import requests
import json
import random


def get_available_settings():
    return ['api_token']


def get_type():
    return Supercook


class Supercook(PluginBase):
    def __init__(self, plugin_id, settings_manager):
        super().__init__(plugin_id, settings_manager)

    def add_ingredient(self, ingredient):
        requests.post('http://www.supercook.com/dyn/ai', data={'i': ingredient, 'lh': self._get_setting('api_token')})

    def remove_ingredient(self, ingredient):
        requests.post('http://www.supercook.com/dyn/ri', data={'i': ingredient, 'lh': self._get_setting('api_token')})

    def get_ingredients(self):
        resp = requests.post('https://www.supercook.com/dyn/refresh_ingredients',
                             data={'lh': self._get_setting('api_token')})

        data = json.loads(resp.text)

        return [item['i'] for item in data['ingredients']]

    def get_recipes(self, category=',', start_from=0):
        ingridients = self.get_ingredients()

        post_data = {
            'needsimage': '0',
            'kitchen': ','.join(ingridients),
            'focus': '',
            'kw': '',
            'catname': category,
            'exclude': '',
            'start': start_from
        }

        resp = requests.post('http://www.supercook.com/dyn/results', data=post_data)

        data = json.loads(resp.text)

        return data['results']

    def get_a_suggested_recipe(self, category=','):
        recipes = self.get_recipes(category)

        full_recipes = [recipe for recipe in recipes if len(recipe['needs']) < 1]

        return random.choice(full_recipes) if len(full_recipes) > 0 else random.choice(recipes)
