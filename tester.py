#tester

import sys

if __name__ == "__main__":
    
    print(f"Arguments count: {len(sys.argv)}")
    
    if(len(sys.argv) != 3):
        print("Needs 3 arguments: tester.py [market data] [algorithm]")
        
    
    
    
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")





