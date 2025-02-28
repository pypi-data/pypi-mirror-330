import pprint

def pprint_limited_dict(data, limit=10):
    """
    딕셔너리를 예쁘게 출력하되, 리스트/튜플/세트 타입의 값은 최대 `limit` 개까지만 표시합니다.

    매개변수:
        data (dict): 출력할 딕셔너리.
        limit (int, optional): 리스트, 튜플, 세트의 경우 최대 출력할 항목 개수. 기본값은 10.

    반환값:
        None: `pprint.pprint()`를 사용하여 결과를 직접 출력합니다.

    예제:
        >>> sample_data = {
        ...     "numbers": list(range(20)),
        ...     "name": "Alice",
        ...     "scores": (95, 88, 92, 76, 89, 100),
        ...     "tags": {"AI", "ML", "Data Science"},
        ... }
        >>> pprint_limited_dict(sample_data, limit=3)
        {'numbers': [0, 1, 2],
         'name': 'Alice',
         'scores': [95, 88, 92],
         'tags': ['AI', 'Data Science', 'ML']}
    """
    trimmed_data = {}
    for key, value in data.items():
        if isinstance(value, (list, tuple, set)):  # 리스트, 튜플, 세트일 경우
            trimmed_data[key] = list(value)[:limit]  # 최대 10개까지만 출력
        else:
            trimmed_data[key] = value  # 다른 타입은 그대로 유지

    pprint.pprint(trimmed_data)