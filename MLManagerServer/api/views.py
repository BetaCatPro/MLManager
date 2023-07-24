import random
from django.http import JsonResponse
from django.views import View
from api.models import AlgExperiments, AlgExperimentsList, AlgMetrics, AlgModels, AlgParameters

import os
import pandas as pd
import uuid 


class insertToMySQL(View):
    def insertOneExpData(self, exp_name, exp_desc):
        
        exp = AlgExperiments.objects.create(
            name = exp_name,
            description = exp_desc
        )
        
        base_power = 1
        
        base_path = './data/{}/'.format(exp_name)
        dataset_list_dir = os.listdir(base_path)
        for data_set in dataset_list_dir:
            ratio_dir =  os.listdir(os.path.join(base_path, data_set))
            for ratio in ratio_dir:
                if not os.path.isfile(os.path.join(base_path, data_set, ratio)):          
                    csv_file_list = os.listdir(os.path.join(base_path, data_set, ratio))
                    for csv_file in csv_file_list:
                        csv_file_path = os.path.join(base_path, data_set, ratio, csv_file)
                        
                        csv_data = pd.read_csv(csv_file_path).iloc[:, 3:]
                        
                        exp_list = AlgExperimentsList.objects.create(
                            experiment = exp,
                            dataset = data_set,
                            ratio = ratio,
                            name = csv_file.split('.csv')[0],
                            runid = uuid.uuid4(),
                            duration = '{} s'.format(base_power * random.randint(10, 40)),
                            status = 'FINISHED',
                            description = '',
                            tags = 'ssl, coreg, m5, dt',
                        )
                        
                        AlgParameters.objects.create(
                            exp_id = exp_list,
                            name = '基础算法',
                            value = 'dt'
                        )
                        
                        AlgParameters.objects.create(
                            exp_id = exp_list,
                            name = '迭代次数',
                            value = 'dt'
                        )
                        
                        AlgParameters.objects.create(
                            exp_id = exp_list,
                            name = '每次选取无标签数据数量',
                            value = '2'
                        )
                        
                        AlgParameters.objects.create(
                            exp_id = exp_list,
                            name = '度量空间维度',
                            value = '64'
                        )
                        
                        AlgMetrics.objects.create(
                            exp_id = exp_list,
                            name = 'co_train_rmse',
                            value = csv_data['co_train_rmse'][0]
                        )
                        
                        AlgMetrics.objects.create(
                            exp_id = exp_list,
                            name = 'm5p_rmse',
                            value = csv_data['m5p_rmse'][0]
                        )
                        
                        AlgModels.objects.create(
                            exp_id = exp_list,
                            name = 'm5p_rmse',
                            file = csv_file_path
                        )
            base_power = base_power*10
        
    def get(self, request):
        self.insertOneExpData('experiment', '在不改变算法框架的基础上, 选取不同的基础算法用于协同训练')        
        self.insertOneExpData('metric_ablation_experiment', '基础算法使用 coreg 协同模型, 进行度量空间训练的消融实验')        
        self.insertOneExpData('stable_ablation_experiment', '基础算法使用 coreg 协同模型, 进行挑选稳定样本的消融实验')        
        return JsonResponse({'status': 200, 'code': 100000, 'msg': 'ok'})

class ExperimentsView(View):
    def get(self, request):
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'})


class ExperimentsListView(View):
    def get(self, request):
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'})
    
class ExpParametersView(View):
    def get(self, request):
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'})
    
class ExpMetricsView(View):
    def get(self, request):
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'})

class ExpModelsView(View):
    def get(self, request):
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'})


class DownloadModelsView(View):
    def get(self, request):
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'})
