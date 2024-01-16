from typing import TypeVar

K = TypeVar("K")
V = TypeVar("V")


def remove_duplicated_values(list_dictionaries: list[dict[K, V]], key: K) -> list[dict[K, V]]:
    """Remove dictionaries with duplicated values by given key"""
    unique_values = {}
    return [
        unique_values.setdefault(dictionary[key], dictionary)
        for dictionary in list_dictionaries
        if dictionary[key] not in unique_values
    ]
