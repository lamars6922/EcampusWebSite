from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse
from django.db import connection
from .forms import *
from .models import *
# Create your views here.

class Login(View):
    template_name = 'supporter/Login.html'

    def get(self, request, *args, **kwargs):
        request.session['LoginProf'] = False #여기 변경
        try:
            admin = Professor.objects.get(pk = 1)
            print("관리자 있음")
        except:
            print("관리자 없음 새로만들기 시작")
            new_admin = Professor(prof_id = "admin@admin.admin", prof_num = 0000, prof_name = "관리자", prof_password = "admin", prof_Phone = "000")
            new_admin.save()

        return render(request, self.template_name)

class LoginProf(View):
    form_class = LoginForm
    template_name = 'supporter/LoginProf.html'

    def get(self, request, *args, **kwargs):
        request.session['LoginProf'] = False #여기 변경
        form = LoginForm(request.GET)

        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        memb_form = Membership(request.POST)
        form = LoginForm(request.GET)
        if memb_form.is_valid():
            new_id = memb_form.cleaned_data['id_text']
            new_pw = memb_form.cleaned_data['pw_text']
            new_num = memb_form.cleaned_data['number_text']
            new_name = memb_form.cleaned_data['name_text']
            new_phone = memb_form.cleaned_data['phone_text']

            new_user = Professor(prof_id = new_id, prof_password = new_pw, prof_num = new_num, prof_name = new_name, prof_Phone = new_phone)
            new_user.save()

        return render(request, self.template_name, {'form':form})

class LoginStud(View):
    form_class = LoginForm
    template_name = 'supporter/LoginStud.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.GET)
        request.session['LoginStud'] = False #여기 변경

        return render(request, self.template_name, {'form':form})

    def post(self, request, *args, **kwargs):
        form = Membership(request.POST)
        retForm = LoginForm(request.GET)
        if form.is_valid():
            new_id = form.cleaned_data['id_text']
            new_pw = form.cleaned_data['pw_text']
            new_num = form.cleaned_data['number_text']
            new_name = form.cleaned_data['name_text']
            new_phone = form.cleaned_data['phone_text']

            new_user = Student(stud_id = new_id, stud_password = new_pw, stud_num = new_num, stud_name = new_name, stud_Phone = new_phone)
            new_user.save()

        return render(request, self.template_name, {'form':retForm})

