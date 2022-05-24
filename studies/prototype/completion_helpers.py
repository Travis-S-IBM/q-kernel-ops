# The contents of this file were originally created by Annie Naveh of Woodside Energy
# in the process of doing research for the paper "Kernel Matrix Completion for Offline Quantum-Enhanced Machine Learning".

import numpy as np
import math
import matplotlib.pyplot as plt
import chompack as cp
from cvxopt import matrix, spmatrix, sparse, normal, solvers, blas, amd, mul
from statsmodels.stats.correlation_tools import corr_clipped
from scipy import linalg as LA
from scipy.linalg import block_diag

import itertools
import time

## network plotting tools
import networkx as nx
import matplotlib as mpl
from kernel_helpers import kernel_samples, erank

def PSD_cliques(M_sparse):
    sym = cp.symbolic(M_sparse,  p=cp.maxcardsearch(M_sparse))
    snrowidx = sym.snrowidx
    sncolptr = sym.sncolptr
    i = 0
    while not np.all([np.all(np.linalg.eigvals(np.array(matrix(cp.symmetrize((M_sparse[snrowidx[sncolptr[k]:sncolptr[k+1]],snrowidx[sncolptr[k]:sncolptr[k+1]].T])))))> -1e-15) for k in range(sym.Nsn-1,-1,-1)]):
        i += 1
        if(i >= 100):
            print("Maximum iterations reached!")
            break
        for k in range(sym.Nsn-1,-1,-1):
            beta  = snrowidx[sncolptr[k]:sncolptr[k+1]]
            M_sparse[beta,beta.T] = corr_clipped(np.array(matrix(M_sparse[beta,beta.T])))
        
    return M_sparse

        
def plot_image(A):
    plt.imshow(A,vmin=0, vmax=1)
    plt.colorbar()

def MCANS(L, thresh = 1e-10):
    L_hat = np.zeros(L.shape)
    calls = 0
    
    L_hat[0,0] = 1
    for j in range(1,len(L)):
        L_hat[j,0] = L[j,0]
        L_hat[0,j] = L_hat[j,0]
        L_hat[j,j] = 1 #doesn't count as a call to the oracle as we already know this
        calls += 1
        
    C = np.array([0])
    
    for c in range(1,len(L)):
        C_temp = np.append(C,c)
        submatrix = L_hat[np.ix_(C_temp, C_temp)]
        if min(LA.svdvals(submatrix)) > thresh:
            C = C_temp
            L_hat[:,c] = L[:,c]
            L_hat[c,:] = L_hat[:,c]
            calls += len(L) - len(C_temp)
            
        #if len(C) == r:
        #    break

    #print("Number of calls to oracle: "+ str(calls))
    #print("Independent columns: "+ str(C))
    W = L_hat[np.ix_(C, C)]
    L_hat = L_hat[:,C].dot(np.linalg.inv(W)).dot(np.matrix.transpose(L_hat[:,C]))
    return L_hat, C, calls

def calc_error(A, A_hat):
    return np.linalg.norm(A - A_hat, "fro") / np.linalg.norm(A, "fro")

def calc_unseen_error(A, A_hat, indices):
    n = A.shape[0]
    unseenEntries = list(set(zip(np.tril_indices(n)[0],np.tril_indices(n)[1])) - set(indices))
    if unseenEntries == []:
        return 0        
    diff = math.sqrt(sum((A - A_hat)[tuple(zip(*unseenEntries))]**2))  # only consider lower half 
    norm = math.sqrt(sum(A[tuple(zip(*unseenEntries))]**2))
    if norm == 0 and diff == 0:
        return 0
    else:
        return diff/norm
    
    
# another error for the KL divergence between the inverse of the solution and the sparse matrix

# define entries of band diagonal
def band_sparsity(q,n):
    u_arrays = np.triu_indices(n,k=-q)
    l_arrays = np.tril_indices(n,k= 0)
    entries_u = list(zip(u_arrays[0],u_arrays[1]))
    entries_l = list(zip(l_arrays[0],l_arrays[1]))
    indices = list(set(entries_u).intersection(entries_l))
    callsPercent = round((len(indices)-n)/len(np.tril_indices(n,k=-1)[0]) *100,2)
    #print("% of calls to the quantum computer: " + str(callsPercent) + '%')
    return indices, callsPercent

def blockArrow_sparsity(q,c,n):
    u_arrays = np.triu_indices(n,k=-q)
    l_arrays = np.tril_indices(n,k= 0)
    entries_l = list(zip(l_arrays[0],l_arrays[1]))
    entries_u = list(zip(u_arrays[0],u_arrays[1]))+ [x for x in entries_l if x[1] in list(range(c))]
    indices = list(set(entries_u).intersection(entries_l))
    callsPercent = round((len(indices)-n)/len(np.tril_indices(n,k=-1)[0]) *100,2)
    #print("% of calls to the quantum computer: " + str(callsPercent) + '%')
    return indices, callsPercent

