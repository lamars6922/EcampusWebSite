# EcampusWebSite

![11](https://user-images.githubusercontent.com/57030114/69805460-07f76d80-1224-11ea-9f99-119a9ee7e15d.png)
![22](https://user-images.githubusercontent.com/57030114/69805470-0b8af480-1224-11ea-8c91-41f2dfe0956d.png)
![33](https://user-images.githubusercontent.com/57030114/69805477-0ded4e80-1224-11ea-97e5-3430236f3ced.png)
----
# 참여 인원 : 2명
# 역할 : 기능 구현, 테스트, 결합
----
# 개발 목적
* (팀 프로젝트)학습을 목적으로 Django 프레임워크를 이용하여 교수 강의 지원 웹사이트 개발

# 개발 목표

-사용자 관리
  * 웹사이트 사용자는 관리자, 교수, 학생으로 나누어 관리한다. 관리자는 한 명이며 웹사이트가 처음 만들어질 때 같이 만들어진다.  관리자의 id는 admin 이며   초기 비밀 번호는 admin으로 한다.  학생은 웹사이트를 이용하기 위해서는 먼저 가입을 해야 하며 가입시 제공하는 정보는 이름, id, 학번, 비밀번호 이다.   id는 이메일로 한다. 
  * 교수 역시 웹사이트를 이용하기 위해서는 먼저 가입을 해야 하며 가입시 제공하는 정보는 이름, id, 직원번호, 비밀번호 이다. id 는 이메일로 한다. 
  * 가입된 사용자(관리자, 교수, 학생)가 웹사이트를 이용하기 위해서는 먼저 로그인을 해야 한다.  로그인후 일정 시간이 지나면 로그아웃 되며, 사용자가 명시적으로 로그 아웃 할 수도 있다. 
  * id를 제외한 사용자의 정보 (비밀번호 포함)는 변경이 가능하다.

-강의 관리 (관리자, 교수)
 * 새로운 강의를 위한 게시판을 생성하거나, 기존 강의의 삭제, 강의 내용 변경을 하는 기능이다. 
 * 새로운 강의를 생성할 때는 강의명, 년도, 학기, 강의 개요를 입력한다.  

-강의 게시판
 * 게시물을 올리거나 변경, 삭제, 댓글을 올릴 수 있는 기능이다. 교수, 관리자는 게시물과 댓글을 올릴 수 있다.  게시물을 올릴 때는 제목, 내용, 파일 업로드가 가능하다.  이때 파일은 한번에 2개 이상 올릴 수 있다.   댓글을 올릴 때도 제목, 내용, 파일업로드가 가능하다.  이때 역시 파일을 2개 이상 올릴 수 있다. 
 * 교수는 자신이 생성한 강의 게시판에만 권한이 있다.
 * 학생은 댓글만 올릴 수 있다. 
 
-기타
 * 과제 생성 및 제출 기능이 있을 수 있다. 
 * 출석부 기능이 있을 수 있다

# 개발 환경
* 개발 툴 : VS Code
* 개발 언어 : Python
* 플랫폼 : Web Server
* 프레임워크 : Django

# 개발한 기능
* 로그인/로그아웃
* 회원가입
* 개인정보변경
* 강의실 관련 기능
* 게시판 관련 기능
* 과제 관련 기능
* 출석부 기능
