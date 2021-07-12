
def readAthalianaData():
    f = open("data/athalianaData/elementstring_tuples.txt", "r")
    content = f.readlines()
    norm_vector = dict()
    in_vivo_vec = dict()
    in_silico_vec = dict()
    in_vivo_sum = 0
    in_silico_sum = 0

    for line in content:
        l = line.split()
        kmer = l[1]
        count = int(l[2])

        norm_vector[kmer] = 0

        if in_vivo_vec.get(kmer) is None:
            in_vivo_vec[kmer] = count
            in_vivo_sum += count
        else:
            in_silico_vec[kmer] = count
            in_silico_sum += count

    in_vivo_vec = {k: (v/in_vivo_sum) for (k,v) in in_vivo_vec.items()}
    in_silico_vec = {k: (v/in_silico_sum) for (k,v) in in_silico_vec.items()}

    norm_vector = {kmer: ((in_vivo_vec[kmer]+in_silico_vec[kmer])/2) for kmer in norm_vector.keys()}

    return norm_vector




