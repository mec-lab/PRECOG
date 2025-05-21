import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as sc
from analysis_indiv import Indiv
from kneed import KneeLocator
import scikits.bootstrap as bootstrap

def dominates(indiv1, indiv2):
    if indiv1.fit1 == indiv2.fit1 and indiv1.fit2 == indiv2.fit2:
        return indiv1.name > indiv2.name
    elif indiv1.fit1 >= indiv2.fit1 and indiv1.fit2 >= indiv2.fit2:
        return True
    else:
        return False
def plot_fitnesses(runName1, runName2):

    run1_fit1 = np.load('data/{}/bestindivs_fit1.npy'.format(runName1))
    run1_fit2 = np.load('data/{}/r2s_2.npy'.format(runName1))

    run2_fit1 = np.load('data/{}/bestindivs_fit1.npy'.format(runName2))
    run2_fit2 = np.load('data/{}/bestindivs_fit2.npy'.format(runName2))


    std_run1_fit1= np.std(run1_fit1)
    std_run1_fit2 = np.std(run1_fit2)
    std_run2_fit1= np.std(run2_fit1)
    std_run2_fit2 = np.std(run2_fit2)

    x = np.arange(2)
    labels = ['AFPO', 'PRECOG']
    plt.rcParams['text.usetex'] = True
    plt.figure()
    plt.bar(x,[np.mean(run1_fit1), np.mean(run2_fit1)], yerr=[std_run1_fit1, std_run2_fit1], color=['tab:blue', 'tab:orange'])
    plt.xlabel("Method")
    plt.ylabel("Task Fitness")
    plt.xticks(x, labels)
    plt.show()

    plt.figure()
    plt.bar(x,[np.mean(run1_fit2), np.mean(run2_fit2)], yerr=[std_run1_fit2, std_run2_fit2], color=['tab:blue', 'tab:orange'])
    plt.xlabel("Method")
    plt.ylabel(r'$R^2$')
    plt.xticks(x, labels)
    plt.show()

    # combined plot
    types = {
        'AFPO': np.stack((np.mean(run1_fit1), np.mean(run1_fit2)), axis=0),
        'PRECOG': np.stack((np.mean(run2_fit1), np.mean(run2_fit2)), axis=0)
    }
    errors = {
        'AFPO': np.stack((std_run1_fit1,std_run1_fit2), axis=0),
        'PRECOG': np.stack((std_run2_fit1, std_run2_fit2), axis=0)
    }
    x = np.arange(2)
    width = 0.5
    multiplier = 0
    xtick_labels = ['Efficacy', 'Predictability']
    for type, fits in types.items():
        print(type)
        print(fits.shape)
        print(errors[type].shape)
        offset = width*multiplier - 0.25
        plt.bar(x+offset, fits, width, label=type, log=True, yerr=errors[type])
        multiplier += 1
    plt.ylabel("Fitness Value")
    plt.xlabel("Fitness Type")
    plt.xticks(x, xtick_labels)
    plt.legend()
    plt.show()


    print("afpo")
    print("fitness")
    print('ave', np.mean(run1_fit1))
    print('min', np.min(run1_fit1))
    print('max', np.max(run1_fit1))
    print("r2")
    print('ave', np.mean(run1_fit2))
    print('min', np.min(run1_fit2))
    print('max', np.max(run1_fit2))

    print("evosync")
    print("fitness")
    print('ave', np.mean(run2_fit1))
    print('min', np.min(run2_fit1))
    print('max', np.max(run2_fit1))
    print("r2")
    print('ave', np.mean(run2_fit2))
    print('min', np.min(run2_fit2))
    print('max', np.max(run2_fit2))

    stat, p = sc.mannwhitneyu(run2_fit1, run1_fit1, alternative='less')
    print("--------------------------------------------------------")
    print('p-values')
    print('fit1', p)

    stat, p = sc.mannwhitneyu(run2_fit2, run1_fit2, alternative='greater')

    print('r2', p)
    print("--------------------------------------------------------")

