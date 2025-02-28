from _typeshed import Incomplete
from typing import Any, Dict, Optional, Union

# Version
from firebase_admin.__about__ import __version__

# Module imports
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
from firebase_admin import messaging
from firebase_admin import storage
from firebase_admin import db
from firebase_admin import app_check
from firebase_admin import exceptions
from firebase_admin import tenant_mgt
from firebase_admin import ml
from firebase_admin import project_management
from firebase_admin import instance_id

# Re-export Client from firestore
from firebase_admin.firestore import Client

def initialize_app(
    credential: Optional[credentials.Certificate] = None,
    options: Optional[Dict[str, Any]] = None,
    name: str = "[DEFAULT]"
) -> App: ...

def delete_app(app: App) -> None: ...

def get_app(name: str = "[DEFAULT]") -> App: ...

class _AppOptions:
    def __init__(self, options: Dict[str, Any]) -> None: ...
    def get(self, key: str, default: Optional[Any] = None) -> Any: ...

class App:
    def __init__(
        self, 
        name: str, 
        credential: credentials.Certificate, 
        options: Dict[str, Any]
    ) -> None: ...
    
    @property
    def name(self) -> str: ...
    
    @property
    def credential(self) -> credentials.Certificate: ...
    
    @property
    def options(self) -> _AppOptions: ...
    
    @property
    def project_id(self) -> str: ...
