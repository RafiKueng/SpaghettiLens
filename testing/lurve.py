class Lurve:

    def __init__(self,canv,loc):
        self.canv = canv
        self.M = [loc[0],loc[1]/2,loc[2]/2]
        self.next = [None,None,None]
        self.par = [None,1,1]
        H = 8
        W = 2*H-1
        self.H = H
        self.W = W
        r = W*[0j]
        for k in range(1,H):
            r[k] = 1-exp(2j*pi*k/H)
            r[k+W/2] = 1-exp(2j*pi*k/H)
        self.r = r
        self.z = W*[0j]
        
    def more(self,k):
        M = self.M
        loc = [M[0]+M[k],M[1],M[2]]
        r = abs(M[1]/M[2])
        if k==1 and r < 1:
            loc[1] *= r
            loc[2] *= r
        if k==2 and r > 1:
            loc[1] /= r
            loc[2] /= r
        self.next[k] = Lurve(self.canv,loc)

    def undo(self,loop):
        for k in (1,2):
            if self.next[k]:
                if self.next[k]==loop:
                    self.next[k] = None
                    break
                self.next[k].undo(loop)


    def refresh(self,opar=1):
        H = self.H
        W = self.W
        M = self.M
        r = self.r
        z = self.z
        next = self.next
        for k in (1,2):
            if next[k]:
                M[k] = next[k].M[0] - M[0]  # reset from lower level
        z[0] = M[0]
        par = [None,opar,opar]
        if (M[2]/M[1]).real > 0:
            if abs(M[1]) < abs(M[2]):
                par[1] *= -1
            else:
                par[2] *= -1
        self.par = par
        for k in range(1,W):
            if k < H:
                z[k] = M[0] + M[1] * r[k]
            else:
                if par[1]*par[2] == -1:
                    z[k] = M[0] + M[2] * r[k]
                else:
                    z[k] = M[0] + M[2] * r[k].conjugate()
        self.trace(z,H)
        if next[1]:
            next[1].refresh(par[1]);
        if next[2]:
            next[2].refresh(par[2]);

    def trace(self,z,H):
        self.curv(z,0,1,-1,2)
        self.curv(z,1,2,0,3)
        for k in range(2,H-2):
            self.curv(z,k,k+1,k-1,k+2)
        self.curv(z,H-2,H-1,H-3,0)
        self.curv(z,H-1,0,H-2,H)
        self.curv(z,0,H,H-1,H+1)
        self.curv(z,H,H+1,0,H+2)
        for k in range(H+1,2*H-3):
            self.curv(z,k,k+1,k-1,k+2)
        self.curv(z,-2,-1,-3,0)
        self.curv(z,-1,0,-2,1)
            
    def point(self,z,r=2,col="white"):
        x = z.real
        y = z.imag
        self.canv.create_oval(x-r,y-r,x+r,y+r,outline=col,fill=col)


    def bezier(self,a,am,bp,b):
        for n in range(11):
            t = 0.1*n
            w = a + t*(b-a)
            w = (1-t)**3 * a + 3*(1-t)**2*t * am + 3*(1-t)*t**2 * bp + t**3 * b
            if n > 0:
                self.canv.create_line(wo.real,wo.imag,w.real,w.imag,
                                      fill="white")
            wo = w


    def curv(self,z,i,j,k,l):
        a = z[i]
        b = z[j]
        am = a + 0.2*(b - z[k])
        bp = b + 0.2*(a - z[l])
        self.point(a)
        self.point(b)
        self.bezier(a,am,bp,b)
        M = self.M
        self.point(M[0],r=6,col='magenta')
        for k in (1,2):
            if not self.next[k]:
                if self.par[k]==1:
                    self.point(M[0]+M[k],r=6,col='red')
                if self.par[k]==-1:
                    self.point(M[0]+M[k],r=6,col='yellow')

    def closep(self,w):
        M = self.M
        loop,ix,ds = (self,0,abs(M[0]-w))
        for k in (1,2):
            if self.next[k]:
                child,k,dstry = self.next[k].closep(w)
                if dstry < ds:
                    loop,ix,ds = (child,k,dstry)
            else:
                dstry = abs(M[0]+M[k]-w)
                if dstry < ds:
                    loop,ix,ds = (self,k,dstry)
        return (loop,ix,ds)

    def closez(self,w):
        M = self.M
        z = self.z
        loop,ix,ds = (self,1,abs(z[1]-w))
        for k in range(2,self.W):
            dstry = abs(z[k]-w)
            if dstry < ds:
                loop,ix,ds = (self,k,dstry)
        for k in (1,2):
            if self.next[k]:
                child,k,dstry = self.next[k].closez(w)
                if dstry < ds:
                    loop,ix,ds = (child,k,dstry)
        return (loop,ix,ds)

def moved(event):
    w = event.x + 1j*event.y
    loop,q,ds = lemur.closep(w)
    loopz,qz,dsz = lemur.closez(w)
    if ds > 20 and dsz > 20:
        return
    if ds < dsz:
        M = loop.M
        if q == 0:
            M[1] += M[0] - w
            M[2] += M[0] - w
            M[0] = w
        else:
            M[q] += w - (M[q]+M[0])
    else:
        M = loopz.M
        r = loopz.r
        par = loopz.par
        if qz < loopz.H:
            r[qz] = (w - M[0])/M[1]
        else:
            r[qz] = (w - M[0])/M[2]
            if par[1]*par[2] == 1:
                r[qz] = r[qz].conjugate()
    draw()


def dclick(event):
    w = event.x + 1j*event.y
    loop,ix,ds = lemur.closep(w)
    if ds > 20:
        return
    if ix > 0:
        loop.more(ix)
    else:
        lemur.undo(loop)
    draw()


def draw():
    canv.delete(ALL)
    if img:
        canv.create_image(0, 0, anchor=NW, image=img)
    lemur.refresh(1)

from numpy import pi, exp
from Tkinter import *
import sys

root = Tk()
canv = Canvas(root, width=541, height=541, background="black")
lemur = Lurve(canv,[300+300j,-200+0j,-50+0j])
canv.bind("<B1-Motion>", moved)
canv.bind("<Double-Button-1>", dclick)

cas = ["irchel","HE1104Hcc","SBS1520Hcc",
       "Q2237Hcc","PG1115Hcc","B1422Hcc","RXJ0911Hcc",
       "serendib","J1148+193","J0022+143"]

if len(sys.argv) > 1:
    fname = cas[int(sys.argv[1])]
    img=PhotoImage(file="images/"+fname+".gif")
else:
    img = None

canv.pack()
draw()
root.mainloop()

