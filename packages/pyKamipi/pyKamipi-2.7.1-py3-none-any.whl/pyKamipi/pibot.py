# -*-coding:utf-8-*-
import sys
import serial
import time
import math
from termcolor import cprint

# 명령타입
class CommandType:
    FORCE_STOP = 0x01
    MOVE_FORWARD_BLOCK = 0x02
    MOVE_BACKWARD_BLOCK = 0x03
    TURN_LEFT_BLOCK = 0x04
    TURN_RIGHT_BLOCK = 0x05
    TURN_BACK_BLOCK = 0x06
    MOVE_FORWARD_LINE = 0x07
    TURN_LEFT_LINE = 0x08
    TURN_RIGHT_LINE = 0x09
    TURN_BACK_LINE = 0x0A
    SET_MOVE_SPEED = 0x0B
    MOVE_FORWARD_SPEED = 0x0C
    MOVE_LEFT_SPEED = 0x0D
    MOVE_RIGHT_SPEED = 0x0E
    MOVE_BACKWARD_SPEED = 0x10
    MOVE_FORWARD_LRSPEED = 0x11
    MOVE_BACKWARD_LRSPEED = 0x12
    MOVE_UNIT = 0x13
    SPIN_DEGREE = 0x14
    WHEEL_SET_SPEED = 0x15
    WHEEL_RUN = 0x16
    WHEEL_RUN_UNIT = 0x17
    WHEEL_RUN_LRUNIT = 0x18
    TOPMOTOR_SET_SPEED = 0x19
    TOPMOTOR_TURN = 0x1A
    TOPMOTOR_TURN_UNIT = 0x1B
    TOPMOTOR_MOVE_ABSOLUTE = 0x1C
    TOPMOTOR_STOP = 0x1D
    LED_TURN = 0x1E
    DRAW_SHAPE = 0x20
    DRAW_CIRCLE = 0x21
    DRAW_SEMICIRCLE = 0x22
    DRAW_SEMICIRCEL_UNIT = 0x23
    MELODY_BEEP = 0x24
    MELODY_MUTE = 0x25
    MELODY_SET_BMP = 0x26
    MELODY_PLAY_FREQ = 0x27
    SENSOR_GET_COLOR = 0x28
    SENSOR_GET_OBJECT = 0x29
    SENSOR_GET_LINE = 0x2A
    TOGGLE_LINERRACER = 0x2B
    BOTPI_STOP = 0x2C
    BOTPI_EMERGENCY_STOP = 0x2D
    BOTPI_INITIALIZE = 0x2E
    BOTPI_RESET = 0x30
    BOTPI_CLEAR = 0x31


# 명령패킷의 인덱스
class PacketIndex:
    START = 0
    LENGTH = 1
    HWID = 2
    HWTYPE = 3
    COMMANDTYPE = 4
    MODETYPE = 5
    MODECOMMAND = 6
    DATA0 = 7
    DATA1 = 8
    DATA2 = 9
    DATA3 = 10
    DATA4 = 11
    DATA5 = 12
    DATA6 = 13
    INDEX = 14
    DATA7 = 15
    DATA8 = 16
    DATA9 = 17
    DATA10 = 18
    END = 19


# 리턴 패킷의 인덱스
class RETURN_PACKET:
    START = 0
    LENGTH = 1
    HWID = 2
    HWTYPE = 3
    CMDTYPE = 4
    MODE = 5
    RESULT = 6
    BATTERY = 7
    LEFT_OBJECT = 8
    RIGHT_OBJECT = 9
    LEFT_LINE = 10
    CENTER_LINE = 11
    RIGHT_LINE = 12
    COLOR = 13
    INDEX = 14
    DATA0 = 15
    DATA1 = 16
    DATA2 = 17
    DATA3 = 18
    END = 19


class ModeType:
    MAPBOARD = 0x01
    CONTROL = 0x02
    RGB = 0x3
    TOP_STEPPER = 0x04
    OBJECT_DETECTER = 0x05
    LINE_DETECTOR = 0x06
    COLOR_DETECTOR = 0x7
    BATTERY = 0x08
    VERSION = 0x9
    REALTIME = 0x0A
    DRAWSHAPE = 0x0B
    PRECISION_CTR = 0x0C
    MELODY = 0x0D
    LINEMAP = 0x0E
    RESET = 0x0F
    EMERGENCY_STOP = 0x11
    LINE = 0x12
    INITIALIZE = 0x22
    MOTOR_SPEED = 0x33


# Command Type
COMMANDTYPE_WRITE = 0x01
COMMANDTYPE_READ = 0x02
COMMANDTYPE_RETURN = 0x03

# 디바이스 타입
HWTYPE_BOTPI = 0x00
HWTYPE_XBLOCK = 0x10

# LED 색상 YELLOW
TEST_COMMAND = [
    0x41, 0x14, 0x01, 0x01, 0x01,
    0x03, 0x00, 0xff, 0xff, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x5a,
]

NULL_COMMAND_PACKET = [
    0x41, 0x14, 0x01, HWTYPE_BOTPI, COMMANDTYPE_WRITE,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x5a,
]

DEFAULT_MOTOR_SPEED = 0x96      # 150


