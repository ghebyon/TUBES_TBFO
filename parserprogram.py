import createToken as token
import CYK
import sys
import timeit

if len(sys.argv) > 1:
    fn = str(sys.argv[1])
    start = timeit.default_timer()
    tokenCode = token.createToken(fn)
    table = CYK.CYK(tokenCode)
    if (CYK.isSyntaxValid(table, "S")):
        print("\nCompile success!")
    else:
        print("\nCompile error!")
    stop = timeit.default_timer()
    print('Time Execution: ', stop - start, 'sec\n') 
else:
	print("\nInput file name")
	print("\t run command : python parserprogram.py <file_name>\n")