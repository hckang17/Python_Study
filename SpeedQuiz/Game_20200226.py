import pygame
import sys
import random, time
import os.path
from pygame import mixer

pygame.init()
mixer.init()


# 게임 내부 실행시 필요한 함수 #

def StartGame_Intro(self):      #main_0의 버튼을 눌렀을때 실행되는 함수 -> 게임화면으로 이동함
    self.bgm.stop()                 #이때 self 인자는 main_0 을 의미함. (클래스 자신을 인자로 넘겨준 함수)
    main()

def StartGame():                    #main_2의 버튼을 눌렀을때 실행되는 함수 -> 다시 게임화면으로 돌아감
    main_3()
    """임시로 건들여놓음 main_1로 수정바람"""

def GotoMain():                    #main_2의 버튼을 눌렀을때 실행되는 함수 -> 다시 게임화면으로 돌아감
    main_0()

def QuestionReset(score):       # 문제판을 초기화 하는 함수
    num = MakeProblem(score)
    return num
    
def Time(nowTime, finishTime):      # 남은시간 나타내는 함수
    remainTime = finishTime - nowTime
    remainTime = round(remainTime, 2)
    return remainTime

class MakeProblem():                    #문제에 사용할 무작위 정수를 고르는 클래스
    def __init__(self, score):
        self.num1 = MakeProblem.choice_num(score)
        self.num2 = MakeProblem.choice_num(score)
        print(self.num1*self.num2)

    def choice_num(score):  # num1, num2에 점수에 따라 무작위의 숫자를 할당해주는 함수
        if(score < 150):
            return random.randint(2, 9)
        elif(score >= 150 and score <300):
            return random.randint(2, 15)
        elif(score >= 300 and score <500):
            return random.randint(5, 19)
        elif(score >= 500 and score <600):
            return random.randint(5, 24)
        elif(score >= 600 and score <1000):
            return random.randint(5, 29)
        elif(score >= 1000 and score < 2000):
            return random.randint(9, 39)
        elif(score >= 2000 and score < 4000):
            return random.randint(2, 69)
        else:
            return random.randint(2, 99)
    
def GameOver(self):         ## 게임오버 함수. 모든 브금을 멈추고 main_2를 부르기 위한 준비를 한다.
    self.bgm.stop()
    self.out_bgm.play()

    pygame.display.update()
    self.screen.blit(self.result_background, (0,0))
    self.screen.blit(self.gameover_sign, (0, 175))
    pygame.display.update()

    pygame.time.delay(5000)
    self.finish_bgm.play()
    main_2(self.score)    ## 화면전환


def Scoring(self, OX):  #점수를 더하거나 뺀다.       #self 인자는 main클래스의 __init__(self)의 self임.
    if(OX == "CORRECT"):
        if(self.score < 200):
            self.score += (10 + random.randint(2,5))
            if(random.random() < 0.05):
                self.score += 8
                return True
            return False
        elif(self.score >= 200 and self.score < 400):
            self.score += (15 + random.randint(2, 8))
            if(random.random() < 0.08):
                self.score += 12
                return True
            return False
        elif(self.score >= 400 and self.score < 800):
            self.score += (23 + random.randint(2, 12))
            if(random.random() < 0.1):
                self.score += 20
                return True
            else:
                return False
        elif(self.score >= 800 and self.score < 2000):
            self.score += (30 + random.randint(2,16))
            if(random.random() < 0.2):
                self.score += 45
                return True
            else:
                return False
        elif(self.score >= 2000):
            self.score += (50 + random.randint(2, 39))
            if(random.random() < 0.25):
                self.score += 55
                return True
            return False
        else:
            self.score += (60 + random.randint(8, 39))
            if(random.random() < 0.30):
                self.score += 60
                return True
            return False
    elif(OX == "WRONG"):
        if(self.score <= 150):
            self.score = int(self.score / 3 * 2)
        elif(self.score > 150 and self.score <= 400):
            self.score = int(self.score / 4 * 3)
        elif(self.score > 400 and self.score <= 1000):
            self.score = int(self.score / 5 * 4)
        elif(self.score > 1000 and self.score <= 2500):
            self.score = int(self.score / 6 * 5)
        else:
            self.score = self.score / 7 * 6
        
def Correct_Answer(self):       #사용자가 입력한 정답이 맞을때, #self.역시 main클래스의 __init__의 self임.
    self.finishTime += 2.45
    if(Scoring(self, "CORRECT")):
        sign = self.correct_sign_bonus
        pygame.mixer.Sound("Resources\\SOUND\\treasurebox_bonus.wav").play()
    else:
        sign = self.correct_sign
    self.correct_wav.play()
    eraseTime = round(time.time(), 1) + 0.45
    while(round(time.time(), 1) < eraseTime):
        self.screen.blit(sign, (200,100))
        pygame.display.update()
    self.Question = QuestionReset(self.score)
    
