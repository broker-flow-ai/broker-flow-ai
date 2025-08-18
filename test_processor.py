import os
import sys
import traceback
from config import INBOX_PATH, OUTPUT_PATH

def test_processor():
    print("Testing processor...")
    
    # Check if required directories exist
    print(f"INBOX_PATH: {INBOX_PATH}")
    print(f"OUTPUT_PATH: {OUTPUT_PATH}")
    
    if not os.path.exists(INBOX_PATH):
        print(f"INBOX_PATH does not exist: {INBOX_PATH}")
        return False
        
    if not os.path.exists(OUTPUT_PATH):
        print(f"OUTPUT_PATH does not exist: {OUTPUT_PATH}")
        # Try to create it
        try:
            os.makedirs(OUTPUT_PATH)
            print(f"Created OUTPUT_PATH: {OUTPUT_PATH}")
        except Exception as e:
            print(f"Failed to create OUTPUT_PATH: {str(e)}")
            return False
    
    # Check if there are any PDF files in the inbox
    pdf_files = [f for f in os.listdir(INBOX_PATH) if f.endswith(".pdf")]
    print(f"PDF files in inbox: {pdf_files}")
    
    # Try to import the main module
    try:
        print("Importing main module...")
        import main
        print("Main module imported successfully")
    except Exception as e:
        print(f"Failed to import main module: {str(e)}")
        traceback.print_exc()
        return False
    
    # Try to call process_inbox
    try:
        print("Calling process_inbox...")
        main.process_inbox()
        print("process_inbox completed successfully")
    except Exception as e:
        print(f"Failed to call process_inbox: {str(e)}")
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = test_processor()
        if success:
            print("Processor test completed successfully")
        else:
            print("Processor test failed")
            sys.exit(1)
    except Exception as e:
        print(f"Error in test_processor: {str(e)}")
        traceback.print_exc()
        sys.exit(1)