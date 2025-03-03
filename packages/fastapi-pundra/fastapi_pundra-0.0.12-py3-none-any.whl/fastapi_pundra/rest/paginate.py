from fastapi import Request
from urllib.parse import urlparse

def paginate(request: Request, query, serilizer, the_page: int = 1, the_per_page: int = 10, wrap: str = "data", additional_data: dict = None):
    """Paginate the query.
    
    Args:
        request (Request): The FastAPI request object.
        query: The database query to paginate.
        serilizer: The serializer class to convert database objects.
        the_page (int, optional): Default page number. Defaults to 1.
        the_per_page (int, optional): Default items per page. Defaults to 10.
        wrap (str, optional): Key name for the data in response. Defaults to 'data'.
        additional_data (dict, optional): Additional data to include in the response. Defaults to None.
    """

    page = int(request.query_params.get("page", the_page))
    per_page = int(request.query_params.get("per_page", the_per_page))

    total = query.count()
    last_page = (total + per_page - 1) // per_page
    offset = (page - 1) * per_page
    paginated_query = query.offset(offset).limit(per_page).all()

    data = [serilizer.model_validate(item) for item in paginated_query]

    base_url = str(request.base_url)

    full_path = str(request.url)
    parsed_url = urlparse(full_path)
    path_without_query = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

    first_page_url = f"{path_without_query}?page=1&per_page={per_page}"
    last_page_url = f"{path_without_query}?page={last_page}&per_page={per_page}"
    next_page_url = f"{path_without_query}?page={page + 1}&per_page={per_page}" if page < last_page else None
    prev_page_url = f"{path_without_query}?page={page - 1}&per_page={per_page}" if page > 1 else None

    output = {
        "total": total,
        "per_page": per_page,
        "current_page": page,
        "last_page": last_page,
        "first_page_url": first_page_url,
        "last_page_url": last_page_url,
        "next_page_url": next_page_url,
        "prev_page_url": prev_page_url,
        "path": base_url,
        "from": offset + 1 if data else None,
        "to": offset + len(data) if data else None,
        wrap: data
    }

    if additional_data:
        if callable(additional_data):
            output["additional_data"] = additional_data(data)
        else:
            output["additional_data"] = additional_data

    return output
