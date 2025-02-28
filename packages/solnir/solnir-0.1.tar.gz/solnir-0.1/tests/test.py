import solnir
from solnir import Solnir

a = 0

@Solnir.main
def main():
    global a
    solnir.log(f"testing {a}")
    solnir.sleep(5)
    a+=1

if __name__ == "__main__":
    solnir.run(main)