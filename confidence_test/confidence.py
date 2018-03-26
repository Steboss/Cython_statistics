import numpy as np
import scipy.stats
import glob
import sys
import perturb
import time

def get_error_bounds(data):
    n = data.shape[0]
    mean = np.mean(data)
    data_sorted = np.sort(data)
    x1= int(np.floor(0.05*n))
    x2= int(np.ceil(0.95*n))
    lower_bound = data_sorted[x1]
    upper_bound = data_sorted[x2]
    return (lower_bound, mean, upper_bound)

def calculate_R2 ( series1, series2 ):
    r_value = perturb.correlation(series1,series2)
    #rp_value,p = scipy.stats.pearsonr(series1,series2)
    #print(r_value,rp_value)
    return r_value**2, r_value

def calculate_tau(series1, series2):
    tau = perturb.kendaltau(series1,series2)
    #tau = scipy.stats.kendalltau(series1, series2)
    #print(tau_c,tau[0])
    return tau#[0] the [0] is for the scipy one

def calculate_mue( series1, series2 ):

    #sumdev = 0.0
    #for x in range(0,len(series1)):
    #    sumdev += abs( series1[x] - series2[x] )

    #sumdev /= len(series1)

    #sumdev_c = 0.0
    sumdev = perturb.mue(series1,series2)
    #print(sumdev_c,sumdev)
    return sumdev

def bootstrap(data):
    r""" generates new set of data based on gauss distribution
    Parameters
    ----------
    data : nd.array(shape(datapoints,2))
        first column holding actual data, second error on data

    """
    repeat = np.zeros(np.shape(data))

    count = 0
    for d in data:
        val = d[0]
        err = d[1]
        if err != 0.0:
            #generate a gaussian random number which is lying between
            # val-err and val+err
            val2 = perturb.perturbation(val, err)
            #val2 = np.random.normal(val,err)
        else:
            val2 = val
        repeat[count][0] = val2
        repeat[count][1] = err
        count = count + 1

    return repeat

def compute_for_subdata_set(exp_file, comput_file):
    experimental, computed = read_subdata(exp_file, comput_file)
    compute_errors(experimental, computed)
    return experimental, computed

def read_subdata(exp_file, comput_file):
    print ('Computing observables for %s and %s data pair' %(exp_file, comput_file))
    f = open(exp_file, 'r')
    lines = f.readlines()
    experimental = []
    for l in lines:
        val = float(l.split(",")[1])
        err = float(l.split(",")[2])
        experimental.append(np.array([val,err]))
    f.close()
    #order F is extremelly important
    #C expects to have x-coordinates on one line, y coords on another list and so on
    #so we need a F order
    #normally we hav ea  C order, which gather x and y contigously
    experimental = np.array(experimental,dtype=float,order="F")

    f = open(comput_file, 'r')
    lines = f.readlines()
    computed = []
    for l in lines:
        val = float(l.split(",")[1])
        err = float(l.split(",")[2])
        computed.append(np.array([val,err]))
    f.close()
    computed = np.array(computed,dtype=float,order="F")
    #print(experimental)
    #print(computed)
    return (experimental, computed)



def compute_errors(experimental, computed):
    r_dist = []
    mue_dist = []
    rsqrt_dist = []
    taus = []
    start = time.time()
    for i in range(10000):
        computed_new = bootstrap(computed)
        computed_new = np.array(computed_new,dtype=float,order="F")
        rsqrt,r = calculate_R2(computed_new[:,0],experimental[:,0])
        mue = calculate_mue(computed_new[:,0],experimental[:,0])
        tau = calculate_tau(computed_new[:,0],experimental[:,0])

        mue_dist.append(mue)
        r_dist.append(r)
        rsqrt_dist.append(rsqrt)
        taus.append(tau)
    end = time.time()
    print("Total computing time %.4f s" % (end-start))
    rsqrt_dist = np.array(rsqrt_dist)
    r_dist = np.array(r_dist)
    mue_dist = np.array(mue_dist)
    taus = np.array(taus)
    (r_min, r_mean, r_max) = get_error_bounds(r_dist)
    (rsqrt_min, rsqrt_mean, rsqrt_max) = get_error_bounds(rsqrt_dist)
    (mue_min, mue_mean, mue_max) = get_error_bounds(mue_dist)
    (tau_min, tau_mean,tau_max) = get_error_bounds(taus)
    print ("Observables are:")
    print ("R: %f < %f < %f " % (r_min, r_mean, r_max))
    print ("Rsqrt: %f < %f < %f " % (rsqrt_min, rsqrt_mean, rsqrt_max))
    print ("mue: %f < %f < %f " % (mue_min, mue_mean, mue_max))
    print("Kendall tau : %f < %f < %f" % (tau_min, tau_mean, tau_max) )



if __name__ == '__main__':
    print ("========Analysis==========")
    print ("++++++++++++++Protocol+++++++++++++++++")
    exp_file = sys.argv[1]
    comput_file = sys.argv[2]
    exp, comput = compute_for_subdata_set(exp_file, comput_file)
