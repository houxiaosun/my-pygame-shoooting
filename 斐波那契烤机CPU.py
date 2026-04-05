import multiprocessing

def infinite_fib():
    a, b = 0, 1
    while True:
        a, b = b, a + b

if __name__ == "__main__":
    for _ in range(6):  # 我的5600X是6核12线程，6个就能全核满载，要是8核就改成8
        p = multiprocessing.Process(target=infinite_fib)
        p.start()