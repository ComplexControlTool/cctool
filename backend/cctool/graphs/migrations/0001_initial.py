# Generated by Django 2.0.9 on 2019-02-20 01:42

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('analysis_type', models.CharField(choices=[('CA', 'Controllability'), ('USA', 'Up stream'), ('DSA', 'Down stream'), ('SLA', 'Subjective logic'), ('XCS', 'XCS classifier')], default='CA', max_length=3, verbose_name='type of analysis')),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
            ],
            options={
                'verbose_name': 'analysis',
                'verbose_name_plural': 'analyses',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Edge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identifier', models.CharField(default='0-0', max_length=21, verbose_name='identifier of edge')),
                ('label', models.CharField(blank=True, max_length=255, verbose_name='label of edge')),
            ],
            options={
                'verbose_name': 'edge',
                'verbose_name_plural': 'edges',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Graph',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='Untitled Graph', max_length=255, verbose_name='title of graph')),
                ('description', models.TextField(blank=True, max_length=1500, verbose_name='description of graph')),
            ],
            options={
                'verbose_name': 'graph',
                'verbose_name_plural': 'graphs',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('identifier', models.IntegerField(default=-1, verbose_name='identifier of node')),
                ('label', models.CharField(default='Untitled Node', max_length=255, verbose_name='label of node')),
                ('position_x', models.IntegerField(blank=True, default=None, null=True, verbose_name='position on x-axis of node')),
                ('position_y', models.IntegerField(blank=True, default=None, null=True, verbose_name='position on y-axis of node')),
            ],
            options={
                'verbose_name': 'node',
                'verbose_name_plural': 'nodes',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Structure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
            ],
            options={
                'verbose_name': 'structure',
                'verbose_name_plural': 'structures',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Visualization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('options', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
                ('structure', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
            ],
            options={
                'verbose_name': 'visualization',
                'verbose_name_plural': 'visualizations',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EdgePlus',
            fields=[
                ('edge_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='graphs.Edge')),
                ('weight', models.CharField(choices=[('N', 'Neutral'), ('+W', 'Positive Weak'), ('+M', 'Positive Medium'), ('+S', 'Positive Strong'), ('-W', 'Negative Weak'), ('-M', 'Negative Medium'), ('-S', 'Negative Strong')], default='N', max_length=2, verbose_name='edge weight')),
                ('tags', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True)),
                ('custom', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
            ],
            options={
                'verbose_name': 'edge',
                'verbose_name_plural': 'edges',
                'abstract': False,
            },
            bases=('graphs.edge',),
        ),
        migrations.CreateModel(
            name='NodePlus',
            fields=[
                ('node_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='graphs.Node')),
                ('function', models.CharField(choices=[('L', 'Linear')], default='L', max_length=1, verbose_name='node function')),
                ('controllability', models.CharField(choices=[('N', 'Neutral'), ('E', 'Easy'), ('M', 'Medium'), ('H', 'Hard')], default='N', max_length=1, verbose_name='node controllability')),
                ('vulnerability', models.CharField(choices=[('N', 'None'), ('E', 'Low'), ('M', 'Medium'), ('H', 'High')], default='N', max_length=1, verbose_name='node vulnerability')),
                ('importance', models.CharField(choices=[('N', 'None'), ('L', 'Low'), ('H', 'High')], default='N', max_length=1, verbose_name='node importance')),
                ('tags', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True)),
                ('custom', django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True)),
            ],
            options={
                'verbose_name': 'node',
                'verbose_name_plural': 'nodes',
                'abstract': False,
            },
            bases=('graphs.node',),
        ),
        migrations.AddField(
            model_name='node',
            name='graph',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nodes', related_query_name='node', to='graphs.Graph'),
        ),
        migrations.AddField(
            model_name='graph',
            name='structure',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='graphs.Structure'),
        ),
        migrations.AddField(
            model_name='graph',
            name='visualization',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='graphs.Visualization'),
        ),
        migrations.AddField(
            model_name='edge',
            name='graph',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='edges', related_query_name='edge', to='graphs.Graph'),
        ),
        migrations.AddField(
            model_name='edge',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sources', related_query_name='source', to='graphs.Node'),
        ),
        migrations.AddField(
            model_name='edge',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targets', related_query_name='target', to='graphs.Node'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='edge',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='analyses', related_query_name='analysis', to='graphs.Edge'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='graph',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='analyses', related_query_name='analysis', to='graphs.Graph'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='analyses', related_query_name='analysis', to='graphs.Node'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='visualization',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='graphs.Visualization'),
        ),
    ]
