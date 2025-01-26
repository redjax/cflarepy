from loguru import logger as log
import typing as t
from contextlib import contextmanager, AbstractContextManager
from cflarepy.libs import http_lib

import httpx

class CloudflareController(AbstractContextManager):
    def __init__(
        self,
        api_base_url: str = "https://api.cloudflare.com/client/v4",
        debug_secrets: bool = False,
        account_id: str | None = None,
        account_email: str | None = None,
        api_key: str | None = None,
        api_token: str | None = None,
        use_cache: bool = True,
        force_cache: bool = True,
        follow_redirects: bool = True,
        cache_type: str | None = "sqlite",
        cache_file_dir: str | None = ".cache/http/hishel",
        cache_db_file: str = ".cache/http/hishel.sqlite3",
        cache_ttl: int | None = 900,
        check_ttl_every: float | None = 60,
        headers: dict | None = None,
    ) -> None:
        self.base_url = api_base_url
        self.debug_secrets = debug_secrets
        self.account_id = account_id
        self.account_email = account_email
        self.api_key = api_key
        self.api_token = api_token
        self.use_cache = use_cache
        self.force_cache = force_cache
        self.follow_redirects = follow_redirects
        self.cache_type = cache_type
        self.cache_file_dir = cache_file_dir
        self.cache_db_file = cache_db_file
        self.cache_ttl = cache_ttl
        self.check_ttl_every = check_ttl_every
        self.headers = headers

        self.http_controller: http_lib.HttpxController | None = None

    def __enter__(self) -> t.Self:
        self.http_controller = self._get_controller()

        return self

    def __exit__(self, exc_type, exc_val, traceback) -> t.Literal[False] | None:
        return False
    
    @property
    def use_token(self) -> bool:
        if self.api_token:
            return True

    def __repr__(self) -> str:
        vals = [
            f"debug_secrets={self.debug_secrets}",
            f"account_id={self.account_id}",
            f"account_email={self.account_email}",
            f"api_key={self.api_key if self.debug_secrets else '<Redacted>'}",
            f"api_token={self.api_token if self.debug_secrets else '<Redacted>'}",
            f"use_cache={self.use_cache}",
            f"force_cache={self.force_cache}",
            f"follow_redirects={self.follow_redirects}",
            f"cache_type={self.cache_type}",
            f"cache_file_dir={self.cache_file_dir}",
            f"cache_db_file={self.cache_db_file}",
            f"cache_ttl={self.cache_ttl}",
            f"check_ttl_every={self.check_ttl_every}",
            f"headers={self.headers}",
            f"use_token={self.use_token}",
        ]
        vals_str: str = ", ".join(vals)
        # return f"CloudflareController(account_id={self.account_id}, account_email={self.account_email}, api_key=<Redacted>, api_token=<Redacted>, use_cache={self.use_cache}, force_cache={self.force_cache}, follow_redirects={self.follow_redirects}, cache_type={self.cache_type}, cache_file_dir={self.cache_file_dir}, cache_db_file={self.cache_db_file}, cache_ttl={self.cache_ttl}, check_ttl_every={self.check_ttl_every}, headers={self.headers})"
        return f"CloudflareController({vals_str})"

    def merge_headers(self, headers: dict | None) -> dict | None:
        if not self.headers:
            return headers

        merged = {**self.headers, **headers}

        return merged

    def _get_controller(self) -> http_lib.HttpxController:
        controller = http_lib.HttpxController(
            use_cache=self.use_cache,
            force_cache=self.force_cache,
            follow_redirects=self.follow_redirects,
            cache_type=self.cache_type,
            cache_file_dir=self.cache_file_dir,
            cache_db_file=self.cache_db_file,
            cache_ttl=self.cache_ttl,
            check_ttl_every=self.check_ttl_every,
            headers=self.headers,
        )

        return controller
    
    def _validate_auth(self):
        if self.api_token:
            return True
        
        if self.account_email and self.api_key:
            return True
        
    def _validate_token_auth(self, token: str | None):
        if not token:
            if not self.api_token:
                raise ValueError("No API token provided")
            else:
                return self.api_token
            
        return token
    
    def _get_auth_headers(self) -> dict:
        if self.use_token:
            headers: dict = {"Authorization": f"Bearer {self.api_token}"}
        else:
            headers: dict = {"X-Auth-Email": self.account_email, "X-Auth-Key": self.api_key}
            
        return headers
    
    def get_accounts(self, token: str | None = None, headers: dict | None = None) -> str:
        if not headers:
            headers: dict = self._get_auth_headers()
        
        token = self._validate_token_auth(token)
        if not token:
            raise ValueError("No API token provided")
        
        if not self.http_controller:
            self.http_controller = self._get_controller()

        url: str = f"{self.base_url}/accounts"
        req: httpx.Request = http_lib.build_request(url=url, headers=headers)
        
        log.info("Requesting accounts for token")
        try:
            with self.http_controller as http_ctl:
                http_res = http_ctl.send_request(request=req)
                http_res.raise_for_status()
        except Exception as exc:
            msg = f"({type(exc)}) Error getting accounts for token. Details: {exc}"
            log.error(msg)
            
            raise exc
        
        if not http_res.status_code == 200:
            log.warning(f"Non-20 status code requesting accounts for token: [{http_res.status_code}: {http_res.reason_phrase}]: {http_res.text}")
            return
        
        log.info(f"Request accounts response: [{http_res.status_code}: {http_res.reason_phrase}]")
        res_dict = http_lib.decode_response(response=http_res)
        log.debug(f"Response ({type(res_dict)}): {res_dict}")
        res = res_dict["result"]

        return res
