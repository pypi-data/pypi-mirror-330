from . import OptimalTransport
import numpy as np
from . import intersection
from . import ForwardSelection

def interval_DA(ns, nt, X_, B, S_, h_, a, b):
    Bc = np.delete(np.array(range(ns*nt)), B)

    OMEGA = OptimalTransport.constructOMEGA(ns,nt)
    c_ = np.zeros((ns * nt, 1))
    for i in range(X_.shape[1]-1):
        c_ += (OMEGA.dot(X_[:, [i]])) * (OMEGA.dot(X_[:, [i]]))

    Omega_a = OMEGA.dot(a)
    Omega_b = OMEGA.dot(b)

    w_tilde = c_ + Omega_a * Omega_a
    r_tilde = Omega_a * Omega_b + Omega_b * Omega_a
    o_tilde = Omega_b * Omega_b
    S_B_invS_Bc = np.linalg.inv(S_[:, B]).dot(S_[:, Bc])

    w = (w_tilde[Bc, :].T - w_tilde[B, :].T.dot(S_B_invS_Bc)).T
    r = (r_tilde[Bc, :].T - r_tilde[B, :].T.dot(S_B_invS_Bc)).T
    o = (o_tilde[Bc, :].T - o_tilde[B, :].T.dot(S_B_invS_Bc)).T
    list_intervals = []

    interval = [(-np.inf, np.inf)]
    for i in range(w.shape[0]):
        g3 = - o[i][0]
        g2 = - r[i][0]
        g1 = - w[i][0]
        itv = intersection.solve_quadratic_inequality(g3,g2,g1)

        interval = intersection.interval_intersection(interval, itv)
    return interval

def interval_SFSabs(X, Y, K, lst_SELEC_k, lst_Portho, a, b):
    n_sample, n_fea = X.shape

    A=[]
    B=[]

    I = np.identity(n_sample)   

    for step in range(1, K+1):
        P_pp_Mk_1 = lst_Portho[step - 1]
        Xjk = X[:, [lst_SELEC_k[step][-1]]].copy()
        sign_projk = np.sign(np.dot(Xjk.T , np.dot(P_pp_Mk_1, Y)).item()).copy()
        
        projk = sign_projk*(np.dot(Xjk.T, P_pp_Mk_1)) / np.linalg.norm(P_pp_Mk_1.dot(Xjk))

        # if step == 1:
        A.append(-1*projk[0].copy())
        B.append(0)
        for otherfea in range(n_fea):
            if otherfea not in lst_SELEC_k[step]:

                Xj = X[:, [otherfea]].copy()
                sign_proj = np.sign(np.dot(Xj.T , np.dot(P_pp_Mk_1, Y)).item()).copy()
                proj = sign_proj*(np.dot(Xj.T, P_pp_Mk_1)) / np.linalg.norm(P_pp_Mk_1.dot(Xj))

                A.append(-1*(projk-proj)[0].copy())
                B.append(0)
                A.append(-1*(projk+proj)[0].copy())
                B.append(0)


    A = np.array(A)
    B = np.array(B).reshape((-1,1))

    Ac = np.dot(A,  b)
    Az = np.dot(A,  a)

    Vminus = np.NINF
    Vplus = np.inf

    for j in range(len(B)):
        left = Ac[j][0]
        right = B[j][0] - Az[j][0]

        if abs(right) < 1e-14:
            right = 0
        if abs(left) < 1e-14:
            left = 0
        
        if left == 0:
            if right < 0:
                print('Error')
        else:
            temp = right / left
            if left > 0: 
                Vplus = min(Vplus, temp)
            else:
                Vminus = max(Vminus, temp)
    return Vminus, Vplus
    # return np.around(Vminus, 10), np.around(Vplus, 10)
