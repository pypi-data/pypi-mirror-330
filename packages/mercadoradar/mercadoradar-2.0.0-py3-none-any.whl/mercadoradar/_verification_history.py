from ._api import MercadoRadarAPI
from ._models.verification_history import VerificationHistory as VerificationHistorySchema
from .enums import VerificationType, VerificationObjectType


class VerificationHistory:

    @classmethod
    def create(cls,
               type: VerificationType,
               object_type: VerificationObjectType,
               object_id: int,
               is_verified: bool,
               reason: str = None,
               suggestion: str = None) -> VerificationHistorySchema:
        api = MercadoRadarAPI()
        data = dict(
            type=type,
            object_type=object_type,
            object_id=object_id,
            is_verified=is_verified,
            reason=reason,
            suggestion=suggestion
        )
        verification = api.create_request(path=f'/v3/verification-history/', data=data)

        return VerificationHistorySchema(**verification)
