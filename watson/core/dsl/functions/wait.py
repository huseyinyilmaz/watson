def wait(duration: int):
    def f(client):
        print('Wait function is running duration:', duration)
        return True
    return f
