from src.kMerScatterPlotData import KMerScatterPlotData as sctPlt
from src.processing import Processing


def test_processData():
    # Test1
    # Preparation
    testData = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]
    k = 5
    top = 3
    highlight = 2
    peak = None
    process = Processing(testData, None, k, peak, top)

    # Execution
    results = sctPlt.processData(process)
    df = results[0]
    label = results[1]
    fileName1 = results[2][0]
    fileName2 = results[2][1]
    xAxis = df[fileName1].values.tolist()
    yAxis = df[fileName2].values.tolist()
    highlight = df['highlight'].values.tolist()

    # Testing
    assert len(xAxis) == len(yAxis)
    assert xAxis == [1, 2, 2, 1, 3, 0, 0, 0, 0, 0, 0]
    assert yAxis == [0, 0, 0, 0, 0, 1, 2, 3, 1, 1, 1]
    assert label == ["AAACC", "AACCC", "ACCCC", "CAACC", "AAAAA", "TTTGG", "TTGGG", "TGGGG", "GTTGG", "GGGGC", "GGGCA"]
    assert fileName1 == "testFile1.fa"
    assert fileName2 == "testFile2.fa"

    # Test2: with peak position
    # Preparation
    testData = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]
    k = 5
    top = 3
    highlight = 1
    peak = 2
    process2 = Processing(testData, None, k, peak, top)

    # Execution
    results2 = sctPlt.processData(process2)
    df = results2[0]
    label = results2[1]
    fileName1 = results2[2][0]
    fileName2 = results2[2][1]
    xAxis = df[fileName1].values.tolist()
    yAxis = df[fileName2].values.tolist()
    highlight = df['highlight'].values.tolist()

    print(label)
    # Testing
    assert len(xAxis) == len(yAxis)
    assert xAxis == [1, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    assert yAxis == [0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 1, 1, 1]
    assert label == ['aAacc', 'Aaccc', 'acccc', 'cAacc', 'aAaaa', 'Aaaaa', 'aaaaa', 'tTtgg', 'Ttggg', 'tgggg', 'gTtgg',
                     'tGggg', 'Ggggc', 'gggca']

    assert fileName1 == "testFile1.fa"
    assert fileName2 == "testFile2.fa"
