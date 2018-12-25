def wait(duration: int):
    def f(**kwargs):
        log = kwargs['log']
        log(f'log({duration}): success')
        return True
    return f
