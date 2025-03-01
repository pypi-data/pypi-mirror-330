

class MomentCurvatureAnalysis:
    @staticmethod
    def solve_eps(sect, kap, axial: float, eps0, tol=1e-6, maxiter=25):
        # Newton-Raphson iteration
        eps = eps0
        s = sect.getStressResultant([eps, kap], False)
        for i in range(maxiter):
            if abs(s[0] - axial) < tol:
                return eps
            s = sect.getStressResultant([eps, kap], False)
            eps -= (s[0] - axial)/sect.getSectionTangent()[0,0]
        return eps

    def __init__(self, axial):
        pass


class MaterialLocus:
    def __init__(self, section, axial):
        self.axial = axial
        self.section = section

    def plot(self):
        pass

    def analyze(self, nstep = 30, incr=5e-6):
        import matplotlib.pyplot as plt
        import numpy as np
        fig, ax = plt.subplots(1,2, constrained_layout=True)
        sect = self.section
        axial = self.axial

        if sect.name is None:
            sect.name = 1

        solve_eps = MomentCurvatureAnalysis.solve_eps

        # Curvature increment
        dkap = incr
        for P in axial:
            with sect as s:
                k0 = 0.0
                e0 = solve_eps(s,  k0,  P,  solve_eps(s,  k0,  P,  0.0))
                PM = [
                    s.getStressResultant([e0, k0], True),
                    s.getStressResultant([solve_eps(s, k0+dkap, P, e0), k0+dkap], True),
                ]
                e = e0
                kap = 2*dkap
                for _ in range(nstep):
                    if abs(PM[-1][1]) < 0.995*abs(PM[-2][1]):
                        break
                    e = solve_eps(s, kap, P, e)
                    PM.append(s.getStressResultant([e, kap], True))
                    kap += dkap

            p, m = zip(*PM)

            ax[0].plot(np.linspace(0.0, kap, len(m)), m)

            ax[1].scatter(m, p, s=0.2, color="k")

        ax[1].set_ylabel("Axial force, $P$")
        ax[1].set_xlabel("Moment, $M$")

        plt.show()