def Incorrect_Answer(self):     #사용자가 입력한 답안이 틀렸을 때. #self.역시 main클래스의 __init__의 self임.
    Scoring(self, "WRONG")
    if(self.finishTime - self.nowTime < 6.55):
        GameOver(self)
    else:
        self.finishTime -= 6.55
        eraseTime = round(time.time(), 1) + 0.45
        self.incorrect_wav.play()
        while(round(time.time(), 1) < eraseTime):
            self.screen.blit(self.incorrect_sign, (200,100))
            pygame.display.update()

'''게임 내 버튼 클래스'''

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, images ,func = None, effect = None):    #effect 매개변수는 func의 매개변수가 됩니다.
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.Surface([width, height])
        self.rect = self.surface.get_rect()
        self.width, self.height = width, height ######### 넓이랑 높이를 부여함.
        self.rect.x = x
        self.rect.y = y
        self.image = images
        self.now_image = self.image[0]
        self.func = func 
        self.argument = effect
        self.button_click_sound = pygame.mixer.Sound("Resources\\SOUND\\button_click.wav")

    def isOver(self, pos):  # 마우스가 해당 객체위에 올라가있을때 발생하는 이벤트
        if self.rect.x < pos[0] < self.rect.x+self.width:
            if self.rect.y < pos[1] <self.rect.y+self.height:
                self.now_image = self.image[1] # 
                return True
        self.now_image = self.image[0]  
        return False

    def isClick(self,pos):  # 마우스가 해당 객체를 클릭했을때 발생하는 이벤트
        if self.rect.x < pos[0] < self.rect.x+self.width:
            if self.rect.y < pos[1] < self.rect.y+self.height:
                self.button_click_sound.play()
                if (not self.argument):     #매개변수가 없으면!
                    self.func()
                else:                               #매개변수가 있으면!
                    self.func(self.argument)
                return True
        self.now_image = self.image[0]
        return False


'''문자열 입력을 위한 클래스 모음'''


class InputNum: # 사용자가 입력한 숫자를 띄우기 위한 기본 작업 (폰트, 위치 등등 설정)
    def __init__(self, getNum = None, inputNumberCount = 0):
        self.count = inputNumberCount
        self.inputNum = PresentNum(self.count, x = 318, y = 480, content = str(getNum),\
                                   fontSize = 40, nextNumLocation = 25)
        
    def NumInGame(self): # pygame 화면에 숫자 띄우기
        textSurfNumber, textRectNumber = self.inputNum.showNum()
        return (textSurfNumber, textRectNumber)

    def moveToNext(self): #33
        self.inputNum.moveNum() # 숫자 입력 칸 이동 (x좌표)

class PresentNum:
    def __init__(self, count = 0, x = 0, y = 0, width = 100, height = 80, content = None\
                 , textColor = (0, 0, 0), fontSize = 55, nextNumLocation = 0): # BLACK = (0, 0, 0)
        self.surface = pygame.Surface([width, height]) # 배경
        self.content = content # 내용
        self.textColor = textColor # 글자색
        self.xCoor = x # x좌표
        self.yCoor = y # y좌표
        self.fontSize = fontSize # 글자 크기
        self.nextNumLocation = nextNumLocation # 다음 글자가 이동할 자리 (x좌표)
        self.count = count # 입력된 숫자 개수 (이 개수에 의해 다음 숫자의 입력될 위치를 설정)

    def moveNum(self):
        self.xCoor += (self.nextNumLocation * self.count) #글자 이동(x좌표)
        
    def showNum(self): # 입력한 숫자 보여주기 위한 준비 단계 (폰트 설정, 위치 설정)
        fontObj = pygame.font.Font('210 긴생머리R.ttf', self.fontSize)
        textSurfaceObj = fontObj.render(self.content, True, self.textColor)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (self.xCoor, self.yCoor)
        return (textSurfaceObj, textRectObj) #출력할 오브젝트, 출력할 내용을 넘겨주게 됨.


'''게임 실행 클래스 부분'''

class main():       ## 본게임(게임플레이 신)
    def __init__(self):
