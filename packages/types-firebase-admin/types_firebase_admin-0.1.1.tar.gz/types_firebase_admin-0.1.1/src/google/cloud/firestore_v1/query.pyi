from typing import Any, List, TypeVar, Union, Optional
from google.cloud.firestore_v1 import DocumentSnapshot

# Define a type variable for Query
Q = TypeVar('Q', bound='Query')

class Query:
    def where(self, field_path: str, op_string: str, value: Any) -> "CollectionReference": ...
    def stream(self) -> List[Any]: ...
    def get(self) -> List[DocumentSnapshot]: ...

# Forward reference for CollectionReference
from google.cloud.firestore_v1 import CollectionReference
