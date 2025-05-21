from kneed import KneeLocator
import numpy as np
from analysis_indiv import Indiv

def locate_knee(runName, runNum):
    fitness1 = np.load('data/{}/run{}/pareto_fit1.npy'.format(runName, runNum))
    fitness2 = np.load('data/{}/run{}/pareto_fit2.npy'.format(runName, runNum))
    names = np.load('data/{}/run{}/pareto_names.npy'.format(runName, runNum))
    fitness2 = np.nan_to_num(fitness2, nan=-1, posinf=-1,neginf=-1)

    kneedle = KneeLocator(fitness1, fitness2, S=1.0, curve='concave', direction='decreasing')
    best1 = np.where(fitness2 == kneedle.knee_y)[0]
    if len(best1) == 0:
        pop = []
        for j in range(fitness1.shape[0]):
            indiv = Indiv(fitness1[j], fitness2[j], names[np.where(fitness2 == fitness2[j])])
            pop.append(indiv)
        pop = sorted(pop, key=lambda ind:ind.fit1, reverse=True)
        name = pop[0].name
        fit1 = pop[0].fit1
        fit2 = pop[0].fit2
    else:
        best1 = np.where(fitness2 == kneedle.knee_y)[0].tolist()
        best2 = np.where(fitness1 == kneedle.knee)[0].tolist()
        best = list(set(best1) & set(best2))
        name = names[best]
        fit1 = kneedle.knee
        fit2 = kneedle.knee_y
    return int(name), float(fit1), float(fit2)

def locate_knee_afpo(runName, runNum):
    fitness1 = np.load('data/{}/run{}/pareto_fit1.npy'.format(runName, runNum))
    fitness2 = np.load('data/{}/run{}/pareto_fit2.npy'.format(runName, runNum))
    names = np.load('data/{}/run{}/pareto_names.npy'.format(runName, runNum))

    kneedle = KneeLocator(fitness1, fitness2, S=1.0, curve='concave', direction='increasing')
    best = np.where(fitness2 == kneedle.knee_y)[0]
    if len(best) == 0:
        pop = []
        for j in range(fitness1.shape[0]):
            indiv = Indiv(fitness1[j], fitness2[j], names[np.where(fitness2 == fitness2[j])])
            pop.append(indiv)
        pop = sorted(pop, key=lambda ind:ind.fit1, reverse=True)
        name = pop[0].name
        fit1 = pop[0].fit1
        fit2 = pop[0].fit2
    else:
        name = names[best][0]
        fit1 = kneedle.knee
        fit2 = kneedle.knee_y
    return int(name), float(fit1), float(fit2)


def dominates(indiv1, indiv2):
    if indiv1.fit1 == indiv2.fit1 and indiv1.fit2 == indiv2.fit2:
        return indiv1.name > indiv2.name
    elif indiv1.fit1 >= indiv2.fit1 and indiv1.fit2 >= indiv2.fit2:
        return True
    else:
        return False

def dominates_afpo(indiv1, indiv2):
    if indiv1.fit1 == indiv2.fit1 and indiv1.fit2 == indiv2.fit2:
        return indiv1.name > indiv2.name
    elif indiv1.fit1 >= indiv2.fit1 and indiv1.fit2 <= indiv2.fit2:
        return True
    else:
        return False

def get_pareto_front(run, runNum, gen):
    fit1 = np.load('data/{}/run{}/fit1.npy'.format(run, runNum))[:, gen]
    fit2 = np.load('data/{}/run{}/fit2.npy'.format(run, runNum))[:, gen]
    names = np.load('data/{}/run{}/names.npy'.format(run, runNum))[:, gen]

    total_pop = []
    pop_to_save = []
    for j in range(fit1.shape[0]):
        total_pop.append(Indiv(fit1[j], fit2[j], names[j]))
    for ind1 in total_pop:
        for ind2 in total_pop:
            if ind1 != ind2 and not ind1.remove:
                ind1.remove = dominates(ind2, ind1)
        if np.isnan(ind1.fit2):
            ind1.remove = True
    for ind in total_pop:
        if not ind.remove:
            pop_to_save.append(ind)

    pop_to_save = sorted(pop_to_save, key=lambda indiv: indiv.fit1)

    fits1 = []
    fits2 = []
    names = []
    for ind in pop_to_save:
        fits1.append(ind.fit1)
        fits2.append(ind.fit2)
        names.append(ind.name)
        # print('Ind', ind.name, 'Fit1', ind.fit1, "Fit2", ind.fit2)
    np.save('data/{}/run{}/pareto_fit1'.format(run, runNum), fits1)
    np.save('data/{}/run{}/pareto_fit2'.format(run, runNum), fits2)
    np.save('data/{}/run{}/pareto_names'.format(run, runNum), names)

def get_pareto_front_afpo(run, runNum, gen):
    fit1 = np.load('data/{}/run{}/fit1.npy'.format(run, runNum))[:, gen]
    fit2 = np.load('data/{}/run{}/age.npy'.format(run, runNum))[:, gen]
    names = np.load('data/{}/run{}/names.npy'.format(run, runNum))[:, gen]

    total_pop = []
    pop_to_save = []
    for j in range(fit1.shape[0]):
        total_pop.append(Indiv(fit1[j], fit2[j], names[j]))
    for ind1 in total_pop:
        for ind2 in total_pop:
            if ind1 != ind2 and not ind1.remove:
                ind1.remove = dominates_afpo(ind2, ind1)

    for ind in total_pop:
        if not ind.remove:
            pop_to_save.append(ind)

    pop_to_save = sorted(pop_to_save, key=lambda indiv: indiv.fit1)

    fits1 = []
    fits2 = []
    names = []
    for ind in pop_to_save:
        fits1.append(ind.fit1)
        fits2.append(ind.fit2)
        names.append(ind.name)
        # print('Ind', ind.name, 'Fit1', ind.fit1, "Fit2", ind.fit2)
    np.save('data/{}/run{}/pareto_fit1'.format(run, runNum), fits1)
    np.save('data/{}/run{}/pareto_fit2'.format(run, runNum), fits2)
    np.save('data/{}/run{}/pareto_names'.format(run, runNum), names)



if __name__ == '__main__':
    runName1 = 'bm_afpo'
    runName2 = 'bm_quadruped'
    gen = 49

    afpo_bots = []
    moo_bots = []
    afpo_fit1s = []
    moo_fit1s = []
    moo_fit2s = []
    for i in range(30):
        print('------------------------------------------------------')
        print('Run', i)
        get_pareto_front(runName2, i, gen)
        get_pareto_front_afpo(runName1, i, gen)
        best_afpo, afpo_fit1, age = locate_knee_afpo(runName1, i)
        afpo_bots.append(best_afpo)
        afpo_fit1s.append(afpo_fit1)
        best_moo, moo_fit1, moo_fit2 = locate_knee(runName2, i)
        moo_bots.append(best_moo)
        moo_fit1s.append(moo_fit1)
        moo_fit2s.append(moo_fit2)
        print("AFPO Best Fit1", afpo_fit1, 'name', best_afpo)
        print("MOO Best Fit1", moo_fit1, "Fit2", moo_fit2, 'name', best_moo)


    np.save('data/{}/bestindivs'.format(runName1), afpo_bots)
    np.save('data/{}/bestindivs_fit1'.format(runName1), afpo_fit1s)
    np.save('data/{}/bestindivs'.format(runName2), moo_bots)
    np.save('data/{}/bestindivs_fit1'.format(runName2), moo_fit1s)
    np.save('data/{}/bestindivs_fit2'.format(runName2), moo_fit2s)