def Check(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['id_text']
            user_pw = form.cleaned_data['pw_text']
            try:
                user = Professor.objects.get(prof_id = user_id, prof_password = user_pw)
            except Professor.DoesNotExist:
                raise Http404("Professor does not exist!!!!")
            request.session['LoginProf'] = True #여기 변경
            request.session.set_expiry(600) # 여기 변경
            return HttpResponseRedirect(reverse('supporter:ProfUser', args=(user.id,)))
    
def Check2(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['id_text']
            user_pw = form.cleaned_data['pw_text']
            try:
                user = Student.objects.get(stud_id = user_id, stud_password = user_pw)
            except Student.DoesNotExist:
                raise Http404("Student does not exist!!!!")
            request.session['LoginStud'] = True #여기 변경
            request.session.set_expiry(600) # 여기 변경

            return HttpResponseRedirect(reverse('supporter:StudUser', args=(user.id,)))

def Check3(request):
    if request.method == 'POST':
        form = AdminForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['id_text']
            user_pw = form.cleaned_data['pw_text']
            if user_id == user_pw and user_pw == "admin":
                request.session['LoginProf'] = True #여기 변경
                request.session.set_expiry(600) # 여기 변경
                try:
                    user = Professor.objects.get(pk = 1, prof_password = user_pw)
                except Professor.DoesNotExist:
                    raise Http404("Professor does not exist!!!!")
                
            else:
                raise Http404("Admin Login Fail!!!")


            return HttpResponseRedirect(reverse('supporter:ProfUser', args=(user.id,)))
    
class LoginAdmin(View):
    form_class = AdminForm
    template_name = 'supporter/LoginAdmin.html'

    def get(self, request, *args, **kwargs):
        request.session['LoginProf'] = False #여기 변경
        form = AdminForm(request.GET)

        return render(request, self.template_name, {'form':form})


class StudUser(View):
    template_name = 'supporter/StudUserMain.html'
    
    def get(self, request, *args, **kwargs):
        user_id = kwargs['student_id']
        user = Student.objects.get(id = user_id)

        addList = Attend.objects.all().filter(att_stud = user_id)

        return render(request, self.template_name, {'user':user, 'addList':addList})


class ProfUser(View):
    template_name = 'supporter/ProfUserMain.html'
    
    def get(self, request, *args, **kwargs):
        
        user_id = kwargs['professor_id']
        user = Professor.objects.get(id = user_id)
        if user_id != 1:
            lectList = Lecture.objects.all().filter(lec_prof = user_id)
        else:
            lectList = Lecture.objects.all()

        return render(request, self.template_name, {'user':user, 'lectList' : lectList})

    def post(self, request, *args, **kwargs):
        user_id = kwargs['professor_id']
        user = Professor.objects.get(pk = user_id)
        form = LectureForm(request.POST)        
        if form.is_valid():
            new_lecName = form.cleaned_data['lec_name']
            new_lecYear = form.cleaned_data['lec_year']
            new_lecSeme = form.cleaned_data['lec_seme']
            new_lecInfo = form.cleaned_data['lec_info']
            new_lecProf = form.cleaned_data['Professor_id']
            new_lecture = Lecture(lec_name = new_lecName, lec_year = new_lecYear, lec_seme = new_lecSeme, lec_info = new_lecInfo, lec_prof = Professor.objects.get(pk = user_id))
            new_lecture.save()
            lectList = Lecture.objects.all().filter(lec_prof = user_id)
            return render(request, self.template_name, {'user':user, 'lectList':lectList})

class ProfUserinfo(View):
    template_name = 'supporter/BeforeProfInfo.html'
    
    def get(self, request, *args, **kwargs):
        if not request.session.get('LoginProf', False): # 여기 변경
            return render(request, 'supporter/Login.html') # 여기 변경
        else:
            user_id = kwargs['professor_id']
            user = Professor.objects.get(id = user_id)
            form = Join(initial={'number_text':user.prof_num, 'name_text':user.prof_name, 'phone_text':user.prof_Phone})

            return render(request, self.template_name, {'user': user ,'form': form})
    
    def post(self, request, *args, **kwargs):
        form = Join(request.POST)
        if form.is_valid():
            user_pw = form.cleaned_data['pw_text']
            user_num = form.cleaned_data['number_text']
            user_name = form.cleaned_data['name_text']
            user_phone = form.cleaned_data['phone_text']

            user_id = kwargs['professor_id']
            user = Professor.objects.get(id = user_id)
            user.prof_password = str(user_pw)
            user.prof_num = str(user_num)
            user.prof_name = str(user_name)
            user.prof_Phone = str(user_phone)
            user.save()
            
            return render(request, 'supporter/AfterProfInfo.html', {'form' : form})

class StudUserinfo(View):
    template_name = 'supporter/BeforeStudInfo.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('LoginStud', False): # 여기 변경
            return render(request, 'supporter/Login.html') # 여기 변경
        else:
            user_id = kwargs['student_id']
            user = Student.objects.get(id = user_id)
            form = Join(initial={'number_text':user.stud_num, 'name_text':user.stud_name, 'phone_text':user.stud_Phone})

        return render(request, self.template_name, {'user': user ,'form': form})

    def post(self, request, *args, **kwargs):
        form = Join(request.POST)
        if form.is_valid():
            user_pw = form.cleaned_data['pw_text']
            user_num = form.cleaned_data['number_text']
            user_name = form.cleaned_data['name_text']
            user_phone = form.cleaned_data['phone_text']

            user_id = kwargs['student_id']
            user = Student.objects.get(id = user_id)
            user.stud_password = str(user_pw)
            user.stud_num = str(user_num)
            user.stud_name = str(user_name)
            user.stud_Phone = str(user_phone)
            user.save()
            
            return render(request, 'supporter/AfterStudInfo.html', {'form' : form})

class LecList(View):
    template_name = 'supporter/Lecturelist.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['student_id']
        lectList = Lecture.objects.all()

        return render(request, self.template_name, {'lectList' : lectList, 'user_id':user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs['student_id']
        lectList = Lecture.objects.all()

        return render(request, self.template_name, {'lectList' : lectList, 'user_id':user_id})

class StudApplication(View):
    template_name = 'supporter/Studrequest.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['student_id']
        lect_id = kwargs['lecture_id']
        lect = Lecture.objects.get(id = lect_id)

        return render(request, self.template_name, {'lect': lect, 'user_id':user_id})

class LecCheck(View):

    def post(self, request, *args, **kwargs):
        user_id = kwargs['student_id']
        lect_id = kwargs['lecture_id']

        attmember = Attend.objects.create(att_lect=Lecture.objects.get(id = lect_id), att_stud=Student.objects.get(id = user_id))
        attmember.save()
        return HttpResponseRedirect(reverse('supporter:StudUser', args=(user_id,)))


class ProfMemb(View):
    form_class = Membership
    template_name = 'supporter/ProfMemb.html'

    def get(self, request, *args, **kwargs):
        form = Membership(request.GET)

        return render(request, self.template_name, {'form':form})

class StudMemb(View):
    form_calss = Membership
    template_name = 'supporter/StudMemb.html'

    def get(self, request, *args, **kwargs):
        form = Membership(request.GET)

        return render(request, self.template_name, {'form': form})

class AddLecP(View):
    form_class = LectureForm
    template_name = 'supporter/ProfAddLecture.html'

    def post(self, request, *args, **kwargs):
        if not request.session.get('LoginProf', False): # 여기 변경
            return render(request, 'supporter/Login.html') # 여기 변경
        else:
            user_id = kwargs['professor_id']
            user = Professor.objects.get(pk = user_id)
            form = LectureForm(request.POST)
            form = LectureForm(initial={'Professor_id':user_id})

            return render(request, self.template_name, {'form':form, 'user':user})

class LecInfo(View):
    form_class = LectureForm
    template_name = 'supporter/Lecture.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('LoginProf', False): # 여기 변경
            return render(request, 'supporter/Login.html') # 여기 변경
        else:
            form = LectureForm(request.GET)
            user_id = kwargs['professor_id']
            lect_id = kwargs['lecture_id']
            user = Professor.objects.get(id = user_id)
            lect = Lecture.objects.get(id = lect_id)

            return render(request, self.template_name, {'form':form, 'user': user,'lect': lect})

    def post(self, request, *args, **kwargs):
        form = LecJoin(request.POST)
        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)

        if form.is_valid():
            lect_name = form.cleaned_data['lec_name']
            lect_info = form.cleaned_data['lec_info']

            lect.lec_name = str(lect_name)
            lect.lec_info = str(lect_info)
            lect.save()

            return render(request, self.template_name, {'form':form, 'user': user, 'lect' : lect})

class ProflectureChange(View):
    template_name = 'supporter/ChangeLecture.html'
    
    def get(self, request, *args, **kwargs):
        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        form = LectureForm(initial={'Professor_id':user_id, 'lec_name':lect.lec_name, 'lec_year':lect.lec_year, 'lec_seme':lect.lec_seme, 'lec_info':lect.lec_info})
        
        return render(request, self.template_name, {'form': form, 'user': user, 'lect' : lect})

def dele(request, professor_id, lecture_id):
    if request.method == 'POST':
        delLec = Lecture.objects.get(id = lecture_id)
        delLec.delete()
    return HttpResponseRedirect(reverse('supporter:ProfUser', args=(professor_id,)))

def BoardDel(request, professor_id, lecture_id, board_id):
    if request.method == 'POST':
        delBoard = Board.objects.get(id = board_id)
        delBoard.delete()
    return HttpResponseRedirect(reverse('supporter:BoardList', args=(professor_id,lecture_id,)))

def ReportDel(request, professor_id, lecture_id, report_id):
    if request.method == 'POST':
        delReport = Report.objects.get(id = report_id)
        delReport.delete()
    return HttpResponseRedirect(reverse('supporter:ReportList', args=(professor_id,lecture_id,)))

def ReplyDel(request, professor_id, lecture_id, board_id, reply_id):
    if request.method == 'POST':
        delReply = Reply.objects.get(id = reply_id)
        delReply.delete()
    return HttpResponseRedirect(reverse('supporter:BoardInfo', args=(professor_id,lecture_id,board_id,)))

def RepoReplyDel(request, professor_id, lecture_id, report_id, reply_id):
    if request.method == 'POST':
        delReply = ReplyR.objects.get(id = reply_id)
        delReply.delete()
    return HttpResponseRedirect(reverse('supporter:ReportInfo', args=(professor_id,lecture_id,report_id,)))


class AddBoard(View):
    form_class = BoardForm
    template_name = 'supporter/ProfAddBoard.html'

    def get(self, request, *args, **kwargs):
        form = BoardForm(request.GET)

        lect_id = kwargs['lecture_id']
        form = BoardForm(initial={'lecture_id':lect_id})
        user_id = kwargs['professor_id']

        return render(request, self.template_name, {'form':form, 'user_id':user_id, 'lect_id':lect_id})

class BoardList(View):
    form_class = BoardForm
    template_name = 'supporter/ProfBoardList.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        boardList = Board.objects.all().filter(board_lec = lect_id)
    
        return render(request, self.template_name, {'user':user, 'lect':lect, 'boardList': boardList})

    def post(self, request, *args, **kwargs):
        form = BoardForm(request.POST, request.FILES)
        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        if form.is_valid():
            board_tittle = form.cleaned_data['board_tittle']
            board_info = form.cleaned_data['board_info']
            try:
                board_file = request.FILES['board_file']
            except:
                board_file = "파일없음"

            board = Board(board_tittle = board_tittle, board_info = board_info, board_file = board_file, board_lec = Lecture.objects.get(pk = lect_id))
            board.save()
    
        boardList = Board.objects.all().filter(board_lec = lect_id)
        return render(request, self.template_name, {'user':user, 'lect':lect, 'boardList': boardList})

class BoardInfo(View):
    template_name = 'supporter/Board.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        board_id = kwargs['board_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        board = Board.objects.get(id = board_id)
        replyList = Reply.objects.all().filter(reply_board = board_id)
        form = ReplyForm(initial={'reply_prof':user_id, 'reply_board':board_id})

        return render(request, self.template_name, {'user':user, 'lect':lect, 'board':board, 'form':form, 'replyList':replyList})

    def post(self, request, *args, **kwargs):
        form = BoardForm(request.POST, request.FILES)
        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        board_id = kwargs['board_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        board = Board.objects.get(id = board_id)
        
        if form.is_valid():
            board_tittle = form.cleaned_data['board_tittle']
            board_info = form.cleaned_data['board_info']
            try:
                board_file = request.FILES['board_file']
            except:
                board_file = "파일없음"

            board.board_tittle = str(board_tittle)
            board.board_info = str(board_info)
            board.board_file = board_file
            board.save()

            return HttpResponseRedirect(reverse('supporter:BoardList', args=(user_id,lect_id,)))
            

class ProfBoardChange(View):
    template_name = 'supporter/ChangeBoard.html'
    
    def get(self, request, *args, **kwargs):
        form = BoardForm(request.GET)

        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        board_id = kwargs['board_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        board = Board.objects.get(id = board_id)

        form = BoardForm(initial={'lecture_id':lect_id, 'board_tittle':board.board_tittle, 'board_info':board.board_info})

        return render(request, self.template_name, {'form': form, 'user': user, 'lect' : lect, 'board':board})
'''    
def AddReply(request, professor_id, lecture_id, board_id):
    if request.method == 'POST':
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            Professor.objects.get(pk = professor_id)
            reply_info = form.cleaned_data['reply_info']
            try:
                reply_file = request.FILES['reply_file']
            except:
                reply_file = "파일없음"
            
            reply = Reply(reply_info = reply_info, reply_prof = , reply_board = Board.objects.get(pk = board_id), reply_file = reply_file)
            reply.save()
            print("reply save complete!")
    return HttpResponseRedirect(reverse('supporter:BoardInfo', args=(professor_id,lecture_id,board_id,)))
'''
def AddReplyStud(request, student_id, lecture_id, board_id):
    if request.method == 'POST':
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            user = Student.objects.get(pk = student_id)
            reply_info = form.cleaned_data['reply_info']
            try:
                reply_file = request.FILES['reply_file']
            except:
                reply_file = "파일없음"
            
            reply = Reply(reply_info = reply_info, reply_writer = user.stud_name, reply_stud = user, reply_board = Board.objects.get(pk = board_id), reply_file = reply_file)
            reply.save()
            print("reply save complete!")
    
    return HttpResponseRedirect(reverse('supporter:BoardInfoStud', args=(student_id,lecture_id,board_id,)))

    
class ReportList(View):
    form_class = ReportForm
    template_name = 'supporter/ProfReportList.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        reportList = Report.objects.all().filter(report_lec = lect_id)
    
        return render(request, self.template_name, {'user':user, 'lect':lect, 'reportList': reportList})

    def post(self, request, *args, **kwargs):
        form = ReportForm(request.POST, request.FILES)
        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        if form.is_valid():
            report_tittle = form.cleaned_data['report_tittle']
            report_info = form.cleaned_data['report_info']
            report_endline = form.cleaned_data['report_endline']
            try:
                report_file = request.FILES['report_file']
            except:
                report_file = "파일없음"

            report = Report(report_tittle = report_tittle, report_info = report_info, report_endline = report_endline, report_file = report_file, report_lec = Lecture.objects.get(pk = lect_id))
            report.save()
    
        reportList = Report.objects.all().filter(report_lec = lect_id)
        return render(request, self.template_name, {'user':user, 'lect':lect, 'reportList': reportList})

class AddReport(View):
    form_class = ReportForm
    template_name = 'supporter/ProfAddReport.html'

    def get(self, request, *args, **kwargs):
        form = ReportForm(request.GET)

        lect_id = kwargs['lecture_id']
        form = ReportForm(initial={'lecture_id':lect_id})
        user_id = kwargs['professor_id']

        return render(request, self.template_name, {'form':form, 'user_id':user_id, 'lect_id':lect_id})

class ReportInfo(View):    
    template_name = 'supporter/Report.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        report_id = kwargs['report_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        report = Report.objects.get(id = report_id)
        replyList = ReplyR.objects.all().filter(reply_report = report_id)
        form = ReplyRForm(initial={'reply_prof':user_id, 'reply_report':report_id, 'reply_writer':user.prof_name})

        
        report_studList = Report_Stud.objects.all().filter(report_report = report_id)


        return render(request, self.template_name, {'user':user, 'lect':lect, 'report':report, 'form':form, 'replyList':replyList, 'report_studList':report_studList})

    def post(self, request, *args, **kwargs):
        form = ReportForm(request.POST, request.FILES)
        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        report_id = kwargs['report_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        report = Report.objects.get(id = report_id)
        
        if form.is_valid():
            report_tittle = form.cleaned_data['report_tittle']
            report_info = form.cleaned_data['report_info']
            report_endline = form.cleaned_data['report_endline']
            try:
                report_file = request.FILES['report_file']
            except:
               report_file = "파일없음"

            report.report_tittle = str(report_tittle)
            report.report_info = str(report_info)
            report.report_endline = str(report_endline)
            report.report_file = report_file
            report.save()

            return HttpResponseRedirect(reverse('supporter:ReportList', args=(user_id,lect_id,)))

class ProfReportChange(View):
    template_name = 'supporter/ChangeReport.html'
    
    def get(self, request, *args, **kwargs):
        form = ReportForm(request.GET)

        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        report_id = kwargs['report_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        report = Report.objects.get(id = report_id)

        form = ReportForm(initial={'lecture_id':lect_id, 'report_tittle':report.report_tittle, 'report_info':report.report_info, 'report_endline':report.report_endline})

        return render(request, self.template_name, {'form': form, 'user': user, 'lect' : lect, 'report':report})
    
def AddReply(request, professor_id, lecture_id, board_id):
    if request.method == 'POST':
        form = ReplyForm(request.POST, request.FILES)
        if form.is_valid():
            reply_info = form.cleaned_data['reply_info']
            user = Professor.objects.get(pk = professor_id)
            try:
                reply_file = request.FILES['reply_file']
            except:
                reply_file = "파일없음"
            
            reply = Reply(reply_info = reply_info, reply_writer = user.prof_name, reply_prof = user, reply_board = Board.objects.get(pk = board_id), reply_file = reply_file)
            reply.save()
            print("reply save complete!")
    
    return HttpResponseRedirect(reverse('supporter:BoardInfo', args=(professor_id,lecture_id,board_id,)))


def AddRepoReply(request, professor_id, lecture_id, report_id):
    if request.method == 'POST':
        form = ReplyRForm(request.POST, request.FILES)
        if form.is_valid():
            reply_info = form.cleaned_data['reply_info']
            user = Professor.objects.get(pk = professor_id)
            try:
                reply_file = request.FILES['reply_file']
            except:
                reply_file = "파일없음"
            
            reply = ReplyR(reply_info = reply_info, reply_writer = user.prof_name, reply_prof = user, reply_report = Report.objects.get(pk = report_id), reply_file = reply_file)
            reply.save()
    
    return HttpResponseRedirect(reverse('supporter:ReportInfo', args=(professor_id,lecture_id,report_id,)))

def AddRepoReplyStud(request, student_id, lecture_id, report_id):
    if request.method == 'POST':
        form = ReplyRForm(request.POST, request.FILES)
        if form.is_valid():
            reply_info = form.cleaned_data['reply_info']
            user = Student.objects.get(pk = student_id)
            try:
                reply_file = request.FILES['reply_file']
            except:
                reply_file = "파일없음"
            
            reply = ReplyR(reply_info = reply_info, reply_writer = user.stud_name, reply_stud = user, reply_report = Report.objects.get(pk = report_id), reply_file = reply_file)
            reply.save()
    
    return HttpResponseRedirect(reverse('supporter:ReportInfoStud', args=(student_id,lecture_id,report_id,)))

def RepoReplyStudDel(request, student_id, lecture_id, report_id, reply_id):
    if request.method == 'POST':
        delReply = ReplyR.objects.get(id = reply_id)
        delReply.delete()
    return HttpResponseRedirect(reverse('supporter:ReportInfoStud', args=(student_id,lecture_id,report_id,)))

def ReplyStudDel(request, student_id, lecture_id, board_id, reply_id):
    if request.method == 'POST':
        delReply = Reply.objects.get(id = reply_id)
        delReply.delete()
    return HttpResponseRedirect(reverse('supporter:BoardInfoStud', args=(student_id,lecture_id,board_id,)))


def Report_StudDel(request, student_id, lecture_id, report_id):
    if request.method == 'POST':
        delReport = Report_Stud.objects.get(report_stud = student_id)
        delReport.delete()
    return HttpResponseRedirect(reverse('supporter:ReportInfoStud', args=(student_id,lecture_id,report_id,)))


class StudLecInfo(View):
    form_class = LectureForm
    template_name = 'supporter/LectureStud.html'

    def get(self, request, *args, **kwargs):
        if not request.session.get('LoginStud', False): # 여기 변경
            return render(request, 'supporter/Login.html') # 여기 변경
        else:
            form = LectureForm(request.GET)
            user_id = kwargs['student_id']
            lect_id = kwargs['lecture_id']
            user = Student.objects.get(id = user_id)
            lect = Lecture.objects.get(id = lect_id)

        return render(request, self.template_name, {'form':form, 'user': user,'lect': lect})

class BoardListStud(View):
    form_class = BoardForm
    template_name = 'supporter/StudBoardList.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['student_id']
        lect_id = kwargs['lecture_id']
        user = Student.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        boardList = Board.objects.all().filter(board_lec = lect_id)
    
        return render(request, self.template_name, {'user':user, 'lect':lect, 'boardList': boardList})


class BoardInfoStud(View):
    template_name = 'supporter/BoardStud.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['student_id']
        lect_id = kwargs['lecture_id']
        board_id = kwargs['board_id']
        user = Student.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        board = Board.objects.get(id = board_id)
        replyList = Reply.objects.all().filter(reply_board = board_id)
        form = ReplyForm(initial={'reply_stud':user_id, 'reply_board':board_id, 'reply_writer':user.stud_name})

        return render(request, self.template_name, {'user':user, 'lect':lect, 'board':board, 'form':form, 'replyList':replyList})


class ReportListStud(View):
    form_class = ReportForm
    template_name = 'supporter/StudReportList.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['student_id']
        lect_id = kwargs['lecture_id']
        user = Student.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        reportList = Report.objects.all().filter(report_lec = lect_id)
    
        return render(request, self.template_name, {'user':user, 'lect':lect, 'reportList': reportList})


class ReportInfoStud(View):    
    template_name = 'supporter/ReportStud.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['student_id']
        lect_id = kwargs['lecture_id']
        report_id = kwargs['report_id']
        user = Student.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        report = Report.objects.get(id = report_id)
        replyList = ReplyR.objects.all().filter(reply_report = report_id)
        try:
            report_stud = Report_Stud.objects.get(report_stud = user_id)
            print(report_stud)
        except:
            report_stud = "제출안함"
        form = ReplyRForm(initial={'reply_stud':user_id, 'reply_report':report_id, 'reply_writer':user.stud_name})

        return render(request, self.template_name, {'user':user, 'lect':lect, 'report':report, 'form':form, 'report_stud':report_stud, 'replyList':replyList})

class ReportManagStud(View):
    template_name = 'supporter/ReportManagementStud.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['student_id']
        lect_id = kwargs['lecture_id']
        report_id = kwargs['report_id']
        user = Student.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        report = Report.objects.get(id = report_id)
        form = Report_StudForm(initial={'report_stud':user_id, 'report_report':report_id, 'report_writer':user.stud_name})

        return render(request, self.template_name, {'user':user, 'lect':lect, 'report':report, 'form':form})

    def post(self, request, *args, **kwargs):
        form = Report_StudForm(request.POST, request.FILES)
        user_id = kwargs['student_id']
        lect_id = kwargs['lecture_id']
        report_id = kwargs['report_id']
        user = Student.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        report = Report.objects.get(id = report_id)
        
        if form.is_valid():
            report_writer = form.cleaned_data['report_writer']
            report_tittle = form.cleaned_data['report_tittle']
            report_info = form.cleaned_data['report_info']
            report_report = form.cleaned_data['report_report']
            report_stud = form.cleaned_data['report_stud']

            try:
                report_file = request.FILES['report_file']
            except:
                report_file = "파일없음"

            new_report = Report_Stud(report_writer = user.stud_name, report_tittle = report_tittle, report_info = report_info, report_report = Report.objects.get(id=report_id), report_stud = Student.objects.get(id=user_id), report_file = report_file)
            new_report.save()
            print("리포트 제출 완료")

            return HttpResponseRedirect(reverse('supporter:ReportInfoStud', args=(user_id,lect_id,report_id,)))


class AttendBook(View):
    template_name = 'supporter/AttendBook.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs['professor_id']
        lect_id = kwargs['lecture_id']
        user = Professor.objects.get(id = user_id)
        lect = Lecture.objects.get(id = lect_id)
        attendList = Attend.objects.all().filter(att_lect = lect_id)
        stud_num = len(attendList)
        return render(request, self.template_name, {'user':user, 'lect':lect, 'attendList':attendList})
