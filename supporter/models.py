from django.db import models

# Create your models here.
class Professor(models.Model):
    prof_id = models.EmailField(unique = True)
    prof_num = models.CharField(max_length=200, unique = True)
    prof_name = models.CharField(max_length=200)
    prof_password = models.CharField(max_length=200)
    prof_Phone = models.CharField(max_length=200)

    def __str__(self):
        return self.prof_name

class Student(models.Model):
    stud_id = models.EmailField(unique=True)
    stud_num = models.CharField(max_length=200, unique= True)
    stud_name = models.CharField(max_length=200)
    stud_password = models.CharField(max_length=200)
    stud_Phone = models.CharField(max_length=200)

    def __str__(self):
        return self.stud_name

class Lecture(models.Model):
    lec_name = models.CharField(max_length = 20)
    lec_year = models.CharField(max_length = 4)
    lec_seme = models.CharField(max_length = 1)
    lec_info = models.CharField(max_length = 500)
    lec_prof = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return self.lec_name

class Board(models.Model):
    board_tittle = models.CharField(max_length = 20)
    board_info = models.CharField(max_length = 500)
    board_file = models.FileField(upload_to = 'files/%Y/%m/%d', null = True)
    board_lec = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.board_tittle

class Reply(models.Model):
    reply_info = models.CharField(max_length = 500)
    reply_writer = models.CharField(max_length = 200)
    reply_prof = models.ForeignKey(Professor, on_delete=models.CASCADE, null = True)
    reply_stud = models.ForeignKey(Student, on_delete=models.CASCADE, null = True)
    reply_board = models.ForeignKey(Board, on_delete=models.CASCADE)
    reply_file = models.FileField(upload_to = 'files/reply/%Y/%m/%d', null = True)

    def __str__(self):
        return self.reply_info

class Attend(models.Model):
    att_lect = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    att_stud = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.att_lect)


class Report(models.Model):
    report_tittle = models.CharField(max_length = 20)
    report_info = models.CharField(max_length = 500)
    report_file = models.FileField(upload_to = 'files/%Y/%m/%d', null = True)
    report_endline = models.DateField()
    report_lec = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.report_tittle

class ReplyR(models.Model):
    reply_info = models.CharField(max_length = 500)
    reply_writer = models.CharField(max_length = 200)
    reply_prof = models.ForeignKey(Professor, on_delete=models.CASCADE, null = True)
    reply_stud = models.ForeignKey(Student, on_delete=models.CASCADE, null = True)
    reply_report = models.ForeignKey(Report, on_delete=models.CASCADE)
    reply_file = models.FileField(upload_to = 'files/reply/%Y/%m/%d', null = True)

    def __str__(self):
        return self.reply_info


class Report_Stud(models.Model):
    report_writer = models.CharField(max_length = 20)
    report_tittle = models.CharField(max_length = 20)
    report_info = models.CharField(max_length = 500)
    report_stud = models.ForeignKey(Student, on_delete=models.CASCADE)
    report_report = models.ForeignKey(Report, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to = 'files/report/%Y/%m/%d', null = True)

    def __str__(self):
        return self.report_info