def plot_times(runName, numRuns):
    sim_times = np.zeros(numRuns)
    pysr_times = np.zeros(numRuns)
    for i in range(numRuns):
        sim_times[i] = np.load('data/{}/times/simtime{}.npy'.format(runName, i))[0]
        pysr_times[i] = np.load('data/{}/times/pysrtime{}.npy'.format(runName, i))[0]

    sim_std = np.std(sim_times)
    pysr_std = np.std(pysr_times)

    x = np.arange(2)
    labels = ['Simulation', 'Equation Fitting']
    plt.figure()
    plt.bar(x, [np.mean(sim_times), np.mean(pysr_times)], yerr=[sim_std, pysr_std],
            color=['tab:green', 'tab:purple'])
    plt.xlabel("Method Component")
    plt.ylabel("Walltime (s)")
    plt.xticks(x, labels)
    plt.show()

def plot_pareto_front(run, gens, runNum):
    fitness1 = np.load('data/{}/run{}/fit1.npy'.format(run, runNum))
    fitness2 = np.load('data/{}/run{}/fit2.npy'.format(run, runNum))
    names = np.load('data/{}/run{}/names.npy'.format(run, runNum))
    colors = ['tab:blue', 'tab:orange', 'tab:purple', 'tab:green', 'tab:brown', 'tab:grey', 'tab:red', 'tab:black']

    paretos = {}
    for gen in gens:
        total_pop = []
        pop_to_save = []
        fit1 = fitness1[:, gen]
        fit2 = fitness2[:, gen]
        name = names[:, gen]
        for i in range(fit1.shape[0]):
            total_pop.append(Indiv(fit1[i], fit2[i], name[i]))
        for ind1 in total_pop:
            for ind2 in total_pop:
                if ind1 != ind2 and not ind1.remove:
                    ind1.remove = dominates(ind2, ind1)
            if np.isnan(ind1.fit2):
                ind1.remove = True
        print("Gen", gen)
        gen_names = []
        for ind in total_pop:
            if not ind.remove:
                pop_to_save.append(ind)
                gen_names.append(ind.name)
                print(ind.name, ind.fit1, ind.fit2)
        pop_to_save = sorted(pop_to_save, key=lambda ind:ind.fit1, reverse=True)
        paretos[gen] = pop_to_save
        np.save("data/{}/run{}/gen{}_paretonames".format(run, runNum, gen), np.array(gen_names))
        print("---------------------------------------------------------------")

    plt.rcParams['text.usetex'] = True
    plt.figure()
    for j, gen in enumerate(gens):
        fits1 = []
        fits2 = []
        for ind in paretos[gen]:
            fits1.append(ind.fit1)
            fits2.append(ind.fit2)
        plt.scatter(fits1, fits2, color=colors[j], label="Gen {}".format(gen))
        plt.plot(fits1, fits2, color=colors[j])
    plt.xlabel('Task Fitness')
    plt.ylabel(r'$R^2$')
    plt.legend()
    # plt.title('Run {} Pareto Fronts'.format(runNum))
    plt.show()


def locate_knee(population):
    fitness1 = []
    fitness2 = []
    names = []
    for indiv in population:
        fitness1.append(indiv.fit1)
        fitness2.append(indiv.fit2)
        names.append(indiv.name)

    kneedle = KneeLocator(fitness1, fitness2, S=1.0, curve='concave', direction='decreasing')
    best = fitness2.index(kneedle.knee_y)
    name = names[best]
    fit1 = kneedle.knee
    fit2 = kneedle.knee_y
    return int(name), float(fit1), float(fit2)