# 기본 초기화 #
        self.font = pygame.font.Font('210 긴생머리R.ttf', 32)
        self.font_num = pygame.font.Font('210 긴생머리R.ttf', 90)       #문제판에 찍을 숫자 폰트 크기
        self.font_op = pygame.font.Font('210 긴생머리R.ttf', 80)        #문제판에 찍을 연산자 폰트 크기
        self.screen = pygame.display.set_mode((800,600))
        self.nowTime = round(time.time(), 2)    #게임 시작한 시간 처음 지정
        self.finishTime = self.nowTime + 30       #게임 끝날 시간
        pygame.display.set_caption("SPEED QUIZ!!")
        self.FPS = 33   # 초당 프레임(FPS 33)으로 설정하고 .03초 
        self.score = 0 # 최종점수 0점으로 설정
#임의 변수
        inputtedNum = '(이곳에 정답을 입력하세요)' # 입력된 숫자 초기화
        inputNumberCount = 0 # 사용자가 입력한 숫자 개수 세기
        user_input = '' # 사용자가 입력한 답안지
        temp_input = '' # 사용자가 입력한 답안지를 옮긴 임시 답안지 (실제 답과 비교하기 위한 부분)
        userAnswer = [] #InputNum 클래스에 대한 객체가 들어가는 리스트
        
        #기본 리소스#
        self.background = pygame.image.load("Resources\\GameScreen.png")
        self.result_background = pygame.image.load("Resources\\background.png")
        self.clock = pygame.time.Clock()
        self.bgm = pygame.mixer.Sound('Resources\\SOUND\\speedquiz.wav')
        self.correct_wav = pygame.mixer.Sound('Resources\\SOUND\\correct_answer.wav')
        self.incorrect_wav = pygame.mixer.Sound('Resources\\SOUND\\incorrect_answer.wav')
        self.gameover_bgm = pygame.mixer.Sound('Resources\\SOUND\\bgm-timeout.wav')
        self.out_bgm = pygame.mixer.Sound('Resources\\SOUND\\bgm-timeout.wav')
        self.finish_bgm = pygame.mixer.Sound('Resources\\SOUND\\bgm-end.wav')
        
        self.correct_sign = pygame.image.load("Resources\\Correct_Answer.png")
        self.correct_sign_bonus = pygame.image.load("Resources\\Correct_Answer_bonus.png")
        self.incorrect_sign = pygame.image.load("Resources\\Incorrect_Answer.png")
        self.gameover_sign = pygame.image.load("Resources\\GameOver.png")

        self.bgm.play(-1)       #브금 실행
        self.Question = QuestionReset(self.score)     #첫번째 문제 출제        

        
        
        while True:
            #갱신부분               #시간, 점수
            self.nowTime = round(time.time(), 2)
            if(Time(self.nowTime, self.finishTime) < 10):
                timeText = self.font.render(str(Time(self.nowTime, self.finishTime)), True, ((255-(255/10)*int(\
                    Time(self.nowTime, self.finishTime))), 0, 0))
            else:
                timeText = self.font.render(str(Time(self.nowTime, self.finishTime)), True, (0,0,0))
                
            if(self.score <= 1000):         #점수 구간별 색상 변화
                scoreText = self.font.render("{}".format(self.score), True, (0,0,0))
            elif(self.score <= 4000):
                scoreText = self.font.render("{}".format(self.score), True, (255,0,0))
            else:
                scoreText = self.font.render("{}".format(self.score), True, (0, 0, 255))
            

            #갱신부분               #문제 숫자들 연산자들
            num_1 = self.font_num.render(str(self.Question.num1), True, (0,0,0))
            num_2 = self.font_num.render(str(self.Question.num2), True, (0,0,0))
            operator = self.font_op.render("X", True, (0,0,0))
            
            #스크린 출력부분
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(timeText, (520, 40))
            self.screen.blit(scoreText, (220, 40))
            self.screen.blit(num_1, (150, 200))
            self.screen.blit(num_2, (400, 200))
            self.screen.blit(operator, (290, 210))

