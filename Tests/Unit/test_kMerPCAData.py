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
    tFreq1 = results[4].Frequency.values.tolist()
    tFreq2 = results[5].Frequency.values.tolist()
    fileName1 = results[2]
    fileName2 = results[3]

    # Testing
    assert kmer_list1 == ['AAACC', 'AACCC', 'ACCCC']
    assert kmer_list2 == ['TTTGG', 'TTGGG', 'TGGGG']
    assert fileName1 == "testFile1.fa"
    assert fileName2 == "testFile2.fa"
    assert tFreq1 == [1, 2, 2]
    assert tFreq2 == [1, 2, 3]
