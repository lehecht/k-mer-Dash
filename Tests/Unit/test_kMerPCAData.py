from src.kMerPCAData import KMerPCAData
from src.processing import Processing


def test_processData():
    # Test1
    # Preparation
    testData = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]
    k = 5
    top = 3
    highlight = 0
    peak = None
    process = Processing(testData, None, k, peak, top, highlight)

    # Executing
    results = KMerPCAData.processData(process)

    kmer_list1 = results[0].index.tolist()
    kmer_list2 = results[1].index.tolist()
    freq1 = results[4].Frequency.values.tolist()
    freq2 = results[5].Frequency.values.tolist()
    fileName1 = results[2]
    fileName2 = results[3]

    # Testing
    assert kmer_list1 == ['AAACC', 'AACCC', 'ACCCC']
    assert kmer_list2 == ['TTTGG', 'TTGGG', 'TGGGG']
    assert fileName1 == "testFile1.fa"
    assert fileName2 == "testFile2.fa"
    assert freq1 == [1, 2, 2]
    assert freq2 == [1, 2, 3]

    # Test2 with peak-position
    # Preparation
    k = 5
    top = 3
    highlight = 0
    peak = 2
    process2 = Processing(testData, None, k, peak, top, highlight)

    # Executing
    results2 = KMerPCAData.processData(process2)

    kmer_list1 = results2[0].index.tolist()
    kmer_list2 = results2[1].index.tolist()
    freq1 = results2[4].Frequency.values.tolist()
    freq2 = results2[5].Frequency.values.tolist()
    fileName1 = results2[2]
    fileName2 = results2[3]

    # Testing
    print(process2.getTopKmer())
    assert kmer_list1 == ['aAacc', 'Aaccc', 'acccc']
    assert kmer_list2 == ['tTtgg', 'Ttggg', 'tgggg']
    assert fileName1 == "testFile1.fa"
    assert fileName2 == "testFile2.fa"
    assert freq1 == [1, 2, 2]
    assert freq2 == [1, 2, 2]
