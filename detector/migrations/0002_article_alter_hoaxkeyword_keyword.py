# Generated by Django 4.1.4 on 2023-07-13 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detector', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('is_hoax', models.BooleanField(default=False)),
                ('emotion', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='hoaxkeyword',
            name='keyword',
            field=models.CharField(max_length=100),
        ),
    ]
