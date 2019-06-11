# Generated by Django 2.2 on 2019-06-09 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drug', '0010_auto_20190609_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drugs',
            name='brand_name',
            field=models.CharField(help_text='This is the drug brand name', max_length=100, verbose_name='Brand name'),
        ),
        migrations.AlterField(
            model_name='drugs',
            name='des',
            field=models.TextField(max_length=1000, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='drugs',
            name='generic_name',
            field=models.CharField(blank=True, help_text='Drug scientific name (optional)', max_length=100, null=True, verbose_name='Generic name'),
        ),
    ]
