try:
    import selenium
    print(f"Selenium version: {selenium.__version__}")
    print("Selenium is installed correctly!")
except ImportError:
    print("Selenium is not installed in the current environment")