############### main루프 안 이벤트 판단 ###################

            if(self.nowTime >= self.finishTime):
                GameOver(self)
                pygame.display.update()
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                try:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE: # 백스페이스 구현
                            if (inputNumberCount == 0):
                                continue
                            else:
                                inputNumberCount -= 1
                                user_input = user_input[:-1] # 이전에 클릭했던 숫자가 입력되기 전의 문자열을 반환
                                userAnswer.remove(userAnswer[inputNumberCount]) # 이전에 클릭했던 숫자에 해당하는 객체 삭제 (블릿 불가능)
                                print(user_input)
                        
                        elif event.key == pygame.K_t:
                            Correct_Answer(self)

                        elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER: # Enter 입력키
                            if (len(userAnswer) != 0):
                                userAnswer.clear()
                                temp_input = user_input
                                user_input = ''
                                inputNumberCount = 0
                                print(temp_input)
                            if (temp_input == ''):
                                continue
                            if (int(temp_input) == (self.Question.num1 * self.Question.num2)):      ##정답
                                Correct_Answer(self)
                            else:
                                Incorrect_Answer(self)

                        if (inputNumberCount > 4): # 입력한 숫자 5개를 초과하면 더 이상 입력되지 않도록 함
                            continue
                        
                        elif event.key == pygame.K_0 or event.key == pygame.K_KP0: # 0 입력키
                            inputNumberCount += 1 # 입력한 숫자 개수 세기
                            user_input += '0' # 정답 문자열
                            inputtedNum = 0 # InputNum 클라스에 입력된 숫자가 0임을 알려주는 기능을 하는 변수
                            userAnswer.append(InputNum(inputtedNum, inputNumberCount)) # 리스트에 InputNum에 해당하는 객체 생성 & 추가
                            userAnswer[inputNumberCount -1].moveToNext() # 숫자가 추가됨에 따라 x좌표 이동
                
                        elif event.key == pygame.K_1 or event.key == pygame.K_KP1: # 1 입력키
                            inputNumberCount += 1
                            user_input += '1'
                            inputtedNum = 1
                            userAnswer.append(InputNum(inputtedNum, inputNumberCount))
                            userAnswer[inputNumberCount -1].moveToNext()
                        
                        elif event.key == pygame.K_2 or event.key == pygame.K_KP2: # 2 입력키
                            inputNumberCount += 1
                            user_input += '2'
                            inputtedNum = 2
                            userAnswer.append(InputNum(inputtedNum, inputNumberCount))
                            userAnswer[inputNumberCount -1].moveToNext()
                        
                        elif event.key == pygame.K_3 or event.key == pygame.K_KP3: # 3 입력키
                            inputNumberCount += 1
                            user_input += '3'
                            inputtedNum = 3
                            userAnswer.append(InputNum(inputtedNum, inputNumberCount))
                            userAnswer[inputNumberCount -1].moveToNext()
                        
                        elif event.key == pygame.K_4 or event.key == pygame.K_KP4: # 4 입력키
                            inputNumberCount += 1
                            user_input += '4'
                            inputtedNum = 4
                            userAnswer.append(InputNum(inputtedNum, inputNumberCount))
                            userAnswer[inputNumberCount -1].moveToNext()
                
                        elif event.key == pygame.K_5 or event.key == pygame.K_KP5: # 5 입력키
                            inputNumberCount += 1
                            user_input += '5'
                            inputtedNum = 5
                            userAnswer.append(InputNum(inputtedNum, inputNumberCount))
                            userAnswer[inputNumberCount -1].moveToNext()
                    
                        elif event.key == pygame.K_6 or event.key == pygame.K_KP6: # 6 입력키
                            inputNumberCount += 1
                            user_input += '6'
                            inputtedNum = 6
                            userAnswer.append(InputNum(inputtedNum, inputNumberCount))
                            userAnswer[inputNumberCount -1].moveToNext()
                
                        elif event.key == pygame.K_7 or event.key == pygame.K_KP7: # 7 입력키
                            inputNumberCount += 1
                            user_input += '7'
                            inputtedNum = 7
                            userAnswer.append(InputNum(inputtedNum, inputNumberCount))
                            userAnswer[inputNumberCount -1].moveToNext()
                        
                        elif event.key == pygame.K_8 or event.key == pygame.K_KP8: # 8 입력키
                            inputNumberCount += 1
                            user_input += '8'
                            inputtedNum = 8
                            userAnswer.append(InputNum(inputtedNum, inputNumberCount))
                            userAnswer[inputNumberCount -1].moveToNext()
                
                        elif event.key == pygame.K_9 or event.key == pygame.K_KP9: # 9 입력키
                            inputNumberCount += 1
                            user_input += '9'
                            inputtedNum = 9
                            userAnswer.append(InputNum(inputtedNum, inputNumberCount))
                            userAnswer[inputNumberCount -1].moveToNext()

                except SyntaxError: # 다른 키보드의 기능을 눌렀을 때 아무런 예외가 발생하지 않도록 처리
                    break
        
            for i in userAnswer: # 리스트에 있는 블릿하는 객체들 실행하여 지금까지 입력된 모든 숫자가 블릿되도록 반복문 설정
                temp = i.NumInGame()
                self.screen.blit(temp[0], temp[1])
        
            inputtedNum = None # 사용자로부터 입력된 숫자 없애기(초기화)
            self.clock.tick(self.FPS)
            pygame.display.update() #화면업데이트


