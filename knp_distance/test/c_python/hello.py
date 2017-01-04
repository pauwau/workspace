#hello.py
import ctypes
import time

temp_time = time.time()
for i in range(0,10000000):
	j = i
	if(not j % 1000000):
		print j
ptime = time.time() - temp_time
print("python : " + str(ptime))
hello = ctypes.cdll.LoadLibrary("/home/pau/workspace/test/c_python/hello.so")
temp_time = time.time()
hello.hello() #=>Hello World!
ctime = time.time() - temp_time
print("p : " + str(ptime))
print("c : " + str(ctime))