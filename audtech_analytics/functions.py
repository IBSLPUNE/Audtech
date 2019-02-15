def missing_values(l):
    aa = list(x+1 for x,y in zip(l[:-1],l[1:]) if y-x > 1 )
    return aa
import re 
import datetime
import string
import numpy as np
import pandas as pd
def removePunct(stri):
    # punctuations = '''!()[]{};:'"\,<>.?@#$%^&*_~'''
    if type(stri) != str:
        print("================"+str(stri))
        return stri
    else:
        stri=str(stri).strip("  ")
        stri= re.sub(r'[^\w\s]','',stri)
        print("+++++++"+stri)
        return stri
def ImportFunc(x,y):
    y="FinalTable.objects.create(%s=%s,x=y)"%(x,y)
    exec(y)