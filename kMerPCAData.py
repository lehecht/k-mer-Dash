from processing import Processing
import os
import pandas as pd
from sklearn.decomposition import PCA


class KMerPCAData(Processing):

    def __init__(self, data, selected, k, peak, top):
        super().__init__(data, selected, k, peak, top)

    def processData(self):
        fileName1 = os.path.basename(self.getSettings().getSelected()[0])
        fileName2 = os.path.basename(self.getSettings().getSelected()[1])
        df = self.getDF()[[fileName1, fileName2]]

        pca = PCA(n_components=2)
        components = pca.fit_transform(df)  # preprocessing the data
        pca_df = pd.DataFrame(data=components, columns=['PC1', 'PC2'], index=df.index.tolist())

        return pca_df
