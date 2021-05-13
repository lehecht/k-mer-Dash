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

    # Test3 without peak-position
    # Preparation
    k = 5
    top = 10
    peak = None
    process3 = KMerPCAData(test_data, None, k, peak, top, None)

    # Executing
    results3 = KMerPCAData.processData(process3)

    kmer_list1 = results3[0].index.tolist()
    kmer_list2 = results3[1].index.tolist()
    freq1 = results3[4]
    freq2 = results3[5]
    file_name1 = results3[2]
    file_name2 = results3[3]

    nucl_count1 = freq1[['A', 'C', 'G', 'T']]
    nucl_count2 = freq2[['A', 'C', 'G', 'T']]

    trip_count1 = freq1.loc[:, "AAA":"TTT"]
    trip_count2 = freq2.loc[:, "AAA":"TTT"]

    # Testing
    assert kmer_list1 == ['AAAAA', 'AACCC', 'ACCCC', 'AAACC', 'CAACC']
    assert kmer_list2 == ['TGGGG', 'TTGGG', 'TTTGG', 'GTTGG', 'GGGGC', 'GGGCA']
    assert file_name1 == "testFile1.fa"
    assert file_name2 == "testFile2.fa"

    for i in range(0, len(nucl_count1.index)):
        assert sum(list(nucl_count1.iloc[i])) == k

    for i in range(0, len(nucl_count2.index)):
        assert sum(list(nucl_count2.iloc[i])) == k

    for i in range(0, len(trip_count1.index)):
        assert sum(list(trip_count1.iloc[i])) == 7 - k + 1

    for i in range(0, len(trip_count2.index)):
        assert sum(list(trip_count2.iloc[i])) == 7 - k + 1

    # Test4 with peak-position
    # Preparation
    k = 5
    top = 10
    peak = 3
    process4 = KMerPCAData(test_data, None, k, peak, top, None)

    # Executing
    results4 = KMerPCAData.processData(process4)

    kmer_list1 = results4[0].index.tolist()
    kmer_list2 = results4[1].index.tolist()
    freq1 = results4[4]
    freq2 = results4[5]
    file_name1 = results4[2]
    file_name2 = results4[3]

    nucl_count1 = freq1[['A', 'C', 'G', 'T']]
    nucl_count2 = freq2[['A', 'C', 'G', 'T']]

    trip_count1 = freq1.loc[:, "AAA":"TTT"]
    trip_count2 = freq2.loc[:, "AAA":"TTT"]

    print(kmer_list1)
    print(kmer_list2)

    # Testing
    assert kmer_list1 == ['aAccc', 'Acccc', 'aaAcc', 'caAcc', 'aaAaa', 'aAaaa', 'Aaaaa']
    assert kmer_list2 == ['tTggg', 'Tgggg', 'ttTgg', 'gtTgg', 'tgGgg', 'gGggc', 'Gggca']
    assert file_name1 == "testFile1.fa"
    assert file_name2 == "testFile2.fa"

    for i in range(0, len(nucl_count1.index)):
        assert sum(list(nucl_count1.iloc[i])) == k

    for i in range(0, len(nucl_count2.index)):
        assert sum(list(nucl_count2.iloc[i])) == k

    for i in range(0, len(trip_count1.index)):
        assert sum(list(trip_count1.iloc[i])) == 7 - k + 1

    for i in range(0, len(trip_count2.index)):
        assert sum(list(trip_count2.iloc[i])) == 7 - k + 1
