BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_62(num: int) -> str:
    if num == 0:
        return BASE62[0]

    result = []

    while num > 0:
        remainder = num % 62
        result.append(BASE62[remainder])
        num //= 62

    return "".join(reversed(result))