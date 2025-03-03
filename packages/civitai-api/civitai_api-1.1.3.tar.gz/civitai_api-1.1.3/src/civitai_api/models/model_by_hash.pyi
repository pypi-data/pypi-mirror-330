from .model_by_version_id import Response_ModelByVersionId as Response_ModelByVersionId

class Response_Model_ByHash(Response_ModelByVersionId):
    class Config:
        orm_mode: bool
