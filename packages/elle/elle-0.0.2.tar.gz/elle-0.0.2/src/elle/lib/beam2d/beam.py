import jax.numpy as jnp
from functools import partial 


class Beam: pass

def beam(rel=None):
    if rel is None:
        ah = jnp.eye(3)
    else:
        ah = _ah(rel)



    def f(u,xyz,E,A,I):
        """return element local stiffness Matrix"""
        DX = xyz[1,0] - xyz[0,0]
        DY = xyz[1,1] - xyz[0,1]
        L = jnp.linalg.norm([DX,DY])

        EI = E*I
        k = jnp.array([[E*A/L,    0   ,   0   ],
                       [  0  , 4*EI/L , 2*EI/L],
                       [  0  , 2*EI/L , 4*EI/L]])
        f = ah.T @ k @ ah @ u
        return f
    obj = Beam()
    obj.f = f
    obj.Df = Df
    return  obj

def _ah(rel):
    MR = [1 if x else 0 for x in rel]
    ah = jnp.array([[1-MR[0],          0          ,             0        ],
                   [   0   ,       1-MR[1]       ,  -0.5*(1-MR[2])*MR[1]],
                   [   0   , -0.5*(1-MR[1])*MR[2],          1-MR[2]     ]])
    return ah


def beam_2d_stiffness(rel=None,**kwds):
    if rel is None:
        ah = jnp.eye(3)
    else:
        ah = _ah(rel)

    def Df(u,xyz,E,A,I):
        """return element local stiffness Matrix"""
        DX = xyz[1,0] - xyz[0,0]
        DY = xyz[1,1] - xyz[0,1]
        L = jnp.linalg.norm([DX,DY])

        EI = E*I
        k = jnp.array([[E*A/L,    0   ,   0   ],
                        [  0  , 4*EI/L , 2*EI/L],
                        [  0  , 2*EI/L , 4*EI/L]])
        k = ah.T @ k @ ah
        return k

    return partial(Df,**kwds)    


def linear_transform(xyz):
    L = jnp.linalg.norm(xyz)
    cs, sn = (xyz[1] - xyz[0])/L
    ag = jnp.array([[ -cs ,  -sn , 0,  cs ,   sn , 0],
                   [-sn/L,  cs/L,  1, sn/L, -cs/L, 0],
                   [-sn/L,  cs/L,  0, sn/L, -cs/L, 1]])
    return ag

