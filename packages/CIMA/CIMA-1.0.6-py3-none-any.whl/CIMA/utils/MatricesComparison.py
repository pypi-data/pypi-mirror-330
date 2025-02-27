#===============================================================================
#     This file is part of CIMA.
#
#     CIMA is a software designed to help the user in the manipulation
#     and analyses of genomic super resolution localisation data.
#
#      Copyright  2019-2025
#
#                Authors: Ivan Piacere,Irene Farabella
#
#
#
#===============================================================================
import os
import numpy as np
import scipy
import scipy.sparse as sp
import scipy


def makeAxesLabelsLog():
    xlims = plt.gca().get_xlim()
    ylims = plt.gca().get_ylim()
    xticks1 = np.arange(np.ceil(xlims[0]),np.floor(xlims[1])+0.1,1.0)
    yticks1 = np.arange(np.ceil(ylims[0]),np.floor(ylims[1])+0.1,1.0)
    _ = plt.xticks(xticks1, [r"$10^{{ {:0.0f} }}$".format(int(xticks1[i])) for i in range(len(xticks1))])
    _ = plt.yticks(yticks1, [r"$10^{{ {:0.0f} }}$".format(int(yticks1[i])) for i in range(len(yticks1))])


def getLogLinearRegression(vals1, vals2):
    import scipy
    arr1 = np.log10(vals1)
    arr2 = np.log10(vals2)
    where_ok = (np.isfinite(arr1)*np.isfinite(arr2)).astype('bool')
    lr= scipy.stats.linregress(arr1[where_ok],arr2[where_ok])
    return lr.intercept, lr.slope

def plotLine(intercept, slope, xlim0, xlim1, num=10, **kwargs):
    xs = np.linspace(xlim0, xlim1, num)
    ys = intercept + xs*slope
    plt.plot(xs, ys, **kwargs)
    
def plotLogWithKdeColors(arr1,arr2,log=True, **kwargs):
    import scipy
    if log:
        arr1_log = np.log10(arr1)
        arr2_log = np.log10(arr2)
        where_ok = (np.isfinite(arr1_log)*np.isfinite(arr2_log)).astype('bool')
        arr1_log = arr1_log[where_ok]
        arr2_log = arr2_log[where_ok]
    else:
        arr1_log = arr1
        arr2_log = arr2
    sta = np.vstack([arr1_log,arr2_log])
    #z = scipy.stats.gaussian_kde(sta)(sta)
    g = sns.scatterplot(x=arr1_log, y=arr2_log, palette='plasma', s=20, legend=False)  # hue=z
    sns.despine()
    # _ = plt.legend(title='Density')
    # sns.move_legend(g, "upper left", bbox_to_anchor=(1, 1))
    # plt.colorbar(g)
    # g = sns.kdeplot(x=arr1, y=arr2, levels=5,fill=True,alpha=0.6,cut=2,)
    intercept, slope = getLogLinearRegression(arr1, arr2)
    print('pearson: ', scipy.stats.pearsonr(arr1_log,arr2_log).statistic)
    print('slope: ', slope)
    xlims = plt.gca().get_xlim()
    plotLine(intercept, slope, xlims[0], xlims[1], c='black', ls='--', **kwargs)
    makeAxesLabelsLog()
    return (scipy.stats.pearsonr(arr1_log,arr2_log).statistic, slope)




def scc(m1, m2):
    # return hicrep.sccByDiag(sp.coo_matrix(m1[where_ok_inds]), sp.coo_matrix(m2[where_ok_inds]), m1[where_ok_inds].shape[0])
    m1c = m1.copy()
    m2c = m2.copy()
    # m1c[[25,26,27],:] = 0.0
    # m1c[:, [25,26,27]] = 0.0
    # m2c[[25,26,27],:] = 0.0
    # m2c[:,[25,26,27]] = 0.0
    
    # return hicrep.sccByDiag(sp.coo_matrix(m1c), sp.coo_matrix(m2c), m1.shape[0])
    return SCCComputer().sccByDiag2(m1c,m2c)

def pearson_corr(m1, m2):
    # return scipy.stats.pearsonr(m1[where_ok_inds].flatten(), m2[where_ok_inds].flatten()).statistic
    m1c = m1.copy()
    m2c = m2.copy()
    m1c[np.tril_indices(m1c.shape[0],-1)] =np.nan
    m2c[np.tril_indices(m1c.shape[0],-1)] =np.nan
    # m1c[[25,26,27],:] = 0.0
    # m1c[:, [25,26,27]] = 0.0
    # m2c[[25,26,27],:] = 0.0
    # m2c[:,[25,26,27]] = 0.0
    # return scipy.stats.pearsonr(m1c[np.nonzero(m1c+m2c)].flatten(), m2c[np.nonzero(m1c+m2c)].flatten()).statistic
    return scipy.stats.pearsonr(m1c[np.isfinite(m1c+m2c)].flatten(), m2c[np.isfinite(m1c+m2c)].flatten()).statistic
    # return scipy.stats.pearsonr(m1c.flatten(), m2c.flatten()).statistic

def spearman_corr(m1, m2):
    m1c = m1.copy()
    m2c = m2.copy()
    m1c[np.tril_indices(m1c.shape[0],-1)] =np.nan
    m2c[np.tril_indices(m1c.shape[0],-1)] =np.nan
    # m1c[[25,26,27],:] = 0.0
    # m1c[:, [25,26,27]] = 0.0
    # m2c[[25,26,27],:] = 0.0
    # m2c[:,[25,26,27]] = 0.0
    # return scipy.stats.spearmanr(m1c[np.nonzero(m1c+m2c)].flatten(), m2c[np.nonzero(m1c+m2c)].flatten()).statistic
    return scipy.stats.spearmanr(m1c[np.isfinite(m1c+m2c)].flatten(), m2c[np.isfinite(m1c+m2c)].flatten())[0]
    # return scipy.stats.spearmanr(m1c.flatten(), m2c.flatten()).statistic




