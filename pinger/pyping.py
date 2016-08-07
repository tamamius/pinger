import socket
#=============================================#
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

#=============================================#
IPaddr = "192.168.2.10"

ICM_Type = (0x08)
ICM_Code = (0x00)
ICM_ID = (0x01)
ICM_Seq = (0x01)
#=============================================#
ICM_LIST = [0]*6

ICM_LIST[0] = ICM_Type
ICM_LIST[1] = ICM_Code
ICM_LIST[2] = 0#ICM_ChekeSum1
ICM_LIST[3] = 0#ICM_ChekeSum2
ICM_LIST[4] = ICM_ID
ICM_LIST[5] = ICM_Seq
#=============================================#
ICM_DATA = b"abcdefghijklmnopqrstuvwxyz"
ICM_LIST.extend(ICM_DATA)
#=============================================#
csum = 0
for i in range(int(len(ICM_LIST)/2)):
	csum += (ICM_LIST[i*2]<<8) | (ICM_LIST[i*2+1])
csum = (csum&0xffff) + (csum>>16)
csum = 0xffff-(csum)

print("ChekeSum:"+hex(csum))
#=============================================#
ICM_LIST[2] = (csum&0xFF00)>>8        #ICM_ChekeSum2
ICM_LIST[3] = csum&0x00FF     #ICM_ChekeSum1
#=============================================#
print(bytes(ICM_LIST))

sock.sendto(bytes(ICM_LIST), (IPaddr, 0))
#=============================================#
data = sock.recv(255)

for i in range(20,len(data)):
    print ("%r" % hex(data[i])),
#=============================================#