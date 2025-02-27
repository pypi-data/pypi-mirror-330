import sys
import time
from concurrent.futures import ThreadPoolExecutor

def worker(delay: int):
    print("Starting worker")
    time.sleep(delay)
    print("Worker woke up")
    return "Done"


def run():
    with ThreadPoolExecutor(max_workers=4) as executor:
        print("Submitting job")
        f1 = executor.submit(worker, 30)
        try:
            print(f1.result(timeout=2))
        except:
            print("Caught a time out error")
            sys.exit()



if __name__ == '__main__':
    run()
    print("End of program")