def interval_SFS(X, Y, K, lst_SELEC_k, lst_Portho, a, b):
    n_sample, n_fea = X.shape
    intervals = [(-np.inf, np.inf)]
    # if K == n_fea:
    #     print('y')
    #     return intervals
    
    I = np.identity(n_sample)  
    for step in range(1, K + 1):
        jk = lst_SELEC_k[-1]
        # print('----',lst_SELEC_k[step])
        X_jk = X[:, sorted(lst_SELEC_k[step])].copy()
        Pjk = I - np.dot(np.dot(X_jk, np.linalg.inv(np.dot(X_jk.T, X_jk))), X_jk.T)

        Pjk_a = Pjk.dot(a)
        Pjk_b = Pjk.dot(b)
        for j in range(n_fea):
            if j not in lst_SELEC_k[step]:
                Mj = lst_SELEC_k[step-1] + [j]
                X_j = X[:, sorted(Mj)].copy()
                Pj = I - np.dot(np.dot(X_j, np.linalg.inv(np.dot(X_j.T, X_j))), X_j.T)
                Pj_a = Pj.dot(a)
                Pj_b = Pj.dot(b)

                g1 = Pjk_a.T.dot(Pjk_a) - Pj_a.T.dot(Pj_a)
                g2 = Pjk_a.T.dot(Pjk_b) + Pjk_b.T.dot(Pjk_a) - Pj_a.T.dot(Pj_b) - Pj_b.T.dot(Pj_a)
                g3 = Pjk_b.T.dot(Pjk_b) - Pj_b.T.dot(Pj_b)
                g1, g2, g3 = g1.item(), g2.item(), g3.item()
                itv = intersection.solve_quadratic_inequality(g3, g2, g1)

                intervals = intersection.interval_intersection(intervals, itv)
    return intervals 


def interval_AIC(X, Y, Portho, K, a, b, Sigma, seed = 0):
    n_sample, n_fea = X.shape

    A = []
    Pka = Portho[K].dot(a) 
    Pkb = Portho[K].dot(b)

    intervals = [(-np.inf, np.inf)] 

    for step in range(1, n_fea + 1):
        if step != K:
            Pja = Portho[step].dot(a)
            Pjb = Portho[step].dot(b)
            g1 = Pka.T.dot(Sigma.dot(Pka)) - Pja.T.dot(Sigma.dot(Pja)) + 2*(K - step)
            g2 = Pka.T.dot(Sigma.dot(Pkb)) + Pkb.T.dot(Sigma.dot(Pka)) - Pja.T.dot(Sigma.dot(Pjb)) - Pjb.T.dot(Sigma.dot(Pja))
            g3 = Pkb.T.dot(Sigma.dot(Pkb)) - Pjb.T.dot(Sigma.dot(Pjb))

            g1, g2, g3 = g1.item(), g2.item(), g3.item()

            itv = intersection.solve_quadratic_inequality(g3, g2, g1, seed)

            intervals = intersection.interval_intersection(intervals, itv)
    return intervals 
def interval_BIC(X, Y, Portho, K, a, b, Sigma, seed = 0):
    n_sample, n_fea = X.shape

    A = []
    Pka = Portho[K].dot(a) 
    Pkb = Portho[K].dot(b)

    intervals = [(-np.inf, np.inf)] 

    for step in range(1, n_fea + 1):
        if step != K:
            Pja = Portho[step].dot(a)
            Pjb = Portho[step].dot(b)
            g1 = Pka.T.dot(Sigma.dot(Pka)) - Pja.T.dot(Sigma.dot(Pja)) + np.log(n_sample)*(K - step)
            g2 = Pka.T.dot(Sigma.dot(Pkb)) + Pkb.T.dot(Sigma.dot(Pka)) - Pja.T.dot(Sigma.dot(Pjb)) - Pjb.T.dot(Sigma.dot(Pja))
            g3 = Pkb.T.dot(Sigma.dot(Pkb)) - Pjb.T.dot(Sigma.dot(Pjb))

            g1, g2, g3 = g1.item(), g2.item(), g3.item()

            itv = intersection.solve_quadratic_inequality(g3, g2, g1, seed)

            intervals = intersection.interval_intersection(intervals, itv)
    return intervals 

