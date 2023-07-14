import random
import numpy as np
from scipy.optimize import milp, LinearConstraint
from line_profiler_pycharm import profile

def createSet(Totalsize=10, numSubsets=20):
    # to generate .txt file
    # Totalsize: how big the whole "universe" is
    # numSubsets: how many subsets to be generated
    totalsize = Totalsize
    numSubsets = numSubsets

    # creates list of all numbers to make the subsets from
    universe = set(range(1, totalsize + 1))
    subsets = []

    # generate each subset
    for i in range(numSubsets):
        # random the size of subset always less than or equal to half the universe size
        subset_size = random.randint(1, totalsize // 2)
        # getting sample of numbers from universe the size of the subset
        subset = set(random.sample(universe, subset_size))
        subsets.append(subset)

    # write to input.txt file
    with open('input.txt', 'w') as f:
        # first line is universe size and num of subsets
        f.write(f"{totalsize} {numSubsets}\n")
        # second line is universe
        f.write(" ".join(str(x) for x in universe) + "\n")
        # all subsequent lines are subsets
        for subset in subsets:
            f.write(f"{' '.join(str(x) for x in subset)}\n")

def read_input_file(file_path):
    with open(file_path) as f:
        lines = f.readlines()

    # universe set is line 1
    universe = set(map(int, lines[1].split()))
    subsets = []

    # adding subsets to list
    for line in lines[2:]:
        subset = set(map(int, line.split()))
        subsets.append(subset)

    # Doesn't print when more than 20 subsets
    if len(subsets) < 20:
        print(f"Universe: {universe}")
        for idx, i in enumerate(subsets):

            print(f"Subset {idx}: {i}")
    else:
        print(f"Universe size: {len(universe)}")
        print(f"{len(subsets)} subsets")

    return universe, subsets

def greedy_set_cover(universe, subsets):
    # to find set cover of our inputs given the universe and subsets
    # empty set of covered elements
    covered = set()
    # empty list for sets that are used to cover
    cover = []
    # copy as to not change original subsets object
    subsetsCopy = subsets.copy()
    # while sets in covered don't match sets in the universe
    while covered != universe and subsetsCopy:
        # find the subset with most elements not already in covered and add it to cover
        subset = max(subsetsCopy, key=lambda s: len(s - covered))
        cover.append(subset)
        # remove subset to avoid infinite loop
        subsetsCopy.remove(subset)
        # add elements not in covered but in subset
        covered |= subset

    # when all elements added to cover but universe not covered for subsets generated that have no solution
    if not subsetsCopy and covered != universe:
        print("No Solution")
        cover = []
        return cover
    else:
        return cover

def milp_set_cover(universe, subsets):
    # lengths of universe and subsets for making constraints
    n = len(universe)
    m = len(subsets)

    # create matrix of subsets for constraints
    A = np.zeros((n, m))
    for i, element in enumerate(universe):
        for j, subset in enumerate(subsets):
            if element in subset:
                A[i, j] = 1

    # Create constraints: A - matrix defining constraint, and bounds: Lb- 1 (one subset) and Up - m (size of subsets)
    constraints = LinearConstraint(A, 1, m)

    # The coefficients of the linear objective function to be minimized
    # one for each subset since all have the same cost
    c = np.ones(m)

    # Solve the problem using milp
    result = milp(c, integrality=1, constraints=constraints)

    print(result.message)
    if result.success:
        # Get the selected subsets
        # round values in results as using >= 1 misses 0.9999
        selected_subsets = [i for i, value in enumerate(result.x) if round(value,1) >= 1]
        subcover = [subsets[i] for i in selected_subsets]
        return subcover
    else: return []

def checksolution(universe, coverset):
    # check if given cover is actually correct
    covered = set().union(*coverset)
    if covered == universe:
        return True
    else: return False


def run(universe=10, subsets=20):
    # creating new input file of desired universe size and num of subsets
    createSet(universe, subsets)

    # reading in input file
    universe, subsets = read_input_file('input.txt')

    # performing algorithms
    cover = greedy_set_cover(universe, subsets)
    greedysize = len(cover)
    lpcover = milp_set_cover(universe, subsets)
    lpsize = len(lpcover)

    print(f"Cover of greedy {greedysize}: {cover}")
    print(f"Cover of LP {lpsize}: {lpcover}")

    print(f"Check greedy solution Correct: {checksolution(universe, cover)}")
    print(f"Check lp solution Correct: {checksolution(universe, lpcover)}")

def performtests(largestUniverse=100, step=5):
    # performs tests starting at 5 to the largest size with a step size
    a = list(range(5,largestUniverse+5,step))
    print(f"Performing tests for universe of sizes {a}")
    for i in a:
        run(i, i*2)



performtests(500, 50)

