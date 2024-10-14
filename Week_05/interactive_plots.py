import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal as mvn
from scipy.stats import pearsonr, ttest_ind, ttest_1samp
from scipy.special import hyp2f1, gamma

from IPython.display import display, HTML
from ipywidgets import FloatSlider, IntSlider, HBox, Button, Layout, widgets, GridspecLayout, Label

def cor_coefs_of_samples(ρ=0.46, N=10000, n=10):
    """return a dataframe of samples"""
    rv = mvn([20, 22], 3*np.array([[1, ρ], [ρ, 1]]))
    x = rv.rvs((N, n))
    rs = [pearsonr(x[i,:,0], x[i,:,1]).statistic for i in range(x.shape[0])]
    samples = pd.DataFrame({'sample':list(range(1, x.shape[0]+1)), 'r':rs})
    samples.set_index('sample', inplace=True)
    return samples

class cor_coef_demo:
    def __init__(self):
        def update_slider(_):
            # set r to the slider value and replot
            self.r = r_sl.value
            plot()

        def plot():
            # clear plot
            ax.cla()
            if self.r >= 0:
                # if r is positive move points towards y=x
                xp = a + (1-self.r) * b
                yp = a - (1-self.r) * b
            elif self.r < 0:
                # if r is negative move points towards y=-x
                xp = (1+self.r) * a + b    
                yp = (1+self.r) * a - b

            # scatter plot of points removing tick labels and set title to r
            ax.scatter(xp, yp, edgecolors='k', alpha=0.5)
            ax.set_xlim(-4, 4)
            ax.set_ylim(-4, 4)
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_title(f'$r$ = {self.r:.2f}', size=20)
            
        # 100 random variates from a bivariate normal distribution with mean 0, and identity covariance matrix
        xs = mvn.rvs([0, 0], size=100)
        # save variates into x and y and set up a and b for transformation in plot()
        x, y = xs[:,0], xs[:,1]
        a = 0.5*(x + y)
        b = 0.5*(x - y)
        # set initial cor. coef. to 0
        self.r = 0
        
        # set up a slider for r from -1 to 1
        r_sl = FloatSlider(min=-1, max=1, value=self.r, step=0.01,  layout={'width':'200pt'},
                           style={'description_width':'initial', 'handle_color':'Blue'},)
        r_sl.observe(update_slider, 'value')
        display(r_sl)
            
        # initialise figure removing unnecessary clutter
        fig, ax = plt.subplots(1, 1, figsize=(5, 5))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        fig.canvas.footer_visible = False
        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = False
        plot()
        plt.ion()

class sample_pairs_demo:
    def __init__(self):
        def update_button(_):
            try:
                ax, r, pc = next(sample)
            except:
                return None
            pc.set_visible(True)
            ax.set_title(f'$r$ = {r:.2f}', size=12)
            ax.axis('on')
            ax.set_xticklabels([])
            ax.set_yticklabels([])
            ax.set_xticks([])
            ax.set_yticks([])

        def plot():
            ρ = 0.46
            rv = mvn([20, 22], 16*np.array([[1, ρ], [ρ, 1]]))
            xs = rv.rvs((10, 10))
            rps = [pearsonr(xs[i,:,0], xs[i,:,1]) for i in range(xs.shape[0])]
            rs = [i.statistic for i in rps]
            fig, axs = plt.subplots(1, 10, figsize=(10, 1.5), sharex=True, sharey=True)
            fig.subplots_adjust(left=0, top=0.7, wspace=0, hspace=0)
            pcs = []
            for ax, x in zip(axs.flatten(), xs):
                pcs.append(ax.scatter(x[:,0], x[:,1], edgecolors='k', alpha=0.5))
                pcs[-1].set_visible(False)
                ax.axis('off')
            
            fig.canvas.footer_visible = False
            fig.canvas.header_visible = False
            fig.canvas.toolbar_visible = False
            plt.ion()
            for ax, i, pc in zip(axs.flatten(), rs, pcs):
                yield ax, i, pc

        sample = plot()

        button = Button(description="Next sample", button_style='info')
        button.on_click(update_button)
        display(button)

