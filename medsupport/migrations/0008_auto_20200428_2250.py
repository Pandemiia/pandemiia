# Generated by Django 3.0.4 on 2020-04-28 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medsupport', '0007_auto_20200421_0119'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolutionType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Назва типу товару товару')),
            ],
            options={
                'verbose_name': 'Тип засобу',
                'verbose_name_plural': 'Тип засобів',
            },
        ),
        migrations.AlterModelOptions(
            name='hospital',
            options={'ordering': ['pk'], 'verbose_name': 'Медичний заклад', 'verbose_name_plural': 'Медичні заклади'},
        ),
        migrations.RemoveField(
            model_name='hospitalneed',
            name='solution',
        ),
        migrations.AlterField(
            model_name='solution',
            name='attachment',
            field=models.URLField(blank=True, verbose_name='Посилання на завантаження архіву'),
        ),
        migrations.AddField(
            model_name='hospitalneed',
            name='solution_type',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='medsupport.SolutionType', verbose_name='Тип рішення'),
            preserve_default=False,
        ),
    ]