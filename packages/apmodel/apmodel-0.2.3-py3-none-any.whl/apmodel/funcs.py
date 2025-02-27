from typing import Any, Dict, List, Union

def merge_contexts(
    urls: Union[str, List[Union[str, Dict[str, Any]]]],
    additional_data: Union[str, List[Union[str, Dict[str, Any]]]],
) -> List[Union[str, Dict[str, Any]]]:
    result = []
    merged_dict = {}

    if isinstance(urls, str):
        result.append(urls)
    else:
        for item in urls:
            if isinstance(item, dict):
                merged_dict.update(item)
            else:
                result.append(item)

    if isinstance(additional_data, str):
        result.append(additional_data)
    else:
        for item in additional_data:
            if isinstance(item, dict):
                merged_dict.update(item)
            else:
                result.append(item)

    result.append(merged_dict)

    return result