def file_contains_string(search: str, path: str):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return search in f.read()
