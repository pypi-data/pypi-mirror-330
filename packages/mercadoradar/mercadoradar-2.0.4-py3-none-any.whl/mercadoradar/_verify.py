from ._models.VerificationHistory import VerificationHistory
from ._api import MercadoRadarAPI
from .enums import VerifyType, VerifyObjectType


class Verify:

    @classmethod
    def create(cls,
               type: VerifyType,
               object_type: VerifyObjectType,
               object_id: int,
               is_verified: bool,
               reason: str = None,
               suggestion: str = None) -> VerificationHistory:
        api = MercadoRadarAPI()
        data = dict(
            type=type,
            object_type=object_type,
            object_id=object_id,
            is_verified=is_verified,
            reason=reason,
            suggestion=suggestion
        )
        verification = api.create_request(path='/v3/verify/', data=data)

        return VerificationHistory(**verification)