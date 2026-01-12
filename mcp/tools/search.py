def search_keyword(text: str, keyword: str):
    count = text.lower().count(keyword.lower())
    return {
        "keyword": keyword,
        "count": count
    }
