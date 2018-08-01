def vec_x_float(vector,float):
    return [vector[0]*float,vector[1]*float]
def add(*args):
    result = [0,0]
    for vec in args:
        result[0] += vec[0]
        result[1] += vec[1]
    return result
def distance(vectora, vectorb ):
    return ((vectora[0]-vectorb[0])**2 + (vectora[1]-vectorb[1])**2)**(1.0/2)
def sub(vec1,vec2):
    return [vec1[0]-vec2[0],vec1[1]-vec2[1]]
def nor(vec):
    if vec[0] > 0:
        return [vec[0]/abs(vec[0]), vec[1]/abs(vec[0])]
    elif vec[1] > 0:
        return [vec[0]/abs(vec[1]), vec[1]/abs(vec[1])]
    else:
        return [1,1]
