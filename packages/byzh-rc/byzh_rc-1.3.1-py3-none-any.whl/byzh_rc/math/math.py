def get_num(num):
    if isinstance(num, str):
        return float(num)
    return num
def b_divides(iterUp, iterDown):
    """
    支持list, tuple, set, 单个数\n
    iterUp as 分子\n
    iterDown as 分母
    """
    up = 1
    down = 1

    if not isinstance(iterUp, list) and not isinstance(iterUp, tuple) and not isinstance(iterUp, set):
        up *= get_num(iterUp)
    else:
        for x in iterUp:
            up *= get_num(x)

    if not isinstance(iterDown, list) and not isinstance(iterDown, tuple) and not isinstance(iterDown, set):
        down *= get_num(iterDown)
    else:
        for x in iterDown:
            down *= get_num(x)

    return up / down

if __name__ == '__main__':
    result = b_divides([1, 2, 3], [4, 5])
    print(result)

    result = b_divides(6.63e-34, (9.11e-31, 3e8))
    print(result)

    result = b_divides('6.63e-34', ['9.11e-31', 3e8])
    print(result)