import urllib.parse
from pathlib import Path
from typing import List, Dict, Union

import requests
from tqdm.auto import tqdm

from .extraction_request import ExtractionRequest
from .request_status import RequestShortStatus, RequestDetailedStatus
from .submit_request_result import SubmitRequestResult


def _raise_error_if_bad_status_code(response):
    if 400 <= response.status_code < 500:
        raise ValueError(response.text)
    elif 500 <= response.status_code < 600:
        raise ValueError(response.text)




class JsonLLM:

    def __init__(self, api_key: str, url: str = "https://jsonllm.com"):
        self.api_key = api_key
        self.url = url

    def submit_request(self, extraction_request: ExtractionRequest) -> SubmitRequestResult:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        body = extraction_request.model_dump()
        response = requests.post(f"{self.url}/api/request/", headers=headers, json=body)
        _raise_error_if_bad_status_code(response)
        return SubmitRequestResult.model_validate(response.json())

    def cancel_request(self, request_id: str) -> Dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        url = f'{self.url}/api/request/{request_id}/cancel/'
        response = requests.post(url, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def get_detailed_request_status(self, request_id: str) -> RequestDetailedStatus:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        url = f'{self.url}/api/request/{request_id}/detailed/'
        response = requests.get(url, headers=headers)
        _raise_error_if_bad_status_code(response)
        return RequestDetailedStatus.model_validate(response.json())

    def get_short_request_status(self, request_id: str) -> RequestShortStatus:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        url = f'{self.url}/api/request/{request_id}/short/'
        response = requests.get(url, headers=headers)
        _raise_error_if_bad_status_code(response)
        return RequestShortStatus.model_validate(response.json())

    def upload(self, dataset: str, paths: List[Union[str, Path]]):
        if isinstance(paths, str):
            paths = [Path(paths)]
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        files = {}
        for path in paths:
            path = Path(path)
            files[path.name] = path.read_bytes()
        encoded = urllib.parse.quote(dataset)
        response = requests.post(f"{self.url}/api/dataset/{encoded}/document/", files=files, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def add_text(self, dataset: str, filename: str, text: str):
        if not filename.endswith(".txt"):
            filename += ".txt"
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        files = {
            filename: text.encode('utf-8')
        }
        encoded = urllib.parse.quote(dataset)
        response = requests.post(f"{self.url}/api/dataset/{encoded}/document/", files=files, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def add_texts(self, dataset: str, filenames: List[str], texts: List[str], batch_size: int = None):
        if not batch_size:
            return self._add_texts_batch(dataset, filenames, texts)
        for start in tqdm(range(0, len(filenames), batch_size)):
            end = start + batch_size
            self._add_texts_batch(dataset, filenames[start:end], texts[start:end])

    def _add_texts_batch(self, dataset: str, filenames, texts):
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        files = {filename: text for filename, text in zip(filenames, texts)}
        encoded = urllib.parse.quote(dataset)
        response = requests.post(f"{self.url}/api/dataset/{encoded}/document/", files=files, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def list_documents(self, dataset: str) -> List[Dict]:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        encoded = urllib.parse.quote(dataset)
        response = requests.get(f"{self.url}/api/dataset/{encoded}/document/", headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()["filenames"]

    def delete_document(self, dataset: str, filename: str):
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        encoded = urllib.parse.quote(dataset)
        encoded_filename = urllib.parse.quote(filename)
        response = requests.delete(f"{self.url}/api/dataset/{encoded}/document/{encoded_filename}", headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def remove_dataset(self, dataset: str) -> Dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        encoded = urllib.parse.quote(dataset)
        url = f'{self.url}/api/dataset/{encoded}/'
        response = requests.delete(url, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()

    def create_dataset(self, dataset: str) -> Dict:
        headers = {
            'Authorization': f'Bearer {self.api_key}'
        }
        encoded = urllib.parse.quote(dataset)
        url = f'{self.url}/api/dataset/{encoded}'
        response = requests.post(url, headers=headers)
        _raise_error_if_bad_status_code(response)
        return response.json()


