#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 10:28:04 2019

@author: sadra

We have three type of objects:
    * H-polytopes
    * Zonotopes
    * AH-polytopes
"""
# Numpy
import numpy as np
# Pypolycontain
from pypolycontain.utils.utils import unique_rows

class H_polytope():
    def __init__(self,H,h):
        """
        Class Polytope. A Polytope is defined as (x \in R^n | Hx <= h)
        """
        if h.shape[1]!=1:
            ValueError("Error: not appropriate h size, it is",h.shape)
        if H.shape[0]!=h.shape[0]:
            ValueError("Error: not consistent dimension of H: %d and h: %d"%(H.shape[0],h.shape[0]))
        self.type="H_polytope"
        self.H,self.h=unique_rows(H,h)
        self.n=H.shape[1]
        self.hash_value = None

    def __repr__(self):
        return ("polytope in R^%d"%self.n)

    def __hash__(self):
        if self.hash_value is None:
            self.hash_value = hash(str(np.hstack([self.H, self.h])))
        return self.hash_value

    def if_inside(self,x,tol=10**-5):
        if x.shape[0]!=self.H.shape[1]:
            return ValueError("H and x dimensions mismatch")
        return all(np.dot(self.H,x)<=self.h+tol)
    
class zonotope():
    """
    Definition of a Zonotope
    """
    def __init__(self,x,G,name=None,color=None):
        self.x=x
        self.G=G
        if name==None:
            self.name="zonotope"
        else:
            self.name=name
        try:
            assert color!=None
            self.color=color
        except:
            self.color=(np.random.random(),np.random.random(),np.random.random())
        self.type="zonotope"
        self.hash_value = hash(str(np.hstack([self.G, x])))

    def __repr__(self):
        return self.name

    def __hash__(self):
        if self.hash_value is None:
            self.hash_value = hash(str(np.hstack([self.G, self.x])))  # FIXME: better hashing implementation
        return self.hash_value
    
class AH_polytope():
    """
    Affine Transformation of an H-polytope
    Attributes:
        P: The underlying H-polytope P:{x in R^q | Hx \le h}
        T: R^(n*q) matrix: linear transformation
        t: R^{n*1) vector: translation
    """
    def __init__(self,T,t,P):
        """
        Initilization: T,t,P. X=TP+t
        """
        self.T=T # Matrix n*n_p
        self.t=t # vector n*1
        self.P=P # Polytope in n_p dimensions
        self.n=T.shape[0]
        if T.shape[1]!=P.H.shape[1]:
            ValueError("Error: not appropriate T size, it is",T.shape[1],P.n)
        self.type="AH_polytope"
        self.method="Gurobi"
        self.hash_value = None

    def __repr__(self):
        return "AH_polytope from R^%d to R^%d"%(self.P.n,self.n)

    def __hash__(self):
        if self.hash_value is None:
            self.hash_value = hash(self.P) + hash(str(np.hstack([self.T, self.t])))  # FIXME: better hashing implementation
        return self.hash_value
    
def Box(N,d=1,corners=None):
    """
    returns N-dimensional Box 
    corners=typle of 2 numpy arrays: lower_corner and upper_corner
    """
    H=np.vstack((np.eye(N),-np.eye(N)))
    if corners==None:
        h=d*np.ones((2*N,1))
    else:
        l,u=corners[0:2]
        if not all(u>=l):
            raise ValueError("Upper-right corner not totally ordering lower-left corner")
        h=np.vstack((u,-l))
    return H_polytope(H,h)