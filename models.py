from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class IncomingSource:
    id: int
    name: str
    description: str

@dataclass
class OutgoingDestination:
    id: int
    name: str
    description: str

@dataclass
class IncomingType:
    id: int
    name: str
    description: str

@dataclass
class Employee:
    id: int
    name: str
    department: str
    position: str
    is_active: bool

@dataclass
class Specialization:
    id: int
    name: str
    description: str

@dataclass
class Attachment:
    id: int
    record_id: int
    record_type: str
    file_name: str
    file_path: str
    upload_date: datetime
    description: str

@dataclass
class IncomingRecord:
    id: int
    record_number: str
    incoming_number: str
    serial_number: str
    title: str
    incoming_source_id: int
    incoming_type_id: int
    employee_id: int
    specialization_id: int
    registration_date: str
    details: str
    attachments: List[Attachment] = None
    
    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []

@dataclass
class OutgoingRecord:
    id: int
    record_number: str
    outgoing_number: str
    serial_number: str
    title: str
    outgoing_destination_id: int
    employee_id: int
    specialization_id: int
    registration_date: str
    details: str
    attachments: List[Attachment] = None
    
    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []