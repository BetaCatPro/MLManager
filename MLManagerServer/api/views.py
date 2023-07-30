import random
import os
import pandas as pd
import uuid 

from django.views import View
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse, Http404, StreamingHttpResponse
from django.http import QueryDict
from django.db.models import Count, Avg

from api.models import AlgExperiments, AlgExperimentsList, AlgMetrics, AlgModels, AlgParameters

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
        all_exp = AlgExperiments.objects.all()
        resp_data = serialize('json', all_exp)
        return HttpResponse(resp_data, "application/json")

    def delete(self, request):
        delete = QueryDict(request.body)
        master_exp_id = delete.get('master_exp_id')
        AlgExperiments.objects.filter(id=master_exp_id).delete()
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'}, safe=False)
    
    def post(self, request):
        master_exp_id =  request.POST.get('master_exp_id')
        master_exp_name =  request.POST.get('master_exp_name')
        AlgExperiments.objects.filter(id=master_exp_id).update(name = master_exp_name)
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'}, safe=False)



class ExperimentsListView(View):
    def get(self, request):
        master_exp_id = request.GET.get('master_exp_id', 0)
        dataset = request.GET.get('data_set', 'abalone')
        ratio = request.GET.get('data_ratio', 0.005)
        
        page = int(request.GET.get('cur_page', 0))
        
        exp_list = AlgExperimentsList.objects.filter(experiment=master_exp_id, dataset=dataset, ratio=ratio)[6*page:6*page+6]
        # resp_data = serialize('json', exp_list)
        
        resp_data = {
            'total': exp_list.count(),
            'list': [{
                    'id': item.id,
                    'dataset': item.dataset,
                    'name': item.name,
                    'created': item.time,
                    'duration': item.duration,
                    'source': item.dataset,
                    'version': item.ratio
                } for item in exp_list]
            }
        
        # return HttpResponse(resp_data, "application/json")
        return JsonResponse({'status': 200, 'code': 10000, 'msg': resp_data}, safe=False)
    
    def delete(self, request):
        delete = QueryDict(request.body)
        exp_id = delete.get('exp_id', 0)
        AlgExperimentsList.objects.filter(id=exp_id).delete()
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'}, safe=False)
    
    def post(self, request):
        exp_id = request.POST.get('exp_id')
        exp_name = request.POST.get('exp_name')
        AlgExperimentsList.objects.filter(id=exp_id).update(name = exp_name)
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'}, safe=False)
    
    
class ExperimentsDetailView(View):
    def get(self, request):
        exp_id = request.GET.get('exp_detail_id', 0)
        
        exp_list = AlgExperimentsList.objects.get(id=exp_id)
        
        # 获取实验参数
        exp_params = AlgParameters.objects.filter(exp_id = exp_id)
        # 获取实验评估指标
        exp_metrics  = AlgMetrics.objects.filter(exp_id=exp_id)
        
        
        exp_detail_data = dict()
        exp_detail_data['exp_detail'] = {
            'dataset' : exp_list.dataset,
            'ratio' : exp_list.ratio,
            'name' : exp_list.name,
            'runid' : exp_list.runid,
            'duration' : exp_list.duration,
            'status' : exp_list.status,
            'description' : exp_list.description,
            'tags' : exp_list.tags,
            'time' : exp_list.time,
        }
        
        parma_list = []
        for pa in exp_params:
            parma_list.append({
            'name' : pa.name,
            'value': pa.value
        })
        exp_detail_data['exp_params'] = parma_list
        metrics_list = []
        for metric in exp_metrics:
            metrics_list.append({
            'name' : metric.name,
            'value': metric.value
        })
        exp_detail_data['exp_metrics'] = metrics_list
        return JsonResponse({'status': 200, 'code': 10000, 'msg': exp_detail_data}, safe=False)
    
    
class ExpDatasetAndRatioView(View):
    def get(self, request):
        datasets = AlgExperimentsList.objects.values('dataset').annotate(count=Count('id'))
        ratios = AlgExperimentsList.objects.values('ratio').annotate(count=Count('id'))
        
        resp_data = {
            'dataset': [dataset['dataset'] for dataset in datasets],
            'ratio': [ratio['ratio'] for ratio in ratios]
        }
        return JsonResponse({'status': 200, 'code': 10000, 'msg': resp_data}, safe=False)
    
class ExpStatisticView(View):
    def get(self, request):
        exp_id = request.GET.get('exp_id')
        
        result = []
        allDatasetList = AlgExperimentsList.objects.filter(experiment=exp_id).values('dataset').distinct()
        
        for ratio in [0.005, 0.025,0.05]:
            for dataset in allDatasetList:
                perDataset = AlgExperimentsList.objects.filter(experiment=exp_id, dataset=dataset.get('dataset'),ratio=ratio)
                
                data_li_list = [data.id for data in perDataset]
                # for data in perDataset:
                metrics = AlgMetrics.objects.filter(exp_id__in=data_li_list).values('name').annotate(mse_mean=Avg('value'))
                tmp_obj = {
                    'ratio': ratio,
                    'dataset': dataset.get('dataset'),
                    'co-train-rmse': metrics[0].get('mse_mean'),
                    'm5p-rmse':metrics[1].get('mse_mean')
                }                
                result.append(tmp_obj)
        
        return JsonResponse({'status': 200, 'code': 10000, 'msg': result}, safe=False)


class PerExpStatisticView(View):
    def get(self, request):
        exp_id = request.GET.get('exp_id')
        
        result = []
        allDatasetList = AlgExperimentsList.objects.filter(experiment=exp_id).values('dataset').distinct()
        
        for ratio in [0.005, 0.025,0.05]:
            for dataset in allDatasetList:
                perDataset = AlgExperimentsList.objects.filter(experiment=exp_id, dataset=dataset.get('dataset'),ratio=ratio)
                
                data_li_list = [data.id for data in perDataset]
                # for data in perDataset:
                metrics = AlgMetrics.objects.filter(exp_id__in=data_li_list).values('name').annotate(mse_mean=Avg('value'))
                tmp_obj = {
                    'ratio': ratio,
                    'dataset': dataset.get('dataset'),
                    'co-train-rmse': metrics[0].get('mse_mean'),
                    'm5p-rmse':metrics[1].get('mse_mean')
                }                
                result.append(tmp_obj)
        
        return JsonResponse({'status': 200, 'code': 10000, 'msg': result}, safe=False)
