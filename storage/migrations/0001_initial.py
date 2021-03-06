# Generated by Django 2.1.4 on 2018-12-13 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashflowData',
            fields=[
                ('code', models.CharField(db_index=True, max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=8)),
                ('cf_sales', models.FloatField(null=True)),
                ('rateofreturn', models.FloatField(null=True)),
                ('cf_nm', models.FloatField(null=True)),
                ('cf_liabilities', models.FloatField(null=True)),
                ('cashflowratio', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DebtpayingData',
            fields=[
                ('code', models.CharField(db_index=True, max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=8)),
                ('currentratio', models.FloatField(null=True)),
                ('quickratio', models.FloatField(null=True)),
                ('cashratio', models.FloatField(null=True)),
                ('icratio', models.FloatField(null=True)),
                ('sheqratio', models.FloatField(null=True)),
                ('adratio', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GrowthData',
            fields=[
                ('code', models.CharField(db_index=True, max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=8)),
                ('mbrg', models.FloatField(null=True)),
                ('nprg', models.FloatField(null=True)),
                ('nav', models.FloatField(null=True)),
                ('targ', models.FloatField(null=True)),
                ('epsg', models.FloatField(null=True)),
                ('seg', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('day', models.DateField()),
                ('open', models.FloatField()),
                ('close', models.FloatField()),
                ('high', models.FloatField()),
                ('low', models.FloatField()),
                ('vol', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='OperationData',
            fields=[
                ('code', models.CharField(db_index=True, max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=8)),
                ('arturnover', models.FloatField(null=True)),
                ('arturndays', models.FloatField(null=True)),
                ('inventory_turnover', models.FloatField(null=True)),
                ('inventory_days', models.FloatField(null=True)),
                ('currentasset_turnover', models.FloatField(null=True)),
                ('currentasset_days', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProfitData',
            fields=[
                ('code', models.CharField(db_index=True, max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=8)),
                ('roe', models.FloatField(null=True)),
                ('net_profit_ratio', models.FloatField(null=True)),
                ('gross_profit_rate', models.FloatField(null=True)),
                ('net_profits', models.FloatField(null=True)),
                ('eps', models.FloatField(null=True)),
                ('business_income', models.FloatField(null=True)),
                ('bips', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReportData',
            fields=[
                ('code', models.CharField(db_index=True, max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=8)),
                ('eps', models.FloatField(null=True)),
                ('eps_yoy', models.FloatField(null=True)),
                ('bvps', models.FloatField(null=True)),
                ('roe', models.FloatField(null=True)),
                ('epcf', models.FloatField(null=True)),
                ('net_profits', models.FloatField(null=True)),
                ('profits_yoy', models.FloatField(null=True)),
                ('distrib', models.CharField(max_length=16, null=True)),
                ('report_date', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='StockBasics',
            fields=[
                ('code', models.CharField(db_index=True, max_length=6, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=8)),
                ('industry', models.CharField(max_length=8)),
                ('area', models.CharField(max_length=8)),
                ('pe', models.FloatField()),
                ('outstanding', models.FloatField()),
                ('totals', models.FloatField()),
                ('totalAssets', models.FloatField()),
                ('liquidAssets', models.FloatField()),
                ('fixedAssets', models.FloatField()),
                ('reserved', models.FloatField()),
                ('reservedPerShare', models.FloatField()),
                ('eps', models.FloatField()),
                ('bvps', models.FloatField()),
                ('pb', models.FloatField()),
                ('timeToMarket', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Tick',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('day', models.DateField()),
                ('sec1_buy', models.FloatField()),
                ('sec1_sell', models.FloatField()),
                ('sec2_buy', models.FloatField()),
                ('sec2_sell', models.FloatField()),
                ('sec3_buy', models.FloatField()),
                ('sec3_sell', models.FloatField()),
                ('sec4_buy', models.FloatField()),
                ('sec4_sell', models.FloatField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='tick',
            unique_together={('code', 'day')},
        ),
        migrations.AlterUniqueTogether(
            name='history',
            unique_together={('code', 'day')},
        ),
    ]
