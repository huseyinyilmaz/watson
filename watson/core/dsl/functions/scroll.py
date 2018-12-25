def scrollDown(pixels: float):
    def f(**kwargs):
        print('Scroll down function is running', pixels)
        return True
    return f


def scrollUp(pixels: float):
    def f(**kwargs):
        print('Scoll up function is running', pixels)
        return True
    return f


def scrollToStart():
    def f(**kwargs):
        print('Scoll to End function is running')
        return True
    return f


def scrollToEnd():
    def f(**kwargs):
        print('Scoll to End function is running')
        return True
    return f
