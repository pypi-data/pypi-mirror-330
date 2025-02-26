import logging
import time
from typing import Dict, List, Any, Optional, Callable, Union, Pattern


class RequestMonitor:
    def __init__(self):
        self.enabled = False

    def configure(self, 
                 enabled: bool = False
                ) -> None:
        self.enabled = enabled
        if enabled:
            self._patch_requests()

    def _pre_process_request(self, 
                    url: str, 
                    method: str, 
                    headers: Optional[Dict] = None,
                    body: Any = None) -> None:
        if not self.enabled:
            return
        # todo: 修正为打点逻辑
        logging.info(f"Rre-process Request: {time.time()} {method} {url} {headers} {body}")

    def _post_process_request(self):
        pass

    def _patch_requests(self):
        try:
            import requests
            original_request = requests.request
            
            def patched_request(*args, **kwargs):
                if not self.enabled:
                    return original_request(*args, **kwargs)
                
                method = kwargs.get('method', 'GET')
                url = kwargs.get('url', args[0] if args else '')
                headers = kwargs.get('headers', {})
                data = kwargs.get('data', kwargs.get('json', None))
                
                self._pre_process_request(
                    url=url,
                    method=method,
                    headers=headers,
                    body=data
                )

                response = original_request(*args, **kwargs)
                self._post_process_request()
                return response
            
            requests.request = patched_request
            logging.debug("已对 requests 库进行AOP注入")
        except ImportError:
            logging.debug("未找到 requests 库，跳过拦截")


request_monitor = RequestMonitor() 