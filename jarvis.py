from core.JarvisTrigger import JarvisTrigger
from core.OrderListener import OrderListener


def main():
    """
    Entry point of jarvis program
    """
    # Wait that the jarvis trigger is pronounced by the user
    jarvis_triger = JarvisTrigger()
    jarvis_triger.start()

if __name__ == '__main__':
    main()
