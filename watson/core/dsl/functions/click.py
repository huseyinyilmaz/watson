def click(query: str):
    def f(**kwargs):
        log = kwargs['log']
        log(f'click(\'query\'): success')
        return True
    return f
