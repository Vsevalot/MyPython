from math import sqrt
def rectangle_rotation(a, b):
    A=[sqrt(2)*a/2+sqrt(((a/2-b/2)**2)/2),sqrt(((a/2-b/2)**2)/2)]
    B=[A[1],A[0]]
    C=[-A[0],-A[1]]
    D=[-B[0],-B[1]]
    def line(point1,point2,x):
        return ((-point1[1]+point2[1])*x  - point1[0]*point2[1] + point2[0]*point1[1])/(point2[0] - point1[0])
    points=0
    for x in range(-int(A[0]),int(A[0]),1):
        print(line(D,A,x))
        for y in range(int(A[0]),-int(A[0]),-1):
            if (line(D,A,x)>y) and (line(A,B,x)>y) and (line(C,B,x)<y) and (line(C,D,x)<y):
                points+=1
    return points

print(rectangle_rotation(6,4))

a="20090716_09.29.09.mat(5)"

print(a[:8])
