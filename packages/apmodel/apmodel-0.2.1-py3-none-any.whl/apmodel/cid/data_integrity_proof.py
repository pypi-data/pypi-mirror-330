from typing import Union
from ..core import merge_contexts


class DataIntegrityProof:
    def __init__(
        self,
        cryptosuite: str,
        proofValue: str,
        proofPurpose: str,
        verificationMethod: str,
        created: str,
        _context: Union[str, list] = [
            "https://www.w3.org/ns/activitystreams",
            "https://w3id.org/security/data-integrity/v1",
        ],
        **kwargs,
    ):
        self._context = merge_contexts(kwargs.get("@context"), _context)

        self.type = "DataIntegrityProof"
        self.cryptosuite = cryptosuite
        self.verificationMethod = verificationMethod
        self.proofPurpose = proofPurpose
        self.proofValue = proofValue
        self.created = created

        self._extras = {}
        for key, value in kwargs.items():
            self._extras[key] = value

    def to_dict(self):
        ctx = self._context.copy()
        context = merge_contexts(
            ctx,
            [
                "https://www.w3.org/ns/activitystreams",
                "https://w3id.org/security/data-integrity/v1",
            ],
        )
        return {
            "@context": context,
            "type": self.type,
            "cryptosuite": self.cryptosuite,
            "verificationMethod": self.verificationMethod,
            "proofPurpose": self.proofPurpose,
            "proofValue": self.proofValue,
            "created": self.created,
        }
