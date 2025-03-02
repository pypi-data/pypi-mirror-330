import os
import kagglehub
import functools

def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            for dataSetPath in self.dataSetPaths:
                if os.path.exists(dataSetPath):
                    self.exist = True
            if not self.exist:
                return func(self, *args, **kwargs)  # Dataset yoksa fonksiyonu çalıştır
            else:
                print("Dataset already exists, skipping download.")
        return wrapper

class GetDataSetFromKaggle:
    def __init__(self, path):
        '''
            Example data path as url:
            https://www.kaggle.com/datasets/hunter0007/ecommerce-dataset-for-predictive-marketing-2023/data
        '''
        self.cachePath = None
        cwd = os.getcwd()
        self.dataSetsDir = os.path.join(cwd, "__dataSets")
        _splitted = path.split("/")
        self.kagglePath = f"{_splitted[4]}/{_splitted[5]}"
        self.dataSetPaths = []
        self.exist = False
        self.__call__(self)

    @decorator
    def __call__(self, *args, **kwargs):
        self.cachePath = kagglehub.dataset_download(self.kagglePath)
        
        for dataSet in os.listdir(self.cachePath):
            _from = os.path.join(self.cachePath ,dataSet)
            to_ = os.path.join(self.dataSetsDir, dataSet)
            os.makedirs(self.dataSetsDir, exist_ok=True)
            os.replace(_from, to_)
            self.dataSetPaths.append(to_)

    def getDataSets(self):
        return self.dataSetPaths
