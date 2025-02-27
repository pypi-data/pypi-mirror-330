import json

import click
import requests


class Tower:
    def __init__(self, token: str):
        self._token = token
        self._url = 'https://flageval.baai.ac.cn/api/s/openai-style/servings'
        self._headers = {
            'X-Flageval-Token': token,
        }

    def watch_openai_serving(self, chat_url: str, model_name: str = '', api_key: str = ''):
        resp = requests.post(
            self._url,
            json={
                'chat_url': chat_url,
                'model_name': model_name,
                'api_key': api_key,
            },
            headers=self._headers,
        )
        return resp.status_code, self._format_response(resp)

    def unwatch_openai_serving(self, chat_url: str, model_name: str):
        resp = requests.post(
            self._url,
            json={
                'chat_url': chat_url,
                'model_name': model_name,
                'enabled': False,
            },
            headers=self._headers,
        )
        return resp.status_code, self._format_response(resp)

    @staticmethod
    def _format_response(resp):
        if resp.status_code >= 200 and resp.status_code < 300:
            return json.dumps(resp.json(), ensure_ascii=False, indent=2)
        return resp.content



@click.command
@click.option('--token', required=True, help='Token for authenticating.')
@click.option('--chat-url', required=True, help='OpenAI style chat url to monitor, e.g., https://api.pandalla.ai/v1/chat/completions')
@click.option('--model-name', required=False, default='', help='Model name for multiple model support.')
@click.option('--api-key', required=False, default='', help='API key for authenticating of the given chat url.')
@click.option('--enable/--no-enable', default=True)
def main(token, chat_url, model_name, api_key, enable):
    t = Tower(token)
    if enable:
        status_code, response = t.watch_openai_serving(chat_url, model_name, api_key)
    else:
        status_code, response = t.unwatch_openai_serving(chat_url, model_name)

    print(f'[{status_code}] {response}')
