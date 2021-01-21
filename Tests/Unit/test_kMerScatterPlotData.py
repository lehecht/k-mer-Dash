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
    process = Processing(testData, None, k, peak, top, None)

    # Execution
    results = sctPlt.processData(process)
    df = results[0]
    label = results[1]
    fileName1 = results[2][0]
    fileName2 = results[2][1]
    highlight = df['highlight'].values.tolist()

    res_kmer_list = ["AAACC", "AACCC", "ACCCC", "CAACC", "AAAAA", "TTTGG", "TTGGG", "TGGGG", "GTTGG", "GGGGC", "GGGCA"]
    res_xAxis = [1, 2, 2, 1, 3, 0, 0, 0, 0, 0, 0]
    res_yAxis = [0, 0, 0, 0, 0, 1, 2, 3, 1, 1, 1]
    xA_res_dict = dict(zip(res_kmer_list, res_xAxis))
    yA_res_dict = dict(zip(res_kmer_list, res_yAxis))

    # Testing

    # checks if frequencies are are equal
    for l in label:
        assert xA_res_dict[l] == df.loc[l, ['testFile1.fa']].tolist()[0]
        assert yA_res_dict[l] == df.loc[l, ['testFile2.fa']].tolist()[0]
    assert set(label) == {"AAACC", "AACCC", "ACCCC", "CAACC", "AAAAA", "TTTGG", "TTGGG", "TGGGG", "GTTGG", "GGGGC",
                          "GGGCA"}
    assert fileName1 == "testFile1.fa"
    assert fileName2 == "testFile2.fa"

    # Test2: with peak position
    # Preparation
    testData = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]
    k = 5
    top = 3
    highlight = 1
    peak = 2
    process2 = Processing(testData, None, k, peak, top, None)

    # Execution
    results2 = sctPlt.processData(process2)
    df = results2[0]
    label = results2[1]
    fileName1 = results2[2][0]
    fileName2 = results2[2][1]

    res_kmer_list = ['aAacc', 'Aaccc', 'acccc', 'cAacc', 'aAaaa', 'Aaaaa', 'aaaaa', 'tTtgg', 'Ttggg', 'tgggg', 'gTtgg',
                     'tGggg', 'Ggggc', 'gggca']
    res_xAxis = [1, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    res_yAxis = [0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 1, 1, 1]
    xA_res_dict = dict(zip(res_kmer_list, res_xAxis))
    yA_res_dict = dict(zip(res_kmer_list, res_yAxis))

    # Testing

    # checks if frequencies are are equal
    for l in label:
        assert xA_res_dict[l] == df.loc[l, ['testFile1.fa']].tolist()[0]
        assert yA_res_dict[l] == df.loc[l, ['testFile2.fa']].tolist()[0]

    assert set(label) == {'aAacc', 'Aaccc', 'acccc', 'cAacc', 'aAaaa', 'Aaaaa', 'aaaaa', 'tTtgg', 'Ttggg', 'tgggg',
                          'gTtgg',
                          'tGggg', 'Ggggc', 'gggca'}

    assert fileName1 == "testFile1.fa"
    assert fileName2 == "testFile2.fa"
