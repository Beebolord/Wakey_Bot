from operator import index

import pandas as pd

if __name__ == '__main__':
    """
    a = [1,3,5,7,9]
    myvar =  pd.Series(a)
    myvar.name = "Integer Set"
    print(myvar)
    print(myvar[1])
    """
    furniture = [350,200,800,150]
    s = pd.Series(furniture,index=["Table","Chair","Sofa","Stool"])
    
    print(s[s > 400].index.tolist())

