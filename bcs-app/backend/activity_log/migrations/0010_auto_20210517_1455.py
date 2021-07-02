# Generated by Django 3.2.2 on 2021-05-17 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity_log', '0009_auto_20190417_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useractivitylog',
            name='activity_status',
            field=models.CharField(choices=[('完成', 'completed'), ('错误', 'error'), ('成功', 'succeed'), ('失败', 'failed')], default='', help_text='操作状态', max_length=32),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='activity_type',
            field=models.CharField(choices=[('创建', 'add'), ('更新', 'modify'), ('回滚', 'rollback'), ('删除', 'delete'), ('开始', 'begin'), ('结束', 'end'), ('启动', 'start'), ('暂停', 'pause'), ('继续', 'carryon'), ('停止', 'stop'), ('重启', 'restart')], default='', help_text='操作类型', max_length=32),
        ),
        migrations.AlterField(
            model_name='useractivitylog',
            name='resource_type',
            field=models.CharField(blank=True, choices=[('项目', 'project'), ('集群', 'cluster'), ('节点', 'node'), ('命名空间', 'namespace'), ('模板集', 'template'), ('应用', 'instance'), ('Service', 'service'), ('Ingress', 'ingress'), ('LoadBalancer', 'lb'), ('Configmap', 'configmap'), ('Secret', 'secret'), ('Metric', 'metric'), ('WebConsole', 'web_console'), ('Helm', 'helm_app'), ('HPA', 'hpa')], help_text='操作对象类型', max_length=32, null=True),
        ),
    ]
