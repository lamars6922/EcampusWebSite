from django import forms
from django.db import models
from .models import Professor
import datetime
class LoginForm(forms.Form):
    id_text = forms.EmailField(label = "아이디(Email)<br>",
    widget=forms.TextInput(attrs={'size':20, 'placeholder': 'ex) ~@naver.com'}))
    pw_text = forms.CharField(label = "비밀번호<br>", max_length = 15, 
    widget=forms.PasswordInput)

class AdminForm(forms.Form):
    id_text = forms.CharField(label = "아이디<br>", max_length = 15)
    pw_text = forms.CharField(label = "비밀번호<br>", max_length = 15, 
    widget=forms.PasswordInput)

class Membership(forms.Form):
    id_text = forms.EmailField(label = "아이디(Email)<br>",
    widget=forms.TextInput(attrs={'size':20, 'placeholder': 'ex) ~@naver.com'}))
    pw_text = forms.CharField(label = "비밀번호<br>", max_length = 15, 
    widget=forms.PasswordInput)
    pw_text2 = forms.CharField(label = "비밀번호 재확인<br>", max_length = 15, 
    widget=forms.PasswordInput)
    number_text = forms.CharField(label = "교수번호(학번)<br>", max_length=7, 
    widget=forms.TextInput(attrs={'size':20}))
    name_text = forms.CharField(label = "이름<br>", max_length=10, 
    widget=forms.TextInput(attrs={'size':20}))
    phone_text = forms.CharField(label = "전화번호<br>", max_length=10, 
    widget=forms.TextInput(attrs={'size':20}))

class Join(forms.Form):
    pw_text = forms.CharField(label = "비밀번호<br>", max_length = 15, 
    widget=forms.PasswordInput)
    pw_text2 = forms.CharField(label = "비밀번호 재확인<br>", max_length = 15, 
    widget=forms.PasswordInput)
    number_text = forms.CharField(label = "교수번호(학번)<br>", max_length=7, 
    widget=forms.TextInput(attrs={'size':20}))
    name_text = forms.CharField(label = "이름<br>", max_length=10, 
    widget=forms.TextInput(attrs={'size':20}))
    phone_text = forms.CharField(label = "전화번호<br>", max_length=10, 
    widget=forms.TextInput(attrs={'size':20}))

class LecJoin(forms.Form):
    lec_name = forms.CharField(label = "강의명변경", max_length=200, 
    widget=forms.TextInput(attrs={'size':20}))
    lec_info = forms.CharField(label = "강의소개변경", max_length=200, 
    widget=forms.Textarea)
    
class LectureForm(forms.Form):
    lec_name = forms.CharField(max_length=20, label = "강의 이름<br>")
    lec_year = forms.CharField(max_length = 4, label = "강의 년도<br>")
    lec_seme = forms.CharField(max_length = 1, label = "강의 학기<br>")
    lec_info = forms.CharField(max_length=500, label = "강의 내용<br>", widget=forms.Textarea)
    Professor_id = forms.IntegerField(label = "작성자 코드(관리자님이신 경우 해당 교수님의 pk값을 입력해주세요!)<br>", )

    
class BoardForm(forms.Form):
    board_tittle = forms.CharField(max_length=20, label = "게시글 제목<br>")
    board_info = forms.CharField(max_length=500, label = "게시글 내용<br>", widget=forms.Textarea)
    board_file = forms.FileField(label = "첨부 파일<br>", required = False)
    lecture_id = forms.IntegerField(label = "강의 코드<br>")

class ReplyForm(forms.Form):
    reply_info = forms.CharField(max_length = 500, label = "내용<br>", widget=forms.Textarea)
    reply_board = forms.IntegerField(label = "게시판<br>")
    reply_prof = forms.IntegerField(label = "작성자P<br>", required = False)
    reply_stud = forms.IntegerField(label = "작성자S<br>", required = False)
    reply_writer = forms.CharField(max_length = 20, required = False)
    reply_file = forms.FileField(label = "첨부 파일<br>",  required = False)

class ReportForm(forms.Form):
    report_endline = forms.DateField(label = "제출기한(yyyy-mm-dd)<br>", initial=datetime.date.today)
    report_tittle = forms.CharField(max_length=20, label = "과제 제목<br>")
    report_info = forms.CharField(max_length=500, label = "과제 내용<br>", widget=forms.Textarea)
    report_file = forms.FileField(label = "과제 첨부 파일<br>", required = False)
    lecture_id = forms.IntegerField(label = "강의 코드<br>")

class ReplyRForm(forms.Form):
    reply_info = forms.CharField(max_length = 500, label = "내용<br>", widget=forms.Textarea)
    reply_report = forms.IntegerField(label = "과제<br>")
    reply_prof = forms.IntegerField(label = "작성자P<br>", required = False)
    reply_stud = forms.IntegerField(label = "작성자S<br>", required = False)
    reply_writer = forms.CharField(max_length = 20, required = False)
    reply_file = forms.FileField(label = "과제 파일<br>",  required = False)


class Report_StudForm(forms.Form):
    report_tittle = forms.CharField(max_length = 20, label = "제목<br>")
    report_writer = forms.CharField(max_length = 20, label = "작성자<br>")
    report_info = forms.CharField(max_length = 500, label = "내용<br>", widget=forms.Textarea)
    report_report = forms.IntegerField(label = "과제<br>")
    report_stud = forms.IntegerField(label = "작성자S<br>")
    report_file = forms.FileField(label = "과제 파일<br>",  required = False)