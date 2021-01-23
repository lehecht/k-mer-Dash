from src.kMerScatterPlotData import KMerScatterPlotData as sctPlt


def test_processData():
    # Test1
    # Preparation
    test_data = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]
    k = 5
    top = 3
    peak = None
    process = sctPlt(test_data, None, k, peak, top, None)

    # Execution
    results = sctPlt.processData(process)
    df = results[0]
    labels = results[1]
    file_name1 = results[2][0]
    file_name2 = results[2][1]

    res_kmer_list = ["AAACC", "AACCC", "ACCCC", "CAACC", "AAAAA", "TTTGG", "TTGGG", "TGGGG", "GTTGG", "GGGGC", "GGGCA"]
    res_x_axis = [1, 2, 2, 1, 3, 0, 0, 0, 0, 0, 0]
    res_y_axis = [0, 0, 0, 0, 0, 1, 2, 3, 1, 1, 1]
    x_a_res_dict = dict(zip(res_kmer_list, res_x_axis))
    y_a_res_dict = dict(zip(res_kmer_list, res_y_axis))

    # Testing

    # checks if frequencies are are equal
    for label in labels:
        assert x_a_res_dict[label] == df.loc[label, ['testFile1.fa']].tolist()[0]
        assert y_a_res_dict[label] == df.loc[label, ['testFile2.fa']].tolist()[0]
    assert set(labels) == {"AAACC", "AACCC", "ACCCC", "CAACC", "AAAAA", "TTTGG", "TTGGG", "TGGGG", "GTTGG", "GGGGC",
                           "GGGCA"}
    assert file_name1 == "testFile1.fa"
    assert file_name2 == "testFile2.fa"

    # Test2: with peak position
    # Preparation
    test_data = ["Tests/Unit/testdata/testFile1.fa", "Tests/Unit/testdata/testFile2.fa"]
    k = 5
    top = 3
    peak = 2
    process2 = sctPlt(test_data, None, k, peak, top, None)

    # Execution
    results2 = sctPlt.processData(process2)
    df = results2[0]
    labels = results2[1]
    file_name1 = results2[2][0]
    file_name2 = results2[2][1]

    res_kmer_list = ['aAacc', 'Aaccc', 'acccc', 'cAacc', 'aAaaa', 'Aaaaa', 'aaaaa', 'tTtgg', 'Ttggg', 'tgggg', 'gTtgg',
                     'tGggg', 'Ggggc', 'gggca']
    res_x_axis = [1, 2, 2, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0]
    res_y_axis = [0, 0, 0, 0, 0, 0, 0, 1, 2, 2, 1, 1, 1, 1]
    x_a_res_dict = dict(zip(res_kmer_list, res_x_axis))
    y_a_res_dict = dict(zip(res_kmer_list, res_y_axis))

    # Testing

    # checks if frequencies are are equal
    for label in labels:
        assert x_a_res_dict[label] == df.loc[label, ['testFile1.fa']].tolist()[0]
        assert y_a_res_dict[label] == df.loc[label, ['testFile2.fa']].tolist()[0]

    assert set(labels) == {'aAacc', 'Aaccc', 'acccc', 'cAacc', 'aAaaa', 'Aaaaa', 'aaaaa', 'tTtgg', 'Ttggg', 'tgggg',
                           'gTtgg',
                           'tGggg', 'Ggggc', 'gggca'}

    assert file_name1 == "testFile1.fa"
    assert file_name2 == "testFile2.fa"
