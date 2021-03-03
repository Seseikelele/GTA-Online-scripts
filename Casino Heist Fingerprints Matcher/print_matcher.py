import ctypes
import pyautogui
import time
#https://gist.github.com/tracend/912308
#https://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
#https://pythonprogramming.net/direct-input-game-python-plays-gta-v/

SendInput = ctypes.windll.user32.SendInput
TAB = 0x0F
ENTER = 0x1C
W = 0x11
A = 0x1E
S = 0x1F
D = 0x20

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
	_fields_ = [
		('wVk', ctypes.c_ushort),
		('wScan', ctypes.c_ushort),
		('dwFlags', ctypes.c_ulong),
		('time', ctypes.c_ulong),
		('dwExtraInfo', PUL)
	]

class HardwareInput(ctypes.Structure):
	_fields_ = [
		('uMsg', ctypes.c_ulong),
		('wParamL', ctypes.c_short),
		('wParamH', ctypes.c_ushort)
	]

class MouseInput(ctypes.Structure):
	_fields_ = [
		('dx', ctypes.c_long),
		('dy', ctypes.c_long),
		('mouseData', ctypes.c_ulong),
		('dwFlags', ctypes.c_ulong),
		('time',ctypes.c_ulong),
		('dwExtraInfo', PUL)
	]

class Input_I(ctypes.Union):
	_fields_ = [
		('ki', KeyBdInput),
		('mi', MouseInput),
		('hi', HardwareInput)
	]

class Input(ctypes.Structure):
	_fields_ = [
		('type', ctypes.c_ulong),
		('ii', Input_I)
	]

def PressKey(key):
	extra = ctypes.c_ulong(0)
	ii_ = Input_I()
	ii_.ki = KeyBdInput(0, key, 0x008, 0, ctypes.pointer(extra))
	x = Input(ctypes.c_ulong(1), ii_)
	SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(key):
	extra = ctypes.c_ulong(0)
	ii_ = Input_I()
	ii_.ki = KeyBdInput(0, key, 0x008 | 0x0002, 0, ctypes.pointer(extra))
	x = Input(ctypes.c_ulong(1), ii_)
	SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def boop_key(key):
	PressKey(key)
	time.sleep(0.015)
	ReleaseKey(key)
	time.sleep(0.020)

def click(locations):
	if 0 in locations:
		boop_key(ENTER)
	boop_key(D)
	if 1 in locations:
		boop_key(ENTER)
	boop_key(S)
	if 2 in locations:
		boop_key(ENTER)
	boop_key(A)
	if 3 in locations:
		boop_key(ENTER)
	boop_key(S)
	if 4 in locations:
		boop_key(ENTER)
	boop_key(D)
	if 5 in locations:
		boop_key(ENTER)
	boop_key(S)
	if 6 in locations:
		boop_key(ENTER)
	boop_key(A)
	if 7 in locations:
		boop_key(ENTER)
	if len(locations) != 4:
		print('something went wrong, help me')
		time.sleep(5)
		return
	boop_key(TAB)
	print('done clicking')

def match_location(x, y):
	if y < 600:
		return 0 if x < 800 else 1
	elif y < 750:
		return 2 if x > 800 else 3
	elif y < 900:
		return 4 if x < 800 else 5
	else:
		return 6 if x > 800 else 7

def click_fingers(num):
	if num < 0 or 4 < num:
		return
	a = f'images/finger_{num}a.png'
	b = f'images/finger_{num}b.png'
	c = f'images/finger_{num}c.png'
	d = f'images/finger_{num}d.png'
	locations = set()
	for finger in [f'images/finger_{num}{letter}.png' for letter in ['a', 'b', 'c', 'd']]:
		x, y = pyautogui.locateCenterOnScreen(finger, region=(600, 300, 400, 830), grayscale=True, confidence=0.7)
		locations.add(match_location(x, y))
	print(locations)
	click(locations)

def find_finger():
	for finger_num in range(1, 5):
		if pyautogui.locateOnScreen(f'images/finger_{finger_num}.png', region=(1200, 100, 700, 900), grayscale=True, confidence=0.9):
			print(f'finger {finger_num} located')
			return finger_num
	return 0

def main():
	while True:
		id = find_finger()
		if id != 0:
			click_fingers(id)
			time.sleep(3.5)
		else:
			time.sleep(0.1)
	print('done')

if __name__ == '__main__':
	main()