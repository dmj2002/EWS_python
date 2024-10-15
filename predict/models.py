from django.db import models
from django.apps import apps

# Create your models here.
class BaseMeasurement(models.Model):
    # 日期列
    datetime = models.DateTimeField()
    # status 列，表示状态，使用 tinyint（通过 IntegerField 实现，并限制其取值范围）
    STATUS_CHOICES = [
        (0, 'Inactive'),   # 0 表示状态为 Inactive
        (1, 'Active'),     # 1 表示状态为 Active
    ]
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)

    # value 列，表示测量的数值，使用 Double（通过 FloatField 实现）
    value = models.FloatField()
    class Meta:
        abstract = True

def create_table(table_name):
    # 检查模型是否已经注册
    try:
        # 使用 apps.get_model() 直接获取已注册模型
        existing_model = apps.get_model('predict', table_name)
        return existing_model
    except LookupError:
        # 如果模型尚未注册，则创建一个新的模型
        class Meta:
            db_table = table_name

        attrs = {'__module__': 'predict.models', 'Meta': Meta}

        # 动态创建模型
        table = type(table_name, (BaseMeasurement,), attrs)
        return table


