# Statistical Inference for Sequential Feature Selection after Domain Adaptation 

This package provides a statistical inference framework for sequential feature selection (SeqFS) after domain adaptation (DA). It leverages the SI framework and employs a divide-and-conquer strategy to efficiently compute the p-value of selected features. Our method ensures reliable feature selection by controlling the false positive rate (FPR) while simultaneously maximizing the true positive rate (TPR), effectively reducing the false negative rate (FNR).

*For more details, refer to the paper at https://arxiv.org/abs/2501.09933*

Note: This package utilizes the scipy package to solve linear programming problems using the simplex method. However, the default scipy package does not provide the set of basic variables in its output. To address this limitation, we slightly modified the package so that it can return the set of basic variables by replacing the two files '_linprog.py' and '_linprog_simplex.py' in scipy.optimize module with our modified files in the folder 'files_to_replace'.

Please visit [these detailed instructions](https://github.com/locluclak/SI-SeqFS-DA?tab=readme-ov-file#how-to-automatically-replace-the-files) on replacing the files.

## Installization

You can install this package from PyPI using:

`pip install si-seqfs-da`

## Example 

```python 
from si_seqfs_da import gendata, SI_SeqFS_DA
import numpy as np

ns = 50 #number of source's samples
nt = 10 #number of target's samples
p = 4 #number of features

true_beta_s = np.full((p,1), 2) #source's beta
true_beta_t = np.full((p,1), 0) #target's beta

Xs, Xt, Ys, Yt, Sigma_s, Sigma_t = gendata.generate(ns, nt, p, true_beta_s, true_beta_t)



K = 2 # number of features to be selected


# apply DA-SeqFS to select relevant features
print('Selected features: ', DA_SeqFS.DA_SeqFS(Xs, Ys,
                                                Xt, Yt,
                                                Sigma_s, Sigma_t,
                                                K, method='forward'))

# compute p-value with SI-SeqFS-DA 
print('p-value =',SI_SeqFS_DA.SI_SeqFS_DA(Xs, Ys, 
                                Xt, Yt, 
                                K, Sigma_s, Sigma_t, 
                                method='forward', jth=None)) 
                                #jth = None means randomly choose jth

K = 'AIC' # stopping criterion
# apply DA-SeqFS to select relevant features
print('Selected features: ', DA_SeqFS.DA_SeqFS(Xs, Ys, 
                                                Xt, Yt, 
                                                Sigma_s, Sigma_t,
                                                K, method='backward'))
# compute p-value with SI-SeqFS-DA 
print('p-value =',SI_SeqFS_DA.SI_SeqFS_DA(Xs, Ys, Xt, Yt, K, Sigma_s, Sigma_t, method='backward', jth=1))
```