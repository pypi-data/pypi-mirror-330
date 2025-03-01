from dataclasses import dataclass

from ._patch import (
      _patch as patch,
      layer,
      SectionGeometry
)

class Mesh:
    nodes: list
    elems: list

class Material:
    pass 

@dataclass
class _Fiber:
    location: tuple
    area:     float
    warp:     list

@dataclass
class _Element:
    nodes: tuple # of int
  # gauss: tuple # of Gauss
    shape: str
    model: dict = None

@dataclass
class BasicSection:
    iczy: float
    icyy: float
    iczz: float
    area: float


    def centroid(self):
        pass

    def translate(self, location):
        pass


def create_mesh(patches: list, mesh_size: list=None):
    from .solvers import TriangleModel
    from .mesh import sect2gmsh
    mesh = sect2gmsh(patches, mesh_size)
    # meshio object, all tri3s
    GaussT3 = None
    nodes = mesh.points
    elems = [
        _Element(nodes=cell, shape="T3") for cell in mesh.cells[1].data
    ]
    return TriangleModel(nodes, elems) 


def _extract_model(geometry, size)->tuple:
    from .mesh import sect2gmsh
    nodes = {}
    elems = []

    mesh = sect2gmsh(geometry, size)
    # meshio object, all tri3s
    GaussT3 = None
    nodes = mesh.points
    elems = [
        _Element(nodes=cell, gauss=GaussT3, shape="T3") for cell in mesh.cells[1].data
    ]

    return nodes, elems, mesh

def _extract_fibers(geometry, nwarp:int = 0)->list:
    fibers = []
    if isinstance(geometry, list):
        for item in geometry:
            if True:
                fibers.append(_Fiber())

    return fibers

class GeneralSection:
    mesh: "Mesh"

    torsion: "TorsionAnalysis"
    flexure: "FlexureAnalysis"

    _exterior: "list" # of points representing a ring
    _interior: "list" # of rings

    _point_fibers: "list" # of Fiber

    def __init__(self, geometry,
                 warp_twist=True, 
                 warp_shear=True
        ):
        from .solvers import PlaneMesh, TriangleModel, TorsionAnalysis, FlexureAnalysis

        if isinstance(geometry, PlaneMesh):
            self.mesh = geometry
        else:
            nodes, elems, _ = _extract_model(geometry)
            self.mesh = TriangleModel(nodes, elems)

        self._warp_shear:bool = warp_shear 
        self._warp_twist:bool = warp_twist

        nwarp = 0
        if warp_twist:
            nwarp += 1
            self.torsion = TorsionAnalysis(self.mesh)
            # Update fibers
        else:
            self.torsion = None

        if warp_shear is True:
            nwarp += 2
            self.flexure = FlexureAnalysis(self.mesh)
            # Update fibers
        else:
            self.flexure = None

        self._point_fibers = _extract_fibers(geometry, nwarp=nwarp)

    def exterior(self):
        return self.mesh.exterior()

    def interior(self):
        return self.mesh.interior()
    
    def centroid(self):
        return self.torsion.centroid()

    def summary(self, symbols=False):
        s = ""
        tol=1e-13
        A = self.torsion.cnn()[0,0]

        cnm = self.torsion.cnm()
        Ay = cnm[0,1] # int z
        Az = cnm[2,0] # int y
        # Compute centroid
        cx, cy = float(Az/A), float(Ay/A)
        cx, cy = map(lambda i: i if abs(i)>tol else 0.0, (cx, cy))

        cmm = self.torsion.cmm()

        Ivv = self.torsion.cvv()[0,0]
        Irw = self.torsion.cmv()[0,0]

        sx, sy = self.torsion.shear_center()
        sx, sy = map(lambda i: i if abs(i)>tol else 0.0, (sx, sy))

        cww = self.torsion.cww()
        # Translate to shear center to get standard Iww
        Iww = self.translate([sx, sy]).torsion.cww()[0,0]

        Isv = self.torsion.torsion_constant()

        s += f"""
  [nn]  Area                 {A  :>10.4}
  [nm]  Centroid             {cx :>10.4},{cy :>10.4}
  [mm]  Flexural moments  xx {cmm[0,0] :>10.4}
                          yy {cmm[1,1] :>10.4}
                          zz {cmm[2,2] :>10.4}
                          yz {cmm[1,2] :>10.4}

  [mv]                    xx {Irw :>10.4}
        Shear center         {sx :>10.4},{sy :>10.4}
  [ww]  Warping constant     {cww[0,0] :>10.4} ({Iww :>10.4} at S.C.)
        Torsion constant     {Isv :>10.4}
  [vv]  Bishear           xx {Ivv :>10.4}
        """

        return s


    def add_to(self, model, tag):
        pass

    def translate(self, offset):
        # TODO: translate fibers
        return GeneralSection(self.mesh.translate(offset),
                              warp_shear=self._warp_shear,
                              warp_twist=self._warp_twist,
                              ) 

    def rotate(self, angle):
        # TODO: rotate fibers
        return GeneralSection(self.mesh.rotate(angle),
                              warp_shear=self._warp_shear,
                              warp_twist=self._warp_twist,
                              ) 

    def linearize(self)->BasicSection:
        import numpy as np
        y, z = self.mesh.nodes.T
        e = np.ones(y.shape)
        return BasicSection(
            area=self.mesh.inertia(e, e),
            iczy=self.mesh.inertia(y, z),
            icyy=self.mesh.inertia(z, z),
            iczz=self.mesh.inertia(y, y)
        )

    def integrate(self, f: callable):
        pass

    def fibers(self, warp=None):
        for fiber in self._point_fibers:
            yield fiber

        model = self.mesh

        if warp is None:
            twist = self.torsion
            w = self.torsion.solution() #warping() # 
        elif warp == "centroid":
            twist = self.translate(self.torsion.centroid()).torsion
            w = twist.solution()
        elif warp == "shear-center":
            w = self.torsion.warping()
            twist = self.torsion
        elif warp == "shear-center-b":
            twist = self.translate(self.torsion.shear_center()).torsion
            w = twist.solution()
        else:
            raise ValueError

        if callable(self._warp_shear):
            psi = self._warp_shear
        else:
            psi = lambda y,z: 0.0

        for i,elem in enumerate(self.mesh.elems):
            # TODO: Assumes TriangleModel
            yz = sum(model.nodes[elem.nodes])/3
            yield _Fiber(
                location=yz,
                area=model.cell_area(i),
                warp=[
                    [twist.model.cell_solution(i, w), *twist.model.cell_gradient(i,  w)],
                    [0, psi(*yz), 0]
                ]
            )