LED = {
    "off": [0, 0, 0],
    "red": [255, 0, 0],
    "orange": [255, 165, 0],
    "yellow": [255, 255, 0],
    "green": [0, 255, 0],
    "blue": [0, 0, 255],
    "skyblue": [0, 255, 255],
    "purple": [139, 0, 255],
    "white": [255, 255, 255],
}

LED_COLOR = [
    LED["off"], LED["red"], LED["orange"], LED["yellow"], LED["green"],
    LED["blue"], LED["skyblue"], LED["purple"], LED["white"]
]


class LedColor:
    OFF = LED["off"]
    RED = LED["red"]
    ORANGE = LED["orange"]
    YELLOW = LED["yellow"]
    GREEN = LED["green"]
    BLUE = LED["blue"]
    SKYBLUE = LED["skyblue"]
    PURPLE = LED["purple"]
    WHITE = LED["white"]


class KamibotPi:

    def __init__(self, port=None, baud=57600, timeout=2, verbose=False):
        self.__verbose = verbose
        self.__cmdIndex = 1     # 순차적으로 증가

        self.__mode = None
        self.__battery = None
        self.__left_object = None
        self.__right_object = None
        self.__left_line = None
        self.__center_line = None
        self.__right_line = None
        self.__port = port
        self.__baud = baud
        self.__color = None
        self.__index = None     # 리턴받은 명령의 인덱스
        self.__data0 = None
        self.__data1 = None
        self.__data2 = None
        self.__data3 = None
        self.__time = time.time()

        try:
            if self.__verbose:
                print("\nPython Version %s" % sys.version)

            if not port:
                raise ValueError("Could not find port.")

            cprint(f'👽 KamibotPi Connect PORT={self.__port}, BAUD={self.__baud}', "green")
            sr = serial.Serial(port, baud, timeout=timeout)
            sr.flush()
            self.sr = sr
        except Exception as e:
            cprint(f'👽 Error(KamibotPi): {e}', 'green')
            sys.exit()
        # except KeyboardInterrupt:
        #     if self.__verbose:
        #         print("Program Aborted Before Kamibot Instantiated")
        #     sys.exit()

    def __get_idx(self):
        self.__cmdIndex = self.__cmdIndex + 1
        if self.__cmdIndex > 255:
            self.__cmdIndex = 1
        return self.__cmdIndex

    def close(self):
        '''close후 exit()함수를 호출함 
        '''
        try:
            if self.sr and self.sr.is_open:
                self.sr.flush()
                self.sr.close()
                cprint(f'🔥 Close (KamibotPi) {self.__port}', 'red')
        except Exception as e:
            cprint(f'Error(KamibotPi): {e}', 'red')
        finally:
            sys.exit(0)


    def disconnect(self):
        try:
            if self.sr and self.sr.is_open:
                self.sr.flush()
                self.sr.close()
                cprint(f'🔥 Disconnect(KamibotPi) {self.__port}', 'red')
        except Exception as e:
            cprint(f'Error(KamibotPi): {e}', 'red')


    def __process_return(self):
        data = []
        while len(data) < 20:
            if self.sr.inWaiting():
                c = self.sr.read()
                data.append(ord(c))
            else:
                time.sleep(.001)

        if self.__verbose:
            print('return data length {0}'.format(len(data)))

        if len(data) == 20:
            self.__mode = data[RETURN_PACKET.MODE]
            self.__battery = data[RETURN_PACKET.BATTERY]
            self.__left_object = data[RETURN_PACKET.LEFT_OBJECT]
            self.__right_object = data[RETURN_PACKET.RIGHT_OBJECT]
            self.__left_line = data[RETURN_PACKET.LEFT_LINE]
            self.__center_line = data[RETURN_PACKET.CENTER_LINE]
            self.__right_line = data[RETURN_PACKET.RIGHT_LINE]
            self.__color = data[RETURN_PACKET.COLOR]
            self.__index = data[RETURN_PACKET.INDEX]
            self.__data0 = data[RETURN_PACKET.DATA0]
            self.__data1 = data[RETURN_PACKET.DATA1]
            self.__data2 = data[RETURN_PACKET.DATA2]
            self.__data3 = data[RETURN_PACKET.DATA3]
            self.__time = time.time()

            if self.__verbose:
                print(
                    f"leftObj:{self.__left_object}, rightObj:{self.__right_object}, leftLine:{self.__left_line}, centerLine:{self.__center_line}, rightLine:{self.__right_line}")
                print(f"color:{self.__color}, index:{self.__index}, data0:{self.__data0}, data1:{self.__data1}, data2:{self.__data2}, data3:{self.__data3}, battery:{self.__battery}")
        else:
            print(f'Return data error! size={len(data)}')

    # -------------------------------------------------------------------------------------------------------
    #  BLOCK ACTION
    # -------------------------------------------------------------------------------------------------------
    def delay(self, sec):
        """기다리기

        Args:
            sec (float): 초
        Returns:
            None
        """
        time.sleep(sec)

    def delayms(self, ms):
        time.sleep(ms/1000)


    def wait(self, ms):
        """_summary_

        Args:
            ms (int): 밀리초
        """
        self.delayms(ms)


    def toggle_linetracer(self, mode, speed=100):
        """라인트레이서 기능 켜고 끄기

        Args:
            mode (bool): True 켜기, False 끄기
            speed (int): 라인트레이서 속도
        Returns:
            None
        """
        speed = int(float(speed))
        if mode:
            self.__start_linetracer(speed)
        else:
            self.stop()

    def __start_linetracer(self,  speed):
        if self.__verbose:
            print("\n *__start_linetracer")

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.MODETYPE] = ModeType.LINE
        command[PacketIndex.MODECOMMAND] = 0x01
        command[PacketIndex.DATA0] = speed
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    # ------------------- 라인 맵보드 ------------------------------------------
    def move_forward(self,  value, opt="-l"):
        """앞으로 ( 1 )칸 이동하기

        Args:
            value (int): 이동 칸수
            opt (str) '-l': 라인맵보드  '-b': 블록맵보드
        Returns:
            None
        """
        if self.__verbose:
            print("\n * move_forward")
        command = NULL_COMMAND_PACKET[:]
        # print("command bytes %s" % (''.join('\\x' + format(x, '02x') for x in command)))
        # print('\\x'.join(format(x, '02x') for x in command))
        mode = ModeType.MAPBOARD        # 블록맵보드
        cmd = 0x01
        if opt == "-l":
            mode = ModeType.LINEMAP     # 라인맵보드

        command[PacketIndex.MODETYPE] = mode
        command[PacketIndex.MODECOMMAND] = cmd
        command[PacketIndex.DATA0] = value
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def move_backward(self,  value):
        """뒤로 ( 1 )칸 이동하기
        블록맵보드에서만 동작함. 라인맵보드에서는 동작안함.

        Args:
            value (int): 이동 칸수
        Returns:
            None
        """
        if self.__verbose:
            print("\n * move_backward")

        command = NULL_COMMAND_PACKET[:]
        mode = ModeType.MAPBOARD
        cmd = 0x04

        command[PacketIndex.MODETYPE] = mode
        command[PacketIndex.MODECOMMAND] = cmd
        command[PacketIndex.DATA0] = value
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def turn_left(self,  value=1, opt='-l'):
        """블록: 왼쪽으로 ( 1 ) 돌기
        라인: 왼쪽으로 돌기
        라인맵보드에서는 value값에 상관없이 왼쪽으로 1번 돌기만 실행됨.

        Args:
            value (int): 이동 칸수
            opt (str): '-l': 라인맵보드, '-b':블록맵보드
        Returns:
            None
        """
        if self.__verbose:
            print("\n * turn_left")

        command = NULL_COMMAND_PACKET[:]
        mode = ModeType.MAPBOARD
        cmd = 0x03
        if opt == "-l":
            mode = ModeType.LINEMAP

        command[PacketIndex.MODETYPE] = mode
        command[PacketIndex.MODECOMMAND] = cmd
        command[PacketIndex.DATA0] = value
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def turn_right(self,  value=1, opt='-l'):
        """블록: 오른쪽으로 ( 1 ) 돌기
        라인: 오른쪽으로 돌기
        라인맵보드에서는 value값에 상관없이 오른쪽으로 1번 돌기만 실행됨.

        Args:
            value (int): 이동 칸수
            opt (str): '-l': 라인맵보드, '-b':블록맵보드
        Returns:
            None
        """
        if self.__verbose:
            print("\n * turn_right")

        command = NULL_COMMAND_PACKET[:]
        mode = ModeType.MAPBOARD
        cmd = 0x02
        if opt == "-l":
            mode = ModeType.LINEMAP

        command[PacketIndex.MODETYPE] = mode
        command[PacketIndex.MODECOMMAND] = cmd
        command[PacketIndex.DATA0] = value
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def turn_back(self,  value=1, opt='-l'):
        """블록: 뒤로 ( 1 ) 돌기
        라인: 뒤로 돌기
        라인맵보드에서는 value값에 상관없이 뒤로 1번 돌기만 실행됨.

        Args:
            value (int): 이동 칸수
            opt (str): '-l': 라인맵보드, '-b':블록맵보드
        Returns:
            None
        """
        if self.__verbose:
            print("\n * turn_back")

        command = NULL_COMMAND_PACKET[:]
        mode = ModeType.MAPBOARD
        cmd = 0x05
        if opt == "-l":
            mode = ModeType.LINEMAP
            cmd = 0x04

        command[PacketIndex.MODETYPE] = mode
        command[PacketIndex.MODECOMMAND] = cmd
        command[PacketIndex.DATA0] = value
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    # ----- 콘트롤 모드
    def go_dir_speed(self,  ldir, lspeed, rdir, rspeed):
        """왼쪽, 오른쪽 바퀴의 방향과 속도를 지정해서 동작시킴

        Args:
            ldir (str): 왼쪽 바퀴의 회전 방향 설정 'f':앞으로, 'b': 뒤로
            lspeed (int): 왼쪽 바퀴의 회전 속도
            rdir (str): 오른쪽 바퀴의 회전 방향 설정 'f':앞으로, 'b': 뒤로
            rspeed (int): 오른쪽 바퀴의 회전 속도
        Returns:
            None
        """
        if self.__verbose:
            print("\n * turn_back")

        if ldir.upper().startswith("F"):
            ld = 0x00
        else:
            ld = 0x01

        if rdir.upper().startswith("F"):
            rd = 0x00
        else:
            rd = 0x01

        # command = NULL_COMMAND_PACKET[:]
        # command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        # command[PacketIndex.MODETYPE] = ModeType.CONTROL
        # command[PacketIndex.MODECOMMAND] = 0x00  # 양쪽 모터
        # command[PacketIndex.DATA0] = rd
        # command[PacketIndex.DATA1] = rspeed
        # command[PacketIndex.DATA2] = ld
        # command[PacketIndex.DATA3] = lspeed
        # command[PacketIndex.INDEX] = self.__get_idx()

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.CONTROL
        command[PacketIndex.MODECOMMAND] = 0x00  # 양쪽 모터
        command[PacketIndex.DATA0] = ld
        command[PacketIndex.DATA1] = lspeed

        command[PacketIndex.DATA2] = rd
        command[PacketIndex.DATA3] = rspeed

        command[PacketIndex.INDEX] = self.__get_idx()

        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def go_forward_speed(self,  lspeed, rspeed):
        """왼쩍, 오른쪽 바퀴의 속도를 지정해서 앞으로 이동시킴

        Args:
            lspeed (int): 왼쪽 바퀴의 회전 속도
            rspeed (int): 오른쪽 바퀴의 회전 속도
        Returns:
            None
        """
        if self.__verbose:
            print("\n * go_forward_speed")

        return self.go_dir_speed("f", lspeed, "f", rspeed)

    def go_backward_speed(self,  lspeed, rspeed):
        """왼쪽, 오른쪽 바퀴의 속도를 지정해서 뒤로 이동시킴

        Args:
            lspeed (int): 왼쪽 바퀴의 회전 속도
            rspeed (int): 오른쪽 바퀴의 회전 속도
        Returns:
            None
        """
        if self.__verbose:
            print("\n * go_backward_speed")

        return self.go_dir_speed("b", lspeed, "b", rspeed)

    def go_left_speed(self,  speed):
        """속도를 지정해서 왼쪽으로 회전시킴

        Args:
            speed (int): 회전 속도
        Returns:
            None
        """
        if self.__verbose:
            print("\n * go_left_speed")

        return self.go_dir_speed("f", speed, "f", 0)

    def go_right_speed(self,  speed):
        """속도를 지정해서 오른쪽으로 회전시킴

        Args:
            speed (int): 회전 속도
        Returns:
            None
        """
        if self.__verbose:
            print("\n * go_left_speed")

        return self.go_dir_speed("f", 0, "f", speed)

    def stop(self):
        """이동중인 로봇을 정지시킴

        Args:
            None
        Returns:
            None
        """
        if self.__verbose:
            print("\n * stop")

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.CONTROL
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = 0x02
        command[PacketIndex.DATA2] = 0x02

        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    # 초기화
    def init(self):
        """로봇을 초기화 시킴
        Args:
            None
        Returns:
            None
        """
        if self.__verbose:
            print("\n * init")

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.MODETYPE] = ModeType.INITIALIZE
        command[PacketIndex.MODECOMMAND] = 0x01
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    ### ---------- 정밀제어모드 ------------------------- ###
    def move_step(self,  ldir, lstep, rdir, rstep):
        """왼쪽, 오른쪽 모터의 회전 방향을 지정하고 스텝수 단위로 이동

        Args:
            ldir (int): 왼쪽 바퀴 회전 방향 'f':앞으로 'b':뒤로
            lstep (int): 스텝수
            rdir (int): 오른쪽 바퀴 회전 방향 'f':앞으로 'b':뒤로
            rstep (int): 스텝수

        Returns:
            None
        """
        if self.__verbose:
            print("\n * move_step *")

        if rdir.upper().startswith("F"):
            print('RF')
            rd = 0x01
        else:
            rd = 0x02

        if ldir.upper().startswith("F"):
            print('LF')
            ld = 0x01
        else:
            ld = 0x02

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.PRECISION_CTR
        command[PacketIndex.MODECOMMAND] = 0x11  # 스텝단위

        command[PacketIndex.DATA0] = rd
        command[PacketIndex.DATA1] = rstep & 0x00ff         # LOW BIT
        command[PacketIndex.DATA2] = (rstep >> 8) & 0x00ff  # HIGH BIT
        command[PacketIndex.DATA3] = 100  # 속도
        command[PacketIndex.DATA4] = ld
        command[PacketIndex.DATA5] = lstep & 0x00ff  # LOW BIT
        command[PacketIndex.DATA6] = (lstep >> 8) & 0x00ff  # HIGH BIT
        command[PacketIndex.DATA7] = 100  # 속도
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def move_time(self,  ldir, lsec, rdir, rsec):
        """왼쪽, 오른쪽 모터의 회전 방향을 지정하고 시간을 지정하여 이동

        Args:
            ldir (int): 왼쪽 바퀴 회전 방향 'f':앞으로 'b':뒤로
            lsec (int): 시간 (초)
            rdir (int): 오른쪽 바퀴 회전 방향 'f':앞으로 'b':뒤로
            rsec (int): 시간 (초)

        Returns:
            None
        """
        if self.__verbose:
            print("\n * move_time *")

        if rdir.upper().startswith("F"):
            rd = 0x01
        else:
            rd = 0x02

        if ldir.upper().startswith("F"):
            ld = 0x01
        else:
            ld = 0x02

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.PRECISION_CTR
        command[PacketIndex.MODECOMMAND] = 0x12  # 초단위

        command[PacketIndex.DATA0] = rd
        command[PacketIndex.DATA1] = rsec & 0x00ff         # LOW BIT
        command[PacketIndex.DATA2] = (rsec >> 8) & 0x00ff  # HIGH BIT
        command[PacketIndex.DATA3] = 100  # 속도

        command[PacketIndex.DATA4] = ld
        command[PacketIndex.DATA5] = lsec & 0x00ff  # LOW BIT
        command[PacketIndex.DATA6] = (lsec >> 8) & 0x00ff  # HIGH BIT
        command[PacketIndex.DATA7] = 100  # 속도
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def move_forward_unit(self,  value=10, opt="-l", speed=50):
        """ 앞으로 이동할 단위를 지정하여 동작시킴
        1cm, 1초, 1스텝

        Args:
            value (int): 이동할 값
            opt (str): 옵션 '-l': cm, '-t': sec, '-s': step
            speed (int): 속도

        Returns:
            None
        """
        if self.__verbose:
            print("\n * move_forward_unit *")

        if opt == '-l':
            cmd = 0x01  # 1cm 앞으로
        elif opt == '-t':
            cmd = 0x05   # 1초 앞으로
        elif opt == '-s':
            cmd = 0x0d  # 1스텝 앞으로
        else:
            return None

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.PRECISION_CTR
        command[PacketIndex.MODECOMMAND] = cmd

        command[PacketIndex.DATA0] = value & 0x00ff
        command[PacketIndex.DATA1] = (value >> 8) & 0x00ff
        command[PacketIndex.DATA2] = speed
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def turn_right_speed(self, value=90, speed=50):
        """오른쪽으로 제자리에서 회전

        Args:
            value (int): 회전각
            speed (int): 속도

        Returns:
            None
        """
        # return self.move_right_unit(value, "-l", speed)
        if self.__verbose:
            print("\n * turn_right_speed * ")

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.PRECISION_CTR
        command[PacketIndex.MODECOMMAND] = 0x11

        # 오른쪽 바퀴
        command[PacketIndex.DATA0] = 0x02
        command[PacketIndex.DATA1] = value & 0x00ff
        command[PacketIndex.DATA2] = (value >> 8) & 0x00ff
        command[PacketIndex.DATA3] = speed

        # 왼쪽바퀴
        command[PacketIndex.DATA4] = 0x01
        command[PacketIndex.DATA5] = value & 0x00ff
        command[PacketIndex.DATA6] = (value >> 8) & 0x00ff
        command[PacketIndex.DATA7] = speed

        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def move_right_unit(self, value=10, opt="-l", speed=50):
        """오른쪽으로 이동할 단위를 지정하여 동작시킴
        1cm, 1초, 1스텝

        Args:
            value (int): 이동할 값
            speed (int): 속도
            opt (str): 옵션 '-l': cm, '-t': 초, '-s': 스텝

        Returns:
            None
        """
        if self.__verbose:
            print("\n * go_right_unit *")

        if opt == '-l':
            cmd = 0x02  # 1cm 앞으로
        elif opt == '-t':
            cmd = 0x06   # 1초 앞으로
        elif opt == '-s':
            cmd = 0x0e  # 1스텝 앞으로
        else:
            return None

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.PRECISION_CTR
        command[PacketIndex.MODECOMMAND] = cmd

        command[PacketIndex.DATA0] = value & 0x00ff
        command[PacketIndex.DATA1] = (value >> 8) & 0x00ff
        command[PacketIndex.DATA2] = speed
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def turn_left_speed(self, value=90, speed=50):
        """왼쪽으로 제자리에서 회전

        Args:
            value (int): 회전각
            speed (int): 속도

        Returns:
            None
        """
        # return self.move_left_unit(value, "-l", speed)
        if self.__verbose:
            print("\n * turn_left_speed * ")

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.PRECISION_CTR
        command[PacketIndex.MODECOMMAND] = 0x11

        # 오른쪽 바퀴
        command[PacketIndex.DATA0] = 0x01
        command[PacketIndex.DATA1] = value & 0x00ff
        command[PacketIndex.DATA2] = (value >> 8) & 0x00ff
        command[PacketIndex.DATA3] = speed

        # 왼쪽바퀴
        command[PacketIndex.DATA4] = 0x02
        command[PacketIndex.DATA5] = value & 0x00ff
        command[PacketIndex.DATA6] = (value >> 8) & 0x00ff
        command[PacketIndex.DATA7] = speed

        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def move_left_unit(self, value=10, opt="-l", speed=50):
        """왼쪽으로 이동할 단위를 지정하여 동작시킴
        1cm, 1초, 1스텝

        Args:
            value (int): 이동할 값
            speed (int): 속도
            opt (str): 옵션 '-l': cm, '-t': 초, '-s': 스텝

        Returns:
            None
        """
        if self.__verbose:
            print("\n * go_left_unit * ")

        if opt == '-l':
            cmd = 0x03
        elif opt == '-t':
            cmd = 0x07
        elif opt == '-s':
            cmd = 0x0f
        else:
            return None

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.PRECISION_CTR
        command[PacketIndex.MODECOMMAND] = cmd

        command[PacketIndex.DATA0] = value & 0x00ff
        command[PacketIndex.DATA1] = (value >> 8) & 0x00ff
        command[PacketIndex.DATA2] = speed
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def move_backward_unit(self, value=10, opt="-l", speed=50):
        """뒤로 이동할 단위를 지정하여 동작시킴
        1cm, 1초, 1스텝

        Args:
            value (int): 이동할 값
            speed (int): 속도
            opt (str): 옵션 '-l': cm, '-t': 초, '-s': 스텝

        Returns:
            None
        """
        if self.__verbose:
            print("\n * move_backward_unit * ")

        if opt == '-l':
            cmd = 0x04
        elif opt == '-t':
            cmd = 0x08
        elif opt == '-s':
            cmd = 0x10
        else:
            return None

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.PRECISION_CTR
        command[PacketIndex.MODECOMMAND] = cmd

        command[PacketIndex.DATA0] = value & 0x00ff
        command[PacketIndex.DATA1] = (value >> 8) & 0x00ff
        command[PacketIndex.DATA2] = speed
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def turn_continous(self, dir="l", speed=100):
        """지정된 방향으로 계속 회전하기

        Args:
            dir (str): 회전 방향 'r': 오른쪽으로, 'l':왼쪽으로

        Returns:
            None
        """
        if self.__verbose:
            print("\n * turn_continous * ")

        if dir.upper() == 'L':
            cmd = 0x0c
        else:
            cmd = 0x0b

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.PRECISION_CTR
        command[PacketIndex.MODECOMMAND] = cmd

        command[PacketIndex.DATA0] = 0x00
        command[PacketIndex.DATA1] = 0x00
        command[PacketIndex.DATA2] = speed
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    # ------------------------------LED ------------------------------------------------

    def turn_led_idx(self,  idx):
        """컬러 LED 켜기

        Args:
            idx (int): 0 ~ 7,  0:red, 1:orange, 2:yellow, 3:green, 4:blue , 5:skyblue , 6:purple , 7:white

        Returns:
            None
        """
        self.turn_led(LED_COLOR[idx][0], LED_COLOR[idx][1], LED_COLOR[idx][2])

    def turn_led(self,  rval, gval, bval):
        """컬러 LED 켜기

        Args:
            rval (int): 0 ~ 255 Red 값
            gval (int): 0 ~ 255 Green 값
            bval (int): 0 ~ 255 Blue 값

        Returns:
            None
        """
        if self.__verbose:
            print("\n * turn_led *")

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.RGB
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = rval
        command[PacketIndex.DATA1] = gval
        command[PacketIndex.DATA2] = bval

        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    # -------------------------------TOP 스텝퍼 모드 ----------------------------------------
    def top_motor_degree(self,  dir, value=90, speed=50):
        """탑모터 방향으로 지정해서 주어진 각도만큼 회전시키기

        Args:
            dir (int): 방향 'l': 왼쪽으로, 'r': 오른쪽으로
            value (int): 각도값
            speed (int): 회전 속도

        Returns:
            None
        """
        if self.__verbose:
            print("\n * top_motor_degree *")

        if dir.upper().startswith("L"):
            dir = 0x02
        elif dir.upper().startswith("R"):
            dir = 0x01
        else:
            dir = 0x04  # 멈춤

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.TOP_STEPPER
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = value & 0x00ff
        command[PacketIndex.DATA1] = (value >> 8) & 0x00ff
        command[PacketIndex.DATA2] = dir
        command[PacketIndex.DATA3] = speed
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def top_motor_abspos(self,  degree=0, speed=50):
        """탑모터 절대 각도 위치로 이동시키기

        Args:
            dir (int): 방향 'l': 왼쪽으로, 'r': 오른쪽으로
            degree (int): 각도값
            speed (int): 회전 속도

        Returns:
            None
        """
        if self.__verbose:
            print("\n * top_motor_abspos")

        degree = 65000 if degree > 65000 else degree

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.TOP_STEPPER
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = degree & 0x00ff
        command[PacketIndex.DATA1] = (degree >> 8) & 0x00ff
        command[PacketIndex.DATA2] = 0x03  # 절대각도
        command[PacketIndex.DATA3] = speed
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def top_motor_stop(self):
        """탑모터 회전 정지시키기

        Args:
            None

        Returns:
            None
        """
        if self.__verbose:
            print("\n * top_motor_stop *")

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.TOP_STEPPER
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = 0x00
        command[PacketIndex.DATA1] = 0x00
        command[PacketIndex.DATA2] = 0x04
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def top_motor_time(self, dir, value=3, speed=50):
        """탑모터 방향을 지정해서 정해진 시간마큼 회전시키기

        Args:
            dir (int): 방향 'l': 왼쪽으로, 'r': 오른쪽으로
            value (int): 회전 시간을 초단위로 지정
            speed (int): 회전 속도
        Returns:
            None
        """
        if self.__verbose:
            print("\n * top_motor_time *")

        if dir.upper().startswith("L"):
            dir = 0x02
        elif dir.upper().startswith("R"):
            dir = 0x01
        else:
            dir = 0x04
            value = 0x00
            speed = 0x00

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.TOP_STEPPER
        command[PacketIndex.MODECOMMAND] = 0x01
        command[PacketIndex.DATA0] = value & 0x00ff
        command[PacketIndex.DATA1] = (value >> 8) & 0x00ff
        command[PacketIndex.DATA2] = dir
        command[PacketIndex.DATA3] = speed
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def top_motor_round(self,  dir, value=1, speed=50):
        """탑모터 방향을 지정해서 정해진만큼 회전시키기

        Args:
            dir (int): 방향 'left': 왼쪽으로, 'right': 오른쪽으로
            value (int): 회전수
            speed (int): 회전 속도
        Returns:
            None
        """
        if self.__verbose:
            print("\n * top_motor_time *")

        if dir.upper().startswith("L"):
            dir = 0x02
        elif dir.upper().startswith("R"):
            dir = 0x01
        else:
            dir = 0x04
            value = 0x00
            speed = 0x00

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_WRITE
        command[PacketIndex.MODETYPE] = ModeType.TOP_STEPPER
        command[PacketIndex.MODECOMMAND] = 0x02
        command[PacketIndex.DATA0] = value & 0x00ff
        command[PacketIndex.DATA1] = (value >> 8) & 0x00ff
        command[PacketIndex.DATA2] = dir
        command[PacketIndex.DATA3] = speed
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    # ----------------------------물체 감지 ------------------------------------------------

    def get_object_detect(self,  opt=True):
        """물체 감지 센서를 동작시킨다.

        Args:
            opt (bool): True 센서 동작, False 센서 멈춤

        Returns:
            None
        """
        if self.__verbose:
            print("\n * get_object_detect*")

        if opt:
            cmd = 0x00
        else:
            cmd = 0x01

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_READ
        command[PacketIndex.MODETYPE] = ModeType.OBJECT_DETECTER
        command[PacketIndex.MODECOMMAND] = cmd
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        # print(f"left:{self.__left_object}, right:{self.__right_object}")
        return self.__left_object, self.__right_object

    # -------------------------------라인센서, 라인 검출 모드-----------------------------------

    def get_line_sensor(self,  opt=True):
        """라인감지 센서를 동작시킨다.

        Args:
            opt (bool): True 센서 동작, False 센서 멈춤

        Returns:
            None
        """
        if self.__verbose:
            print("\n * get_line_sensor *")

        if opt:
            cmd = 0x01
        else:
            cmd = 0x00

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_READ
        command[PacketIndex.MODETYPE] = ModeType.LINE_DETECTOR
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = cmd
        command[PacketIndex.DATA1] = cmd
        command[PacketIndex.DATA2] = cmd
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        # 2022-04-08 left와 right의 방향을 바꾼다.
        # return (self.__left_line, self.__center_line, self.__right_line)
        return (self.__right_line, self.__center_line, self.__left_line)

    # -------------------------컬러측정 모드-------------------------------------------------------------
    def get_color_sensor(self,  opt=True):
        """컬러센서를 동작시킨다.

        Args:
            opt (bool): True 센서 동작, False 센서 멈춤

        Returns:
            color (int) : 색상 인덱스 값
        """

        if self.__verbose:
            print("\n * get_color_sensor *")

        if opt:
            cmd = 0x00
        else:
            cmd = 0x01

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_READ
        command[PacketIndex.MODETYPE] = ModeType.COLOR_DETECTOR
        command[PacketIndex.MODECOMMAND] = cmd
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return self.__color

    def get_color_elements(self,  opt=True):
        """컬러센서를 동작시킨다.

        Args:
            opt (bool): True 센서 동작, False 센서 멈춤

        Returns:
            color (r, g, b)
        """

        if self.__verbose:
            print("\n * get_color_sensor *")

        if opt:
            cmd = 0x00
        else:
            cmd = 0x01

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_READ
        command[PacketIndex.MODETYPE] = ModeType.COLOR_DETECTOR
        command[PacketIndex.MODECOMMAND] = cmd
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return (self.__data0, self.__data1, self.__data2)

    # --------------------------------배터리 값---------------------------------------------

    def get_battery(self):
        """배터리값을 구한다

        Args:
           opt (bool): 배터리값 획득 기능 옵션 True: 기능 켬, False: 기능 끔

        Returns:
            배터리값
        """
        if self.__verbose:
            print("\n * get_battery*")

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_READ
        command[PacketIndex.MODETYPE] = ModeType.BATTERY
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return self.__battery

    # ---------------------------------버전 정보 -----------------------------------------------------
    def get_version(self):
        """펌웨어 버전 획득 

        Args:
           opt (bool): 펌웨어 버전 획득 기능 옵션 True: 기능 켬, False: 기능 끔 

        Returns:
            버전      
        """
        if self.__verbose:
            print("\n * get_version*")

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.COMMANDTYPE] = COMMANDTYPE_READ
        command[PacketIndex.MODETYPE] = ModeType.VERSION
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    # ---------------------------------도형 모드 --------------------------------------------
    def draw_tri(self, len):
        """삼각형 그리기

        Args:
           len (int): 삼각형 한변의 길이 cm

        Returns:
            None      
        """
        self.__draw_shape(0x01, len)

    def draw_rect(self, len):
        """사각형 그리기

        Args:
           len (int): 사각형 한변의 길이 cm

        Returns:
            None      
        """
        self.__draw_shape(0x02, len)

    def draw_penta(self, len):
        """오각형 그리기

        Args:
           len (int): 오각형 한변의 길이 cm

        Returns:
            None      
        """
        self.__draw_shape(0x03, len)

    def draw_hexa(self, len):
        """육각형 그리기

        Args:
           len (int): 육각형 한변의 길이 cm

        Returns:
            None
        """
        self.__draw_shape(0x04, len)

    def draw_star(self, len):
        """별모양 그리기

        Args:
           len (int): 별모양 한변의 길이 cm

        Returns:
            None      
        """
        self.__draw_shape(0x06, len)

    def draw_circle(self, len):
        """원 그리기

        Args:
           len (int): 원의 반지름

        Returns:
            None      
        """
        self.__draw_shape(0x07, len)

    def draw_semicircle(self, len, side="l"):
        """반원 그리기

        Args:
           len (int): 원의 반지름
           side (str): "l":왼쪽, "r":오른쪽
        Returns:
            None      
        """
        if side.upper().startswith("L"):
            cmd = 0x02
        else:
            cmd = 0x01
        self.__draw_shape(0x08, len, cmd)

    def draw_arc(self, radius, value=1, mode=0):
        """주어진 시간만큼 원호 그리기

        Args:
           radius (int): 원의 반지름
           value (int): mode == 0? 시간 (초) : 각도 
           mode (int) : 0 이면 시간, 1이면 각도 
        Returns:
            None      
        """
        # self.__draw_shape(0x0a, len, time & 0x00ff, (time >> 8) & 0x00ff)
        cmd = 0x0a if mode == 0 else 0x09;
        self.__draw_shape(cmd, radius, value & 0x00ff, (value >> 8) & 0x00ff)

    def __draw_shape(self,  cmd, len, val1=0, val2=0):
        if self.__verbose:
            print("\n * go_lrspeed_unit")

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.MODETYPE] = ModeType.DRAWSHAPE
        command[PacketIndex.MODECOMMAND] = cmd
        command[PacketIndex.DATA0] = len
        command[PacketIndex.DATA1] = val1
        command[PacketIndex.DATA2] = val2
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    # -----------------------------------멜로디 모드 ----------------------------------------

    def melody(self,  scale=45, sec=1):
        """소리내기 

        Args:
            scale (int): 음계 (0 ~ 83)
            sec (int): 시간 (초)
        Returns:
            None      
        """
        if self.__verbose:
            print("\n * melody *")

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.MODETYPE] = ModeType.MELODY
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = scale
        command[PacketIndex.DATA1] = int(sec * 10)
        command[PacketIndex.DATA2] = 0x00
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def beep(self):
        """삐 소리내기 

        Args:
            None

        Returns:
            None      
        """
        if self.__verbose:
            print("\n * go_lrspeed_unit")

        command = NULL_COMMAND_PACKET[:]
        command[PacketIndex.MODETYPE] = ModeType.MELODY
        command[PacketIndex.MODECOMMAND] = 0x00
        command[PacketIndex.DATA0] = 60
        command[PacketIndex.DATA1] = 2  # 0.2초
        command[PacketIndex.DATA2] = 0x00
        command[PacketIndex.INDEX] = self.__get_idx()
        try:
            self.sr.write(bytes(bytearray(command)))
            self.sr.flush()
        except Exception as e:
            print('An Exception occurred!', e)
        self.__process_return()
        return None

    def angle3p(p1, p2, p3):
        """3점 사이의 각도 계산 

        Args:
            p1 : (x1, y1)
            p2 : (x2, y2)
            p3 : (x3, y3)

        Returns:
            시계 반대방향의 각도       
        """
        Ax, Ay = p1[0]-p2[0], p1[1]-p2[1]
        Cx, Cy = p3[0]-p2[0], p3[1]-p2[1]
        a = math.atan2(Ay, Ax)
        c = math.atan2(Cy, Cx)
        if a < 0:
            a += math.pi*2
        if c < 0:
            c += math.pi*2

        rad = (math.pi*2 + c - a) if a > c else (c - a)
        return rad * 180/math.pi

    def remap(self, value, source_range, target_range):
        """Remap a value from the source range to the target range.

        Examples ::

                >>> remap(50, (0, 100), (0, 10))
                5.0

                >>> remap(5, (0, 10), (0, 100))
                50.0

                >>> remap(5, (0, 10), (10, 20))
                15.0

                >>> remap(15, (10, 20), (0, 10))
                5.0

        :param value: The value to be remapped.

        :param source_range: The source range for :code:`value`
        :type source_range: tuple

        :param target_range: The target range for :code:`value`
        :type target_range: tuple

        """
        s0, s1 = source_range
        t0, t1 = target_range
        S = s1 - s0
        T = t1 - t0
        return t0 + ((value - s0) / S) * T
    

# END OF CLASS
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
#-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 
# *-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*- 