def diagBlocks_sparsity(l,n,k=0):
    u = n%l + k*l
    N =int((n-u)/l + u)
    #print('clique order = ' + str(N))
    #print('overlap = ' + str(round(u,2)))
    b = [np.ones((N,N))]*int(l)
    blockDiag = np.where(block_diag(*b) ==1)
    entries_diag_overlap = [(blockDiag[0][i] - blockDiag[0][i]//N * u, blockDiag[1][i] - blockDiag[1][i]//N * u) for i in range(len(blockDiag[0]))]
    
    l_arrays = np.tril_indices(n,k=0)
    entries_l = list(zip(l_arrays[0],l_arrays[1]))
    indices = list(set(entries_diag_overlap).intersection(entries_l))
    callsPercent = round((len(indices)-n)/len(np.tril_indices(n,k=-1)[0]) *100,2)
    #print("% of calls to the quantum computer: " + str(callsPercent) + '%')
    return indices, callsPercent

def extend_sparsity(k,M,n):
    b = [np.ones((n-k,n-k))]
    blockDiag = np.where(block_diag(*b) ==1)
    
    b2 = [np.ones((k,k))]
    blockDiag2 = np.where(block_diag(*b2) ==1)
    
    l_arrays = np.tril_indices(n,k=0)
    
    entries_l = list(zip(l_arrays[0],l_arrays[1]))
    indices = list(set(list(zip(blockDiag[0],blockDiag[1]))).union(set(zip(blockDiag2[0]+(n-k),blockDiag2[1]+(n-k)))).union(set(list(itertools.product(range(n-k,n),range(n-k-M,n-k))))).intersection(entries_l))
    callsPercent = round((len(indices)-n)/len(np.tril_indices(n,k=-1)[0]) *100,2)
    return indices, callsPercent

def rand_maxcardsearch(p,n):
    x = []
    I = []
    J = []
    i_arrays = np.tril_indices(n,k=-1)
    entries = list(zip(i_arrays[0],i_arrays[1]))
    sample = np.random.default_rng(0).choice(entries, int(len(entries)*p/100), replace = False)
    for i in range(len(sample)):
        x.append(1.0)
        I.append(int(sample[i][0]))
        J.append(int(sample[i][1]))
    for i in range(n):
        x.append(1.0)
        I.append(i)
        J.append(i)
    M_sparse = spmatrix(x,I,J)
    M_sparse = cp.maxchord(M_sparse,n-1)[0]
    #print("Does perfect elimination order exist: " + str(cp.peo(M_sparse,pmcs)))    
    sym = cp.symbolic(M_sparse,  p=cp.maxcardsearch(M_sparse))
    randChordal = np.where(np.array(matrix(sym.sparsity_pattern()))==1)
    l_arrays = np.tril_indices(n,k= 0)
    entries_u = list(zip(randChordal[0],randChordal[1]))
    entries_l = list(zip(l_arrays[0],l_arrays[1]))
    indices = list(set(entries_u).intersection(entries_l))
    callsPercent = round((len(indices)-n)/len(np.tril_indices(n,k=-1)[0]) *100,2)
    #print("% of calls to the quantum computer: " + str(callsPercent) + '%')
    return indices, callsPercent
    
def create_spmatrix(M,indices):
    x = []
    I = []
    J = []
    for i in range(len(indices)):
        x.append(M[tuple(indices[i])])
        I.append(int(indices[i][0]))
        J.append(int(indices[i][1])) 
    M_sparse = spmatrix(x,I,J)
    M_sparse = cp.maxchord(M_sparse,M_sparse.size[0]-1)[0]
    return M_sparse

def symbolic_factorisation(M_sparse):
    n= M_sparse.size[0]
    pmcs = cp.maxcardsearch(M_sparse)
    #print("Does perfect elimination order exist: " + str(cp.peo(M_sparse,pmcs)))
    sym = cp.symbolic(M_sparse,  p=pmcs)
    #print("Number of cliques i.e. minimum rank: " +str(sym.clique_number)+'\n')
    L = cp.cspmatrix(sym)
    L += M_sparse
    return L

def chordalCompletion(L,completiontype):
    if completiontype == 'mr':
        Y_complete_mr = cp.mrcompletion(L, reordered=False)      
        M_complete = Y_complete_mr*(Y_complete_mr.T)
    elif completiontype == 'det':
        M_complete = cp.psdcompletion(L, reordered=False)
    return M_complete

def sparsity_graph(sym):
    cliques = sym.cliques()
    
    print("   Cliques")
    for k,sk in enumerate(cliques):
        print( str(sk))
    G = nx.Graph()
    G.add_nodes_from(range(sym.n))
    for k in range(sym.Nsn):
        ck = sym.snrowidx[sym.sncolptr[k]:sym.sncolptr[k+1]]
        G.add_edges_from([(ck[i],ck[j]) for i in range(len(ck)) for j in range(i,len(ck))])
    fig = nx.draw(G, with_labels=True, font_weight='bold',node_color='y')
    return fig

def etree_graph(sym):
    par = sym.parent()
    snodes = sym.supernodes()
    print("\nId  Parent id  Supernode")
    for k,sk in enumerate(snodes):
        print("%2i     %2i     "%(k,par[k]), sk)
    G = nx.DiGraph()
    G.add_nodes_from(range(sym.Nsn))
    G.add_edges_from([(sym.snpar[k],k) for k in range(sym.Nsn) if sym.snpar[k] != k ])
    #pos=graphviz_layout(G, prog='dot')
    fig = nx.draw(G,with_labels=True, arrows=False, node_size=500, node_color='w', node_shape='s', font_size=14)
    return fig
