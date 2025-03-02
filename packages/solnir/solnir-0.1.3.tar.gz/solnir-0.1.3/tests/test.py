from solnir import Solnir

a = 0

@Solnir.main
def main():
    global a
    Solnir.log(f"testing {a}")
    Solnir.sleep(5)
    a+=1

if __name__ == "__main__":
    Solnir.run(main)