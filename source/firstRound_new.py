
def GetAction(points, colors):

       c100 = [['A','A']]

       if points in c100:
              return 100
       
       c90 = [['K','K'],
               ['Q','Q'],
               ['A','K'],
               ['K','A']]
       if points in c90:
              return 90

       c80 = [['J','J'],
              ['10','10'],
              ['9','9'],
              ['A','Q'],
              ['Q','A']]
       
       c80s = [['A','J'],
               ['J','A']]
       
       if points in c80:
              return 80
       elif points in c80s:
              if (colors[0]==colors[1]):
                     return 80
              else:
                     return 70
              

       c70 = [['A','10'],
              ['10','A'],
              ['K','Q'],
              ['Q','K']]

       if points in c70:
              return 70

       c60 = [['8','8'],
              ['7','7'],
              ['6','6']]

       c60s = [['K','J'],
               ['J','K'],
               ['K','10'],
               ['10','K'],
               ['Q','J'],
               ['J','Q'],
               ['Q','10'],
               ['10','Q'],
               ['J','10'],
               ['10','J'],
               ['9','10'],
               ['10','9']]

       if points in c60:
              return 60
       elif points in c60s and colors[0]==colors[1]:
              return 60

       c50 =[['K','J'],
               ['J','K'],
               ['K','10'],
               ['10','K'],
               ['Q','J'],
               ['J','Q'],
               ['Q','10'],
               ['10','Q'],
               ['J','10'],
               ['10','J'],
               ['5','5'],
               ['4','4'],
               ['3','3'],
               ['2','2']]
       
       c50s = [['A','9'],
               ['9','A'],
               ['9','8'],
               ['8','9']]

       if points in c50:
              return 50
       elif points in c50s and colors[0]==colors[1]:
              return 50
       
       if (points[0]=='A' or points[1]=='A') and colors[0]==colors[1]:
              return 40

       return 0
       
       





##ps = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
##cs = ['SP','HE','CL','DI']
##
##i=0
##g= 0
##for p1 in ps:
##       for c1 in cs:
##              for p2 in ps:
##                     for c2 in cs:
##                            if p1==p2 and c1==c2:
##                                   pass
##                            else:
##                                   if GetAction([p1,p2],[c1,c2])>0:
##                                          g+=1
##                                   i+=1
##
##print '---------------------------------'
##print g
##print i
##print float(g)/i
