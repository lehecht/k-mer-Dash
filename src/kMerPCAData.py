from processing import Processing
import os
import pandas as pd
from sklearn.decomposition import PCA
from sklearn import preprocessing


class KMerPCAData(Processing):

    def __init__(self, data, selected, k, peak, top):
        super().__init__(data, selected, k, peak, top)

    def processData(self):
        fileName1 = os.path.basename(self.getSettings().getSelected()[0])
        fileName2 = os.path.basename(self.getSettings().getSelected()[1])
        df = self.getDF()[[fileName1, fileName2]]

        pca = PCA()
        scaled_data = preprocessing.scale(df)
        pca_data = pca.fit_transform(scaled_data)
        pca_df = pd.DataFrame(data=pca_data, columns=['PC1', 'PC2'], index=df.index.tolist())

        return pca_df
