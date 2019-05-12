from typing import Union, List
from torrenttv.utils.httputils import fix_url, join_url
import requests


class Website(object):

    def __init__(self, base_url: Union[str, List[str]], user_agent: str = None):
        self.base_url_list = [base_url] if isinstance(base_url, str) else base_url
        self.headers = {'User-Agent': user_agent} if user_agent else {}

        # fix urls
        self.base_url_list = [fix_url(url) for url in self.base_url_list]

    def get(self, path: str) -> requests.Response:
        for base_url in self.base_url_list:
            url = join_url(base_url, path)
            url = fix_url(url)

            try:
                response = requests.get(url, headers=self.headers)
                if response.status_code in range(200, 300):
                    return response
            except requests.exceptions.RequestException as e:
                pass

        raise Exception('Failed to fetch {path} from {urls}'.format(path=path, urls=', '.join(self.base_url_list)))
