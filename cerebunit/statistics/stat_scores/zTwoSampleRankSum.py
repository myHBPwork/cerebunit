# ============================================================================
# ~/cerebtests/cerebunit/stat_scores/zTwoSampleRankSum.py
#
# created 16 September 2019 Lungsi
#
# This py-file contains custum score functions initiated by
#
# from cerebunit import scoreScores
# from cerebunit.scoreScores import ABCScore
# ============================================================================

import numpy as np
import sciunit


# ======================ZScoreForTwoSampleRankSumTest=========================
class ZScoreForTwoSampleRankSumTest(sciunit.Score):
    """
    Compute z-statistic for Two Sample Rank-Sum Test (aka, Wilcoxon rank-sum or Mann-Whitney test). Note that this is **not** Wilcoxon Signed Rank test.

    .. table:: Title here

    ================= ================================================================================
      Definitions      Interpretation                    
    ================= ================================================================================
    :math:`\eta_0`    some specified value              
    :math:`n_1`       sample size for sample 1
    :math:`n_2`       sample size for sample 2
    :math:`N`         total sample size, :math:`n_1 + n_2`
    :math:`W`         sum of ranks for observations in sample 1 (post dataset ranking)
    :math:`\mu_W`     assuming :math:`H_0` is true,
                      :math:`\mu_W` = :math:`\\frac{ n_1(1+N) }{ 2 }`
    :math:`\sigma_W`  assuming :math:`H_0` is true,
                      :math:`\mu_W` = :math:`\\sqrt{ \\frac{ n_1 n_2 (1+N) }{12} }`
    z-statistic, z    z = :math:`\\frac{ W - \mu_W }{ \sigma_W }`
    ================= ================================================================================

    **NOTE:**

    * :math:`H_0` is true :math:`\Rightarrow` for samples 1 and 2 their population distributions are the same
    *
    
    **Use Case:**

    ::

      x = ZScoreForTwoSampleRankSumTest.compute( observation, prediction )
      score = ZScoreForTwoSampleRankSumTest(x)

    *Note*: As part of the `SciUnit <http://scidash.github.io/sciunit.html>`_ framework this custom :py:class:`.TScore` should have the following methods,

    * :py:meth:`.compute` (class method)
    * :py:meth:`.sort_key` (property)
    * :py:meth:`.__str__`

    """
    #_allowed_types = (float,)
    _description = ( "ZScoreForSignTest gives the z-statistic applied to medians. "
                   + "The experimental data (observation) is taken as the sample. "
                   + "The sample statistic is 'median' or computed median form 'raw_data'. "
                   + "The null-value is the 'some' specified value whic is taken to be the predicted value generated from running the model. " )

    @classmethod
    def compute(self, observation, prediction):
        """
        +----------------------------+------------------------------------------------+
        | Argument                   | Value type                                     |
        +============================+================================================+
        | first argument             | dictionary; observation/experimental data      |
        +----------------------------+------------------------------------------------+
        | second argument            | dictionary; simulated data                     |
        +----------------------------+------------------------------------------------+

        *Note:*

        * observation **must** have the key "raw_data" whose value is the list of numbers
        * simulation, i.e, model prediction **must** also have the key "raw_data"

        """
        n1 = len( observation["raw_data"] )
        n2 = len( prediction["raw_data"] )
        N = n1 + n2
        #
        muW = n1*(1+N)/2
        sigmaW = np.sqrt( n1*n2*(1+N)/12 )
        data = np.array( observation["raw_data"] )
        splus = ( data < prediction ).sum()
        n_u = (data != prediction ).sum()
        self.score = (splus - (n_u/2)) / np.sqrt(n_u/4)
        return self.score # z_statistic

    @property
    def sort_key(self):
        return self.score

    def __str__(self):
        return "ZScore is " + str(self.score)

    def get_observation_rank(self, observation, prediction):
        """Returns ranks for the observation data.

        * sample 1, observation["raw_data"]
        * sample 2, prediction["raw_data"]

        *Example for describing what 'ranking' means:*

        :math:`sample1 = [65, 60, 62, 70]`
        :math:`sample2 = [60, 55, 65, 70]`
        Then,
        :math:`ordered_data = [55, 60, 60, 62, 65, 65, 70, 70]`
        :math:`raw_ranks    = [ 1,  2,  3,  4,  5,  6,  7,  8]`
        and
        :math:`correct_ranks= [ 1, 2.5, 2.5, 4, 5.5, 5.5, 7.5, 7.5]`
        Therefore, ranks for sample1 is
        :math:`sample1_ranks = [5.5, 2.5, 4, 7.5]`

        """
        ordered_data, all_ranks = self.__orderdata_ranks(observation, prediction)
        sample1 = np.array( observation["raw_data"] )
        sample1_ranks = np.zeros((1,len(sample1)))[0]
        for i in range(len(ordered_data)): # go through all the ordered data
            a_data = ordered_data[i]
            its_rank = all_ranks[i]
            # for each picked data value get its index w.r.t sample1
            indx_in_sample1 = np.where( sample1 == a_data )[0]
            if len(indx_in_sample1)>1: # if the picked data value exists within sample1
                for j in range( len(indx_in_sample1) ): # at each corresponding index in sample1
                    sample1_ranks[ indx_in_sample1[j] ] = its_rank # set appropriate rank
        return sample1_ranks

    def __orderdata_ranks(self, observation, prediction):
        """ Private function that orders the data and returns its appropriate rank.

        * sample 1, observation["raw_data"]
        * sample 2, prediction["raw_data"]

        **Step-1:**

        * append the two lists (i.e, the two samples)
        * order the values in ascending manner

        **Step-2:**

        * get unique values in the ordered data
        * also get the number of frequencies for each unique value

        **Step-3:**

        * construct raw ranks based on the ordered data

        **Step-4:**

        * for each value in the ordered data find its index in unique values array
        * if the corresponding count is more than one compute its midrank (sum ranks/its count)
        * set ranks (in raw ranks array) for the corresponding number of values with the computed midrank
        
        """
        ordered_data = np.sort( observation["raw_data"] + prediction["raw_data"] )
        unique_values, counts = np.unique( ordered_data, return_counts=True )
        raw_ranks = [ i+1 for i in range(len(ordered_data)) ]
        #
        i = 0 # initiate from first index of ordered_data and raw_ranks
        while i < len(ordered_data):
            indx_in_uniques = int( np.where( unique_values == ordered_data[i] )[0] )
            if counts[indx_in_uniques]>1:
                numer = 0.0
                numer = [ numer + raw_ranks[i+j] for j in range( counts[indx_in_uniques] ) ][0]
                for j in range( counts[indx_in_uniques] ):
                    raw_ranks[i+j] = numer/counts[indx_in_uniques]
            # raw_ranks[i] does not need to be set for counts = 1
            i = i + counts[indx_in_uniques] # update loop (skipping repeated values)
        return [ ordered_data, raw_ranks ] 
        #sample1 = np.array( observation["raw_data"] )
        #sample1_ranks = np.zeros((1,len(sample1)))[0]
        #for i in range(len(ordered_data)):
        #    a_data = ordered_data[i]
        #    its_rank = raw_ranks[i]
        #    indx_in_sample1 = np.where( sample1 == a_data )[0]
        #    if len(indx_in_sample1)>1:
        #        for j in range( len(indx_in_sample1) ):
        #            sample1_ranks[ indx_in_sample1[j] ] = its_rank
        #return sample1_ranks










# ============================================================================
