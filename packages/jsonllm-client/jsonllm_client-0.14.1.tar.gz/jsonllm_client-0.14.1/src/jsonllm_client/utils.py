import hashlib
import time
from typing import List, Any, Dict

from jsonllm_client import JsonLLM, ExtractionRequest, TextsSpec, JsonEntriesSpec, RequestSettings, RequestShortStatus


def get_text_to_key_prediction(
        jsonllm: JsonLLM, texts: List[str], model: str, dataset: str, schema_name: str, key: str, print_fn
) -> Dict[str, Any]:
    jsonllm.create_dataset(dataset)
    filenames = [f'{hashlib.sha256(text.encode()).hexdigest()}.txt' for text in texts]
    jsonllm.add_texts(dataset, filenames, texts, batch_size=100)
    extraction_request = ExtractionRequest(
        model=model,
        texts=TextsSpec(
            dataset=dataset,
        ),
        json_entries=JsonEntriesSpec(
            schema_name=schema_name,
            subset=[key]
        ),
        settings=RequestSettings(
            batch_size=100,
            min_idle_time_ms=10_000,
            block_ms=1_000,
            max_times_delivered=5,
            use_cache=1
        )
    )
    submittion_res = jsonllm.submit_request(extraction_request)
    submit_request_result = jsonllm.submit_request(extraction_request)
    request_id = submit_request_result.request_id
    request_short_status: RequestShortStatus = jsonllm.get_short_request_status(request_id)
    while request_short_status.status == "running":
        request_short_status: RequestShortStatus = jsonllm.get_short_request_status(request_id)
        print_fn(request_short_status)
        time.sleep(1.)
    successful_rows = jsonllm.get_detailed_request_status(submittion_res.request_id).get_successful_rows()
    filename_to_texts = dict(zip(filenames, texts))
    res = {}
    for r in successful_rows:
        filename = r["filename"]
        text = filename_to_texts.get(filename)
        if not text:
            continue
        res[text] = r[key]
    return res
