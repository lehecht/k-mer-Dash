from src.kMerPCAData import KMerPCAData
from src.processing import Processing


def test_processData():
    # Test1
    # Preparation
    testData = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]
    k = 5
    top = 3
    peak = None
    process = Processing(testData, None, k, peak, top)

    # Executing
    results = KMerPCAData.processData(process)

    kmer_list1 = results[0].index.tolist()
    kmer_list2 = results[1].index.tolist()
    tFreq1 = results[4].values.tolist()
    tFreq2 = results[5].values.tolist()
    fileName1 = results[2]
    fileName2 = results[3]

    # Testing
    assert kmer_list1 == ['AACCC', 'ACCCC', 'AAAAA']
    assert kmer_list2 == ['TTTGG', 'GTTGG', 'GGGGC', 'GGGCA', 'TTGGG', 'TGGGG']
    assert fileName1 == "testFile1.fa"
    assert fileName2 == "testFile2.fa"
    assert tFreq1 == [0, 0, 0]
    assert tFreq2 == [3, 2, 0, 0, 2, 1]