class SCCComputer():
    def __init__(self):
        pass

    def upperDiagCsr(self, m: sp.coo_matrix, nDiags: int):
        """Convert an input sp.coo_matrix into a sp.csr_matrix where each row in the
        the output corresponds to one diagonal of the upper triangle of the input.

        Args:
            m (sp.coo_matrix): input matrix
            nDiags (int): output diagonals with index in the range [1, nDiags)
            as rows of the output matrix
        Returns: `sp.csr_matrix` whose rows are the diagonals of the input
        """
        row = m.col - m.row
        idx = np.where((row > 0) & (row < nDiags))
        idxRowp1 = row[idx]
        # the diagonal index becomes the row index
        idxRow = idxRowp1 - 1
        # offset in the original diagonal becomes the column index
        idxCol = m.col[idx] - idxRowp1
        ans = sp.csr_matrix((m.data[idx], (idxRow, idxCol)),
                            shape=(nDiags - 1, m.shape[1]), dtype=m.dtype)
        ans.eliminate_zeros()
        return ans
    

    def varVstran(self, n):
        """
        Calculate the variance of variance-stabilizing transformed
        (or `vstran()` in the original R implementation) data. The `vstran()` turns
        the input data into ranks, whose variance is only a function of the input
        size:
            ```
            var(1/n, 2/n, ..., n/n) = (1 - 1/(n^2))/12
            ```
        or with Bessel's correction:
            ```
            var(1/n, 2/n, ..., n/n, ddof=1) = (1 + 1.0/n)/12
            ```
        See section "Variance stabilized weights" in reference for more detail:
        https://genome.cshlp.org/content/early/2017/10/06/gr.220640.117

        Args:
            n (Union(int, np.ndarray)): size of the input data
        Returns: `Union(int, np.ndarray)` variance of the ranked input data with Bessel's
        correction
        """
        with suppress(ZeroDivisionError), np.errstate(divide='ignore', invalid='ignore'):
            return np.where(n < 2, np.nan, (1 + 1.0 / n) / 12.0)

    def sccByDiagOriginal(self,m1pre, m2pre):
        """Compute diagonal-wise hicrep SCC score for the two input matrices up to
        nDiags diagonals


        Args:
            m1 (sp.coo_matrix): input contact matrix 1
            m2 (sp.coo_matrix): input contact matrix 2
            nDiags (int): compute SCC scores for diagonals whose index is in the
            range of [1, nDiags)
        Returns: `float` hicrep SCC scores
        """
        m1prec = m1pre
        m1 = sp.coo_matrix(m1pre)
        m2 = sp.coo_matrix(m2pre)
        nDiags = m1.shape[0]
        # convert each diagonal to one row of a csr_matrix in order to compute
        # diagonal-wise correlation between m1 and m2
        m1D = self.upperDiagCsr(m1, nDiags)
        m2D = self.upperDiagCsr(m2, nDiags)
        nSamplesD = (m1D + m2D).getnnz(axis=1)
        rowSumM1D = m1D.sum(axis=1).A1
        rowSumM2D = m2D.sum(axis=1).A1
        # ignore zero-division warnings because the corresponding elements in the
        # output don't contribute to the SCC scores
        with np.errstate(divide='ignore', invalid='ignore'):
            cov = m1D.multiply(m2D).sum(axis=1).A1 - rowSumM1D * rowSumM2D / nSamplesD
            rhoD = cov / np.sqrt(
                (m1D.power(2).sum(axis=1).A1 - np.square(rowSumM1D) / nSamplesD ) *
                (m2D.power(2).sum(axis=1).A1 - np.square(rowSumM2D) / nSamplesD ))
            wsD = nSamplesD * self.varVstran(nSamplesD)
            wsNan2Zero = np.nan_to_num(wsD, copy=True, posinf=0.0, neginf=0.0)
            rhoNan2Zero = np.nan_to_num(rhoD, copy=True, posinf=0.0, neginf=0.0)

        return rhoNan2Zero @ wsNan2Zero / wsNan2Zero.sum()
    
    def getDiagValidCounts(self, m1, m2):
        diaglens = []
        nDiags = m1.shape[1]
        for k in range(1,nDiags):
            d1 = np.diag(m1,k)
            d2 = np.diag(m2,k)
            where_compare = (np.isfinite(d1)*np.isfinite(d2)).astype('bool')
            diaglens.append(where_compare.sum())
        diaglens = np.array(diaglens)
        return diaglens

    
    def sccByDiag2(self, m1, m2):
        prs = []
        diaglens = []
        nDiags = m1.shape[1]
        for k in range(1,nDiags):
            d1 = np.diag(m1,k)
            d2 = np.diag(m2,k)
            where_compare = (np.isfinite(d1)*np.isfinite(d2)).astype('bool')

            diaglens.append(where_compare.sum())
            if(k==1):
                d1saved = d1.copy()
                d2saved = d2.copy()
                where_compare_saved = where_compare.copy()
            if(where_compare.sum() > 1 and d1[where_compare].std()>0 and d2[where_compare].std()>0):
                pr = scipy.stats.pearsonr(d1[where_compare],d2[where_compare]).statistic
            else:
                pr = 0.0
            prs.append(pr)
        
        diaglens = np.array(diaglens)
        ws = np.where(diaglens < 2, 0.0, (1 + 1.0 / diaglens) / 12.0)
        sccval = (np.array(prs)*ws).sum()/ws.sum()
        return sccval

