import logging
from typing import Optional, Tuple, Type
from urllib.parse import urljoin

import requests

from spei.requests import CDARequest
from spei.resources import CDA
from spei.responses import AcuseResponse

logger = logging.getLogger('sice')
logger.setLevel(logging.DEBUG)


class BaseClient(object):
    def __init__(
        self,
        host: str,
        verify: bool = False,
        http_client: Type[requests.Session] = requests.Session,
        auth: Optional[Tuple[str, str]] = None,
    ) -> None:
        self.host: str = host
        self.session: requests.Session = http_client()
        self.session.headers.update({'Content-Type': 'application/xml'})
        self.session.verify = verify
        if auth:
            self.session.auth = auth

    def registra_cda(
        self,
        cda_data: dict,
        cda_cls: Type[CDA] = CDA,
        acuse_response_cls: Type[AcuseResponse] = AcuseResponse,
        endpoint: str = '/enlace-cep/EnvioCdaPortTypeImpl?wsdl',
    ) -> AcuseResponse:
        orden = cda_cls(**cda_data)
        soap_request = CDARequest(orden)
        logger.info(soap_request)
        cda_url = urljoin(self.host, endpoint)
        response: requests.Response = self.session.post(
            data=soap_request,  # type: ignore
            url=cda_url,
        )
        logger.info(response.text)
        response.raise_for_status()
        return acuse_response_cls(response.text)
