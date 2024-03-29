# Generated by Django 2.1.2 on 2018-12-11 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_tittle', models.CharField(max_length=20)),
                ('board_info', models.CharField(max_length=500)),
                ('board_file', models.FileField(null=True, upload_to='files/%Y/%m/%d')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lec_name', models.CharField(max_length=20)),
                ('lec_year', models.CharField(max_length=4)),
                ('lec_seme', models.CharField(max_length=1)),
                ('lec_info', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prof_id', models.EmailField(max_length=254, unique=True)),
                ('prof_num', models.CharField(max_length=200, unique=True)),
                ('prof_name', models.CharField(max_length=200)),
                ('prof_password', models.CharField(max_length=200)),
                ('prof_Phone', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_info', models.CharField(max_length=500)),
                ('reply_writer', models.CharField(max_length=200)),
                ('reply_file', models.FileField(null=True, upload_to='files/reply/%Y/%m/%d')),
                ('reply_board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supporter.Board')),
                ('reply_prof', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='supporter.Professor')),
            ],
        ),
        migrations.CreateModel(
            name='ReplyR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reply_info', models.CharField(max_length=500)),
                ('reply_writer', models.CharField(max_length=200)),
                ('reply_file', models.FileField(null=True, upload_to='files/reply/%Y/%m/%d')),
                ('reply_prof', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='supporter.Professor')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_tittle', models.CharField(max_length=20)),
                ('report_info', models.CharField(max_length=500)),
                ('report_file', models.FileField(null=True, upload_to='files/%Y/%m/%d')),
                ('report_endline', models.DateField()),
                ('report_lec', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supporter.Lecture')),
            ],
        ),
        migrations.CreateModel(
            name='Report_Stud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_writer', models.CharField(max_length=20)),
                ('report_tittle', models.CharField(max_length=20)),
                ('report_info', models.CharField(max_length=500)),
                ('report_file', models.FileField(null=True, upload_to='files/report/%Y/%m/%d')),
                ('report_report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supporter.Report')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stud_id', models.EmailField(max_length=254, unique=True)),
                ('stud_num', models.CharField(max_length=200, unique=True)),
                ('stud_name', models.CharField(max_length=200)),
                ('stud_password', models.CharField(max_length=200)),
                ('stud_Phone', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='report_stud',
            name='report_stud',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supporter.Student'),
        ),
        migrations.AddField(
            model_name='replyr',
            name='reply_report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supporter.Report'),
        ),
        migrations.AddField(
            model_name='replyr',
            name='reply_stud',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='supporter.Student'),
        ),
        migrations.AddField(
            model_name='reply',
            name='reply_stud',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='supporter.Student'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='lec_prof',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supporter.Professor'),
        ),
        migrations.AddField(
            model_name='board',
            name='board_lec',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supporter.Lecture'),
        ),
        migrations.AddField(
            model_name='attend',
            name='att_lect',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supporter.Lecture'),
        ),
        migrations.AddField(
            model_name='attend',
            name='att_stud',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supporter.Student'),
        ),
    ]
