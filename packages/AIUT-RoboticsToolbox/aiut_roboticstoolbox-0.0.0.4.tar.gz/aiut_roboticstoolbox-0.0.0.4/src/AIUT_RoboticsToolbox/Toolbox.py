#In the Name of Allah
        plt.show()
        return 

    
class Puma560(SerialLink):
    def __init__(self,name):
        self.name = name
        a2 = 43.2
        a3 = 0    #10
        d3 = 0    #23.3
        d4 = 43.2
        self.links = [[0.0,     0.0,   0.0,  0.0, 0],
                      [-np.pi/2,0.0,   0.0,  0.0, 0],
                      [0.0,     a2,    d3,   0.0, 0],
                      [-np.pi/2,a3,    d4,   0.0, 0],
                      [np.pi/2, 0.0,   0.0,  0.0, 0],
                      [-np.pi/2,0.0,   0.0,  0.0, 0]]
        SerialLink.__init__(self,self.name,self.links)

#scara robot Friday 1402/2/8
class SCARA(SerialLink):
    def __init__(self,name,l1,l2):
        self.name = name
        self.l1 = l1
        self.l2 = l2
        self.links = [[0.0,     0.0,   0.0,  0.0, 0],
                      [0.0,     l1,    0.0,  0.0, 0],
                      [0.0,     l2,    0.0,  0.0, 0],
                      [np.pi,   0.0,   0.0,  0.0, 1]]
        SerialLink.__init__(self,self.name,self.links)


    def invKin(self,T,type='r'):
        results = []
        theta123 = math.atan2(T[1][0],T[0][0])
        d4 = -T[2][3]
        x = T[0][3]
        y = T[1][3]
        c2 = (x*x+y*y-self.l1*self.l1-self.l2*self.l2)/(2*self.l1*self.l2)
        if (c2 < -1 or c2 > 1):
            print('invalid location')
            return []     
        s2 = math.sqrt(1-c2*c2)
        theta2 = math.atan2(s2,c2)
        k1 = self.l1 + self.l2*c2
        k2 = self.l2*s2
        theta1 = math.atan2(y,x) - math.atan2(k2,k1)
        theta3 = theta123 - theta1 - theta2
        if type == 'r':   #use radians
            joints = [theta1,theta2,theta3,d4]
        elif type == 'd': #use degrees
            joints = [self.toDeg(theta1),self.toDeg(theta2),self.toDeg(theta3),d4]            
        results.append(joints)
        
        s2 = -s2
        theta2 = math.atan2(s2,c2)
        k1 = self.l1 + self.l2*c2
        k2 = self.l2*s2
        theta1 = math.atan2(y,x) - math.atan2(k2,k1)
        theta3 = theta123 - theta1 - theta2
        if type == 'r':  #use radians
            joints = [theta1,theta2,theta3,d4]
        elif type == 'd': #use degrees
            joints = [self.toDeg(theta1),self.toDeg(theta2),self.toDeg(theta3),d4]
        results.append(joints)
        
        return results