def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "run":
        print("Hello")
    else:
        print("Usage: demo-client run")
        sys.exit(1)