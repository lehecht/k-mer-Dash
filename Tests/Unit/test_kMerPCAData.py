from src.kMerPCAData import KMerPCAData


def test_processData():
    # Test1
    # Preparation
    test_data = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]
    k = 5
    top = 3
    peak = None
    process = KMerPCAData(test_data, None, k, peak, top, None)

    triplets = process.all_triplets

    # Executing
    results = KMerPCAData.processData(process)

    kmer_list1 = results[0].index.tolist()
    kmer_list2 = results[1].index.tolist()
    freq1 = results[4].Frequency.values.tolist()
    freq2 = results[5].Frequency.values.tolist()
    file_name1 = results[2]
    file_name2 = results[3]

    # Testing
    assert kmer_list1 == ['AAAAA', 'AACCC', 'ACCCC']
    assert kmer_list2 == ['TGGGG', 'TTGGG', 'TTTGG', 'GTTGG', 'GGGGC', 'GGGCA']
    assert file_name1 == "testFile1.fa"
    assert file_name2 == "testFile2.fa"
    assert freq1 == [3, 2, 2]
    assert freq2 == [3, 2, 1, 1, 1, 1]
    assert len(triplets) == 64

    # Test2 with peak-position
    # Preparation
    k = 5
    top = 3
    peak = 2
    process2 = KMerPCAData(test_data, None, k, peak, top, None)

    # Executing
    results2 = KMerPCAData.processData(process2)

    kmer_list1 = results2[0].index.tolist()
    kmer_list2 = results2[1].index.tolist()
    freq1 = results2[4].Frequency.values.tolist()
    freq2 = results2[5].Frequency.values.tolist()
    file_name1 = results2[2]
    file_name2 = results2[3]

    # Testing
    assert kmer_list1 == ['Aaccc', 'acccc', 'aAacc', 'cAacc', 'aAaaa', 'Aaaaa', 'aaaaa']
    assert kmer_list2 == ['Ttggg', 'tgggg', 'tTtgg', 'gTtgg', 'tGggg', 'Ggggc', 'gggca']
    assert file_name1 == "testFile1.fa"
    assert file_name2 == "testFile2.fa"
    assert freq1 == [2, 2, 1, 1, 1, 1, 1]
    assert freq2 == [2, 2, 1, 1, 1, 1, 1]