############################################################################################################


class main_0():     #Intro화면
    def __init__(self):
        self.screen = pygame.display.set_mode((800,600))
        pygame.display.set_caption("SPEED QUIZ")
        self.background = pygame.image.load("Resources\\Intro.png")
        self.start_button_normal = pygame.image.load("Resources\\Startbutton_normal.png")
        self.start_button_isclick = pygame.image.load("Resources\\Startbutton_mouseover.png")
        self.start_button_image = [self.start_button_normal, self.start_button_isclick]
        self.start_button = Button(225, 425, 360, 100, self.start_button_image, StartGame_Intro, self)
        self.bgm = pygame.mixer.Sound("Resources\\SOUND\\WaitRoom.wav")
        self.bgm.play(-1)
        
        while True:     #게임화면
            self.screen.blit(self.background, (0,0))
            self.screen.blit(self.start_button.now_image, (225, 425))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    self.start_button.isOver(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_button.isClick(pygame.mouse.get_pos())
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

class main_2():     #게임종료 화면(Result) 
    def __init__(self, final_score):    # 생성자
        pygame.time.delay(3000)
        self.final_score = final_score
        self.screen = pygame.display.set_mode((800,600))
        self.font_num = pygame.font.Font('210 긴생머리R.ttf', 70)       #문제판에 찍을 숫자 폰트 크기
        self.score_font = self.font_num.render(str(self.final_score), True, (0,0,0))
        self.result_background = pygame.image.load("Resources\\Result_background.png")
        self.start_button_normal = pygame.image.load("Resources\\Startbutton_normal.png")
        self.start_button_isclick = pygame.image.load("Resources\\Startbutton_mouseover.png")
        self.start_button_image = [self.start_button_normal, self.start_button_isclick]
        self.start_button = Button(225, 425, 360, 100, self.start_button_image, StartGame)
        
        self.UPLOAD_RESULT()

        while True:     #두번째 메인루프
            self.screen.blit(self.result_background, (0,0))
            self.screen.blit(self.start_button.now_image, (225, 425))
            self.screen.blit(self.score_font, (435, 255))

            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    self.start_button.isOver(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.start_button.isClick(pygame.mouse.get_pos())
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
    
    def UPLOAD_RESULT(self):
        temp_list = []
        result_data = open("data\\ranking.txt", "r")
        #우선 랭킹 읽어오기(라인순서대로)
        for line in result_data:
            line = line.strip()
            temp_list.append(int(line))
        temp_list.append(self.final_score)
        result_data.close()
        result_data = open("data\\ranking.txt", "w")
        #데이터 입력하기
        for score in temp_list:
            result_data.write(str(score)+"\n")
        result_data.close()
        
class main_3():     #랭킹창 구현
    def __init__(self):
        self.temp_list = self.sorting_score()
        self.screen = pygame.display.set_mode((800,600))
        self.font_num = pygame.font.Font('NanumGothic.ttf', 37)       #랭킹창에 찍을 숫자 폰트 크기
        # 1위부터 찍힐 위치 = (250, 150)
        self.background = pygame.image.load("Resources\\Result_ranking.png")
        self.to_main_button_image = [pygame.image.load("Resources\\GotoMain_Button.png"), \
            pygame.image.load("Resources\\GotoMain_Button.png")]
        self.to_main_button = Button(325, 540, 150, 40, self.to_main_button_image, GotoMain)

        while True:     #두번째 메인루프
            self.screen.blit(self.background, (0,0))
            self.screen.blit(self.to_main_button_image[0], (325, 540))
            self.blit_result_score()

            for event in pygame.event.get():
                if event.type == pygame.MOUSEMOTION:
                    self.to_main_button.isOver(pygame.mouse.get_pos())
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.to_main_button.isClick(pygame.mouse.get_pos())
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()
    
    def blit_result_score(self):
        y_list = 145
        for score in self.temp_list:
            if 150 + (37 * 9) < y_list:
                break
            score_font = self.font_num.render(str(score) + " pts", True, (0,0,0))
            self.screen.blit(score_font, (255, y_list))
            y_list = y_list + 37

    def sorting_score(self):    # 점수를 읽어서 내림차순으로 정리해줌
        result_data = open("data\\ranking.txt", "r")
        temp_list = []
        for line in result_data:
            line.strip()
            temp_list.append(int(line))
        temp_list.sort(reverse=True)
        return temp_list

##########################################클래스및 함수 선언 완료#####

main_0()            #인트로 화면 열기
    
