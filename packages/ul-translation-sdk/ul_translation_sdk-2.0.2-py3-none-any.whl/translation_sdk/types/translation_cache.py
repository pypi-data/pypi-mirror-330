from typing import Dict

from ul_api_utils.api_resource.api_response import RootJsonApiResponsePayload


class ApiFullTranslationCacheResponse(RootJsonApiResponsePayload[Dict[str, Dict[str, str]]]):
    pass


class ApiLangTranslationCacheResponse(RootJsonApiResponsePayload[Dict[str, str]]):
    pass
