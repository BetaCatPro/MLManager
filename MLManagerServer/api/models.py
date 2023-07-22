from datetime import datetime

from django.db import models


STATUS_CHOICES = [
        (ERROR, 'Error'),
        (FINISHED, 'Finished'),
        (PAUSE, 'Pause'),
    ]


class AlgExperiments(models.Model):
    """
    实验记录
    """
    name = models.CharField(max_length=128, verbose_name='实验记录名称')
    description = models.CharField(max_length=256, verbose_name='实验记录描述')
    time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '实验记录表'
        verbose_name_plural = "实验记录表"
        db_table = 'ml_experiments'


class AlgParameters(models.Model):
    """
    实验参数
    """
    name = models.CharField(max_length=64, verbose_name='实验参数名称')
    value = models.CharField(max_length=32, verbose_name='实验参数值')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '实验参数表'
        verbose_name_plural = "实验参数表"
        db_table = 'ml_Parameters'


class AlgMetrics(models.Model):
    """
    实验算法评估指标
    """
    name = models.CharField(max_length=64, verbose_name='指标名称')
    value = models.CharField(max_length=32, verbose_name='指标值')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '实验算法评估指标表'
        verbose_name_plural = "实验算法评估指标表"
        db_table = 'ml_Metrics'


class AlgModels(models.Model):
    """
    算法模型
    """
    name = models.CharField(max_length=128, verbose_name='算法模型名称')
    file = models.CharField(max_length=256, verbose_name='算法模型保存位置')
    time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '算法模型表'
        verbose_name_plural = "算法模型表"
        db_table = 'ml_algorithms'
        

class AlgExperimentsList(models.Model):
    """
    实验记录列表
    """
    experiment = models.ForeignKey(to=AlgExperiments, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, verbose_name='实验记录名称')
    runid = models.CharField(max_length=64, verbose_name='实验运行记录ID')
    duration = models.CharField(max_length=64, verbose_name='实验持续时间')
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=FINISHED, verbose_name='实验进行状态')
    description = models.CharField(max_length=256, verbose_name='实验记录描述')
    parameters = models.ForeignKey(to=AlgParameters, on_delete=models.CASCADE)
    metrics = models.ForeignKey(to=AlgMetrics, on_delete=models.CASCADE)
    tags = models.CharField(max_length=64, verbose_name='实验性质标签')
    models = models.ForeignKey(to=AlgModels, on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '实验记录表'
        verbose_name_plural = "实验记录表"
        db_table = 'ml_experiments'