def plot_meta_pareto(runName):
    names = np.load('data/{}/bestindivs.npy'.format(runName))
    fit1 = np.load('data/{}/bestindivs_fit1.npy'.format(runName))
    fit2 = np.load('data/{}/bestindivs_fit2.npy'.format(runName))

    best_pop = []
    for i in range(names.shape[0]):
        indiv = Indiv(fit1[i], fit2[i], names[i])
        best_pop.append(indiv)

    meta_pareto = []
    for ind1 in best_pop:
        for ind2 in best_pop:
            if ind1 != ind2 and not ind1.remove:
                ind1.remove = dominates(ind2, ind1)
        if np.isnan(ind1.fit2):
            ind1.remove = True
    for ind in best_pop:
        if not ind.remove:
            meta_pareto.append(ind)
    if len(meta_pareto) > 2:
        knee_name, knee_fit1, knee_fit2 = locate_knee(meta_pareto)
        print("Knee Member:", knee_name, 'Fit1:', knee_fit1, 'Fit2:', knee_fit2)

    meta_pareto = sorted(meta_pareto, key=lambda ind:ind.fit2, reverse=True)
    bestfit2_name = meta_pareto[0].name
    bestfit2_fit1 = meta_pareto[0].fit1
    bestfit2_fit2 = meta_pareto[0].fit2

    meta_pareto = sorted(meta_pareto, key=lambda ind:ind.fit1, reverse=True)
    bestfit1_name = meta_pareto[0].name
    bestfit1_fit1 = meta_pareto[0].fit1
    bestfit1_fit2 = meta_pareto[0].fit2

    print("Best Fit1 Member:", bestfit1_name, 'Fit1:', bestfit1_fit1, 'Fit2:', bestfit1_fit2)
    print("Best Fit2 Member:", bestfit2_name, 'Fit1:', bestfit2_fit1, 'Fit2:', bestfit2_fit2)

    plt.rcParams['text.usetex'] = True
    fits1 = []
    fits2 = []
    for ind in meta_pareto:
        fits1.append(ind.fit1)
        fits2.append(ind.fit2)
    plt.figure()
    plt.scatter(fits1, fits2, color='tab:orange')
    plt.plot(fits1, fits2, color='tab:orange')
    plt.xlabel('Task Fitness')
    plt.ylabel(r'$R^2$')
    # plt.title('Meta Pareto Front')
    plt.show()

def plot_fit_over_time(runName1, runName2, numRuns, numGens):
    fit_precog = np.zeros((numRuns, numGens))
    fit_afpo = np.zeros((numRuns, numGens))

    for i in range(numRuns):
        fit_precog[i] = np.average(np.load('data/{}/run{}/fit1.npy'.format(runName2, i)), axis=0)
        fit_afpo[i] = np.average(np.load('data/{}/run{}/fit1.npy'.format(runName1, i)), axis=0)

    length = numGens
    lower_precog = np.zeros(length)
    upper_precog = np.zeros(length)

    lower_afpo = np.zeros(length)
    upper_afpo = np.zeros(length)

    for i in range(length):
        CIs = bootstrap.ci(data=fit_precog[:, i], statfunction=np.mean)
        lower_precog[i] = CIs[0]
        upper_precog[i] = CIs[1]

        CIs_afpo = bootstrap.ci(data=fit_afpo[:, i], statfunction=np.mean)
        lower_afpo[i] = CIs_afpo[0]
        upper_afpo[i] = CIs_afpo[1]

    x = np.arange(numGens)
    plt.figure()
    plt.plot(np.mean(fit_afpo, axis=0), label='AFPO')
    plt.fill_between(x, lower_afpo, upper_afpo, alpha=0.4)
    plt.plot(np.mean(fit_precog, axis=0), label='PRECOG')
    plt.fill_between(x, lower_precog, upper_precog, alpha=0.4)
    plt.xlabel('Generations')
    plt.ylabel("Efficacy Fitness")
    plt.legend()
    plt.show()


if __name__ == '__main__':
    runName1 = 'bm_afpo'
    runName2 = 'bm_quadruped'
    plot_fitnesses(runName1, runName2)
    exit()
    plot_times(runName2, 30)

    plot_meta_pareto(runName2)
    plot_fit_over_time(runName1, runName2, 30, 50)

    gens_to_plot = [0, 9, 19, 29, 39, 49]
    for l in range(6,7):
        print('Run', l)
        plot_pareto_front(runName2, gens_to_plot, l)
        print("-----------------------------------------------------------")
