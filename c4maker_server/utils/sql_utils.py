

def get_position_of_field_in_insert_query(insert_query: str, field: str) -> int:
    if not insert_query or not field:
        return -1

    try:
        open_index = insert_query.index("(")
        close_index = insert_query.index(")")
    except ValueError:
        return -1

    if open_index < 0 or close_index < 0 or close_index - open_index < 2:
        return -1

    between_parentheses = insert_query[open_index + 1:close_index]
    fields = [f.strip() for f in between_parentheses.split(",")]

    if field in fields:
        return fields.index(field)

    return -1
