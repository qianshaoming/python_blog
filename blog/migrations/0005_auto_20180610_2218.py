# Generated by Django 2.0.6 on 2018-06-10 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180607_2148'),
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='友链标题')),
                ('href', models.URLField(verbose_name='友链地址')),
                ('status', models.PositiveIntegerField(choices=[(1, '正常'), (2, '删除')], default=1, verbose_name='状态')),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-id'], 'verbose_name': '文章分类', 'verbose_name_plural': '文章分类'},
        ),
    ]
