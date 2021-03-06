import createToken as token
import CYK
import sys
import timeit

if len(sys.argv) > 1:
    fn = str(sys.argv[1])
    start = timeit.default_timer()
    tokenCode = token.createToken(fn)
    #print(tokenCode)
    table = CYK.CYK(tokenCode)
    if (CYK.isSyntaxValid(table, "S")):
        print("\nAccepted")
    else:
        print("\nSyntax error!")
    stop = timeit.default_timer()
    print('Time Execution: ', stop - start, 'sec\n') 
else:
	print("\nInput file name")
	print("\trun command : python parserprogram.py <file_name>\n")