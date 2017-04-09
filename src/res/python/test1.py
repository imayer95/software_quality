import sys

if __name__ == '__main__':
    args = sys.argv[1:]

    sum_ = 0
    for arg in args:
        sum_ += int(arg)
    print(sum_)
