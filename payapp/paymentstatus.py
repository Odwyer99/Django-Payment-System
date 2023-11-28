from enum import Enum

class PaymentRequestStatus(Enum):
    NO_REQUEST_SENT = 1
    SENT_TO_YOU = 2
    SENT_TO_USER = 3