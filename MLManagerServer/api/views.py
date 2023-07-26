import random
import os
import pandas as pd
import uuid 

from django.views import View
from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse, Http404, StreamingHttpResponse
from django.http import QueryDict

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
        ratio = request.GET.get('data_ratio', '0.025')
        
        exp_list = AlgExperimentsList.objects.filter(experiment=master_exp_id, dataset=dataset, ratio=ratio)[:6]
        resp_data = serialize('json', exp_list)
        return HttpResponse(resp_data, "application/json")
    
    def delete(self, request):
        delete = QueryDict(request.body)
        exp_id = delete.get('exp_id')
        AlgExperimentsList.objects.filter(id=exp_id).delete()
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'}, safe=False)
    
    def put(self, request):
        update = QueryDict(request.body)
        exp_id = update.get('exp_id')
        exp_name = update.get('exp_name')
        AlgExperimentsList.objects.filter(id=exp_id).update(name = exp_name)
        return JsonResponse({'status': 200, 'code': 10000, 'msg': 'ok'}, safe=False)
    
class ExpParametersView(View):
    def get(self, request):
        exp_list_detail_id = request.GET.get('exp_detail_id')
        params = AlgParameters.objects.filter(exp_id=exp_list_detail_id)
        
        resp_data = {
            'name': params.name,
            'value': params.value
        }
        return JsonResponse({'status': 200, 'code': 10000, 'msg': resp_data}, safe=False)
    
class ExpMetricsView(View):
    def get(self, request):
        exp_list_detail_id = request.GET.get('exp_detail_id')
        params = AlgMetrics.objects.filter(exp_id=exp_list_detail_id)
        
        resp_data = {
            'name': params.name,
            'value': params.value
        }
        return JsonResponse({'status': 200, 'code': 10000, 'msg': resp_data}, safe=False)


class DownloadModelsView(View):
    def get(self, request):
        try:
            pass
            # history = request.GET.get('history', 0)
            # self_ver_history = request.GET.get('self_history', '')

            # if self_ver_history:
            #     res = SelfHistory.objects.filter(history=self_ver_history).first()
            # else:
            #     res = ExpertGraHistory.objects.filter(history=int(history)).first()
            # weight = [res.APA_weight, res.Arc_weight, res.Variance_weight, res.SA_weight, res.RMS_weight]
            # xgboost_result(weight)
            # try:
            #     file_path = file_pathCSV
            #     response = StreamingHttpResponse(open(file_path, 'rb'))
            #     response['content_type'] = "application/octet-stream"
            #     response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            #     return response
            # except Exception as e:
            #     raise Http404
        except Exception:
            raise Http404
