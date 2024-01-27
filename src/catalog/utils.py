from collections import defaultdict


def group_filters(filters: dict):
    """
    Group list of objects {'group_title': str, 'id': int} by group_title,
    collapse ids into list
    """
    grouped_filters = {}
    for title, list_attrs in filters.items():
        if not list_attrs:
            continue
        grouped_attrs = defaultdict(lambda: {'ids': [], 'group_title': None})
        for attr in list_attrs:
            grouped_attrs[attr['group_title']]['ids'].append(attr['id'])
            grouped_attrs[attr['group_title']]['group_title'] = attr['group_title']
        grouped_filters[title] = grouped_attrs.values()
    return grouped_filters
