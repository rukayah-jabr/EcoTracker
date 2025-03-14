import os

from dotenv import load_dotenv

load_dotenv()
CLIMATIQ_API_KEY=os.getenv("CLIMATIQ_API_KEY")

def main():
    print("Hello world")





if __name__ == "__main__":
    main()