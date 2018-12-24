def click(query: str):
    def f(client):
        print('Click function is running', query)
        return True
    return f
