Ex = [22, 4147, 1234, 11]
Nx = Ex[0] + Ex[3]
Lx = Ex[1] + Ex[2]


def ax(e):
    t = len(e)
    s = Lx
    for r in range(t):
        s = s * Nx + ord(e[r])
        s &= 0xFFFFFFFF  # Simulate 32-bit unsigned integer overflow
    return s


def px(path: str, security_key: str, params: str):
    s = "baf4c54e9dae"
    return ax(path + security_key + params + s)
