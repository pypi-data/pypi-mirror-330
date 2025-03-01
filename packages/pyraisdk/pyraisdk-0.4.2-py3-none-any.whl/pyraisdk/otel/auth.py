import logging
import sys
import threading
from time import sleep
from typing import NamedTuple, Optional
import time
from azure.identity import DefaultAzureCredential, ClientSecretCredential
from azure.core.credentials import AccessToken
from .config import OtelConfig
from azure.keyvault.secrets import SecretClient

TOKEN_FETCHER_KV_CLIENT_SECRET = "KeyVaultClientSecretFetcher"
TOKEN_FETCHER_CLIENT_SECRET_CREDENTIAL = "ClientSecretCredentialTokenFetcher"
TOKEN_FETCHER_DEFAULT = "DefaultAzureCredentialFetcher"
logger = logging.getLogger("pyraisdk.otel.TokenFetcher")

class Token(NamedTuple):
    token: str
    """The token string."""
    expires_on: int
    """The token's expiration time in Unix time."""
    refresh_on: Optional[int]
    """Specifies the time, in Unix time, when the cached token should be proactively refreshed. Optional."""

class TokenFetcher:
    def __init__(self, token_type: str, fetch_fn, stop_evt: threading.Event):
        self._token_type = token_type
        self._fetch_fn = fetch_fn
        self._stop_evt = stop_evt
        self._current_value : Optional[Token] = None
        self._error_counter = 0
        self._error = None
        self._lock = threading.Lock()
        self._first_fetch = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self):
        def try_set_first_fetch_event():
            if not self._first_fetch.is_set():
                self._first_fetch.set()
        while(not self._stop_evt.is_set()):
            try:
                start_ts = int(time.time())
                val = self._fetch_fn()
                if isinstance(val, Token):
                    with self._lock:
                        self._error = None
                        self._error_counter = 0
                        self._current_value = val
                    try_set_first_fetch_event()
                    fetch_ts = int(time.time())
                    refresh_ts = val.refresh_on
                    if refresh_ts == None:
                        refresh_ts = val.expires_on - (5 * 60)

                    delay = refresh_ts - fetch_ts
                    delay = delay if delay > 0 else 0
                    logger.info(f"[{self._token_type}] Token fetch succeeded. Took {fetch_ts - start_ts}sec. Will refetch token in {delay}sec.")
                    if delay > 0:
                        sleep(delay)
                else:
                    logger.error(f"[{self._token_type}] Token type mismatch. Retrying in 2sec.")
                    sleep(2)
            except:
                delay = 0
                ect = 0
                with self._lock:
                    self._error_counter += 1
                    ect = self._error_counter
                    delay = 2 ** self._error_counter
                self._error = sys.exc_info()
                logger.error(f"[{self._token_type}] Token fetch error. Attempts={ect}. Retrying in {delay}sec.", exc_info=True)
                if ect >= 3:
                    try_set_first_fetch_event()
                sleep(delay)
        try_set_first_fetch_event()

    def get_token(self) -> Token:
        if not self._first_fetch.is_set():
            self._first_fetch.wait()
        with self._lock:
            token = self._current_value
            if token == None:
                raise RuntimeError(f"[{self._token_type}] Token fetch failed. Attempts={self._error_counter}. Error={self._error}")
            return token
                

class AuthClient:
    def __init__(self, config: OtelConfig, stop_evt: threading.Event):
        self.config = config
        self.token_fetchers = {}
        if self.config.local_run or self.config.environment == "" or self.config.environment != "prod":
            self.client_secret_fetcher = TokenFetcher(TOKEN_FETCHER_KV_CLIENT_SECRET, self.fetch_client_secret, stop_evt)
            self.main_token_fetcher = TokenFetcher(TOKEN_FETCHER_CLIENT_SECRET_CREDENTIAL, self.fetch_token_for_service_pricipal_from_client_secret, stop_evt)
        else:
            self.main_token_fetcher = TokenFetcher(TOKEN_FETCHER_DEFAULT, self.fetch_token, stop_evt)
    
    def get_token(self) -> Token:
        return self.main_token_fetcher.get_token()
        
    def fetch_client_secret(self) -> Token:
        credential = DefaultAzureCredential(exclude_interactive_browser_credential=True, managed_identity_client_id=self.config.uai_client_id)
        client = SecretClient(self.config.kv_url, credential)
        secret = client.get_secret(self.config.kv_secret_name)
        return Token(token=secret.value, expires_on=int(time.time()) + 10 * 60, refresh_on=None)
        
    def fetch_token_for_service_pricipal_from_client_secret(self) -> Token:
        client_secret = self.client_secret_fetcher.get_token()
        cred = ClientSecretCredential(self.config.azure_tenant_id, self.config.azure_client_id, client_secret.token)
        token_info = cred.get_token_info(self.config.auth_scope)
        return Token(token=token_info.token, expires_on=token_info.expires_on, refresh_on=token_info.refresh_on)
    
    def fetch_token(self) -> Token:
        credential = DefaultAzureCredential(exclude_interactive_browser_credential=True, managed_identity_client_id=self.config.uai_client_id)
        token_info = credential.get_token_info(self.config.auth_scope)
        return Token(token=token_info.token, expires_on=token_info.expires_on, refresh_on=token_info.refresh_on)

    
       
                
            
        