class CI_demo:
    def __init__(self):
        def update_slider(_):
            # set n to the slider value and replot
            self.n = n_sl.value
            plot()

        def plot():
            ax = axs[0]
            # clear plot
            ax.cla()
            # scatter plot of male and female pair arrival times
            ax.scatter(data=gannets.iloc[:self.n], x='male', y='female')
            ax.set_xlabel('Male gannet day of arrival')
            ax.set_ylabel('Female gannet day of arrival')
            ax.set_title(f'{self.n} pairs of gannets')
            ax.set_xlim(5, 35)
            ax.set_ylim(5, 35)

            ax = axs[1]
            # clear plot
            ax.cla()
            # fill between lower and upper limits of 95% CI
            ax.fill_between(xr, lower, upper, color='Grey')
            # a line for the correlation coefficient, r
            ax.plot(xr, r, color='Yellow', lw=1)
            ax.set_ylim(-1, 1)
            ax.set_xlabel('Sample size $n$')
            ax.set_ylabel('95% CI for ρ')
            # a vertical line showing the 95% CI for the current sample size
            x = self.n
            y1 = lower[self.n-10]
            y2 = upper[self.n-10]
            ax.plot([x, x], [y1, y2], color='Yellow')
            ax.set_title(f'95% CI = ({y1:.2f}, {y2:.2f})')
            ax.text(x, y1, f'{y1:.2f}', size=12, ha='center', va='top')
            ax.text(x, y2, f'{y2:.2f}', size=12, ha='center', va='bottom')
            
        maxn = 200
        self.n = 10
        xr = np.arange(10, maxn+1, 1)
        
        # sample some random pairs of arrival times and add it to the existing data
        ρ = 0.46
        rv = mvn([20, 22], 16*np.array([[1, ρ], [ρ, 1]]))
        xs = rv.rvs((1, maxn)).round(0)
        new_birds = pd.DataFrame({'male':xs[:,0], 'female':xs[:,1]}, dtype='int')
        gannets = pd.read_csv('../Datasets/gannets.csv')
        gannets = pd.concat([gannets, new_birds])

        # calculate r and the 95% CI for sample sizes ranging from 10 to maxn
        r, lower, upper = [], [], []
        for i in xr:
            result = pearsonr(gannets['male'].iloc[:i], gannets['female'].iloc[:i])
            ci = result.confidence_interval()
            r.append(result.statistic)
            lower.append(ci.low)
            upper.append(ci.high)

        # set up a slider for n from 10 to maxn
        n_sl = IntSlider(min=self.n, max=maxn, value=self.n, step=1, layout={'width':'200pt'},
                           style={'description_width':'initial', 'handle_color':'Blue'},)
        n_sl.observe(update_slider, 'value')
        display(n_sl)
        
        # initialise figure removing unnecessary clutter
        fig, axs = plt.subplots(1, 2, figsize=(11, 5))
        plt.subplots_adjust(bottom=0.2, wspace=0.3)
        for ax in axs:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        fig.canvas.footer_visible = False
        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = False
        plot()
        plt.ion()

class cor_coef_prob_demo:
    def __init__(self, ρ=0, n=10):
        def update_slider(_):
            # set ρ to the slider value and replot
            self.ρ = ρ_sl.value
            plot()

        def r_sampling_dist(ρ, n):
            # the sampling distribution of correlation coefficient r, given ρ and n
            return (n-2)*gamma(n-1)*(1-ρ**2)**((n-1)/2)*(1-xr**2)**((n-4)/2) / \
                (np.sqrt(2*3.142)*gamma(n-0.5)*(1-ρ*xr)**(n-1.5)) * \
                hyp2f1(0.5, 0.5, n-0.5, 0.5*(ρ*xr+1))

        def plot():
            ax = axs[1]
            # clear plot
            ax.cla()
            # histogram of sampling distribution
            pdf = r_sampling_dist(self.ρ, n)
            h = dx*0.5*(pdf[:-1] + pdf[1:])
            # ax.bar(xr[:-1], h, dx, edgecolor='k', align='edge', alpha=0.5)
            ax.plot(xr[:-1], h)
            # plot a red line at the sample cor. coef.
            ax.plot([sample_r, sample_r], [0, h[idx]], color='DarkRed', lw=3)
            ha = 'right' if self.ρ > 0.38 else 'left'
            ax.text(sample_r, h[idx], f'{sample_r}', ha=ha, color='DarkRed')
            ax.set_xlim(-1, 1)
            ax.set_yticklabels([])
            ax.set_yticks([])
            ax.set_xlabel('Sample correlation coefficient, $r$')
            ax.set_ylabel('Probability of observing $r$')
            ax.set_ylim(0, ax.get_ylim()[1])
            ax.set_title(f'ρ = {self.ρ:.2f}', size=20)
            
        if n > 150:
            raise ValueError('n must be less than or equal to 150')
        # set initial cor. coef. to ρ
        self.ρ = ρ
        # bar width
        dx = 0.005
        xr = np.arange(-1, 1+dx, dx)
        # the index in xr of the sample cor. coef. for plotting a line
        sample_r = 0.46
        idx = np.abs(xr - sample_r).argmin()
    
        # set up a slider for ρ from -0.99 to 0.99
        ρ_sl = FloatSlider(min=-0.99, max=0.99, value=self.ρ, step=0.01,  layout={'width':'200pt'},
                           style={'description_width':'initial', 'handle_color':'Blue'},)
        ρ_sl.observe(update_slider, 'value')
        display(ρ_sl)
            
        # initialise figure removing unnecessary clutter
        fig, axs = plt.subplots(1, 2, figsize=(11, 5))
        plt.subplots_adjust(bottom=0.2)

        ax = axs[0]
        gannets = pd.read_csv('../Datasets/gannets.csv')
        # gannets = pd.read_csv('DExB2-development/Datasets/gannets.csv')
        sns.scatterplot(data=gannets, x='male', y='female', ax=ax)
        ax.set_xlabel('Male gannet day of arrival')
        ax.set_ylabel('Female gannet day of arrival')
        ax.text(11, 27, f'$r=0.46$', size=22, color='DarkRed')
        ax.plot([10, 30], [10, 30], ls=':') # diagonal line y=x representing the same day of arrival 

        for ax in axs:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
        # ax.spines['left'].set_visible(False)
        fig.canvas.footer_visible = False
        fig.canvas.header_visible = False
        fig.canvas.toolbar_visible = False
        plot()
        plt.ion()

    def savefig(self, filename):
        plt.savefig(filename)