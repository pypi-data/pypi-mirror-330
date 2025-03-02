from splash import Splash

def test_splash():
    logger = Splash(prefix="Test")
    
    print("\n--- Testing Classic Mode ---\n")
    logger.success("Success message")
    logger.warning("Warning message")
    logger.info("Info message")
    logger.error("Failure message")
    logger.debug("Debug message")
    logger.captcha("Captcha")
    
    print("\n--- Testing Minimal Mode ---\n")
    logger_minimal = Splash(mode="minimal", separator="→")
    logger_minimal.success("Minimal success message")
    logger_minimal.warning("Minimal warning message")
    logger_minimal.info("Minimal info message")
    logger_minimal.error("Minimal failure message")
    logger_minimal.captcha("Captcha")
    
if __name__ == "__main__":
    test_splash()