def interval_AdjustedR2(X, Y, Portho, K, a, b, Sigma, seed = 0):
    n_sample, n_fea = X.shape

    A = []
    Pka = Portho[K].dot(a) 
    Pkb = Portho[K].dot(b)

    intervals = [(-np.inf, np.inf)] 
    ljk = 1/(n_sample - K - 1)
    for step in range(1, n_fea + 1):
        if step != K:
            lj = 1/(n_sample - step - 1)
            Pja = Portho[step].dot(a)
            Pjb = Portho[step].dot(b)
            g1 = ljk*Pka.T.dot(Pka) - lj*Pja.T.dot(Pja)
            g2 = ljk*Pka.T.dot(Pkb) + ljk*Pkb.T.dot(Pka) - lj*Pja.T.dot(Pjb) - lj*Pjb.T.dot(Pja)
            g3 = ljk*Pkb.T.dot(Pkb) - lj*Pjb.T.dot(Pjb)

            g1, g2, g3 = g1.item(), g2.item(), g3.item()

            itv = intersection.solve_quadratic_inequality(g3, g2, g1, seed)

            intervals = intersection.interval_intersection(intervals, itv)
    return intervals 
def OC_Crit_interval(ns, nt, a, b, XsXt_, Xtilde, Ytilde, Sigmatilde, B, S_, h_, SELECTION_F, GAMMA,k,seed = 0):

    lst_SELECk, lst_P = ForwardSelection.list_residualvec(Xtilde, Ytilde)

    itvDA = interval_DA(ns, nt, XsXt_, B, S_, h_, a, b)
    itvFS = interval_SFS(Xtilde, Ytilde, 
                                    len(SELECTION_F),
                                    lst_SELECk, lst_P,
                                    GAMMA.dot(a), GAMMA.dot(b))
    if k == 'AIC':
        itvCriterion = interval_AIC(Xtilde, Ytilde, 
                                        lst_P, len(SELECTION_F), 
                                        GAMMA.dot(a), GAMMA.dot(b), Sigmatilde, seed)
    elif k == 'BIC':
        itvCriterion = interval_BIC(Xtilde, Ytilde, 
                                        lst_P, len(SELECTION_F),
                                        GAMMA.dot(a), GAMMA.dot(b), Sigmatilde, seed)
    elif k == 'Adjusted R2':
        itvCriterion = interval_AdjustedR2(Xtilde, Ytilde, 
                                    lst_P, len(SELECTION_F),
                                    GAMMA.dot(a), GAMMA.dot(b), Sigmatilde, seed)

    finalinterval = intersection.interval_intersection(itvDA, itvFS) 
    finalinterval = intersection.interval_intersection(finalinterval, itvCriterion)
    # print(f"da: {itvDA} | fs: {itvFS} | aic: {itvCriterion}")
    return finalinterval
def OC_fixedFS_interval(ns, nt, a, b, XsXt_, Xtilde, Ytilde, Sigmatilde, B, S_, h_, SELECTION_F, GAMMA,):

    lst_SELECk, lst_P = ForwardSelection.list_residualvec(Xtilde, Ytilde)

    itvDA = interval_DA(ns, nt, XsXt_, B, S_, h_, a, b)
    itvFS = interval_SFS(Xtilde, Ytilde, 
                                    len(SELECTION_F),
                                    lst_SELECk, lst_P,
                                    GAMMA.dot(a), GAMMA.dot(b))
    # print(itvDA, itvFS)
    finalinterval = intersection.interval_intersection(itvDA, itvFS) 
    return finalinterval, itvDA, itvFS


def OC_FS_AIC_nonDA(n,a,b,X,Y,Sigma,SELECTION_F):
    lst_SELECk, lst_P = ForwardSelection.list_residualvec(X, Y)
    # print(lst_SELECk)
    itvFS = interval_SFS(X, Y, len(SELECTION_F), lst_SELECk, lst_P, a, b)
    itvAIC = interval_AdjustedR2(X, Y, lst_P, len(SELECTION_F), a, b, Sigma)

    # finalinterval = intersection.interval_intersection(itvDA, itvFS) 
    finalinterval = intersection.interval_intersection(itvFS, itvAIC)
    # print(f"fs: {itvFS} | aic: {itvAIC}")
    return finalinterval