# coding=<utf-8>
#===============================================================================
# Filename   : pyping_0.0.6.py
# Description: pythonを使用したpingツール
# Auther     : tamami uduki
# Created    : 2014/8/24
#===============================================================================
# 初期設定
IPADDR    = "192.168.2.11"
ICMP_TYPE = 0x08
ICMP_CODE = 0x00
ICMP_ID   = 0x01
ICMP_SEQ  = 0x01
# ICMPデータグラム
ICMP_REQ   = [0, 0, 0, 0, 0, 0, 0, 0]
ICMP_MSG  = b"abcdeabcdeabcdeabcdeabcdeabcdeab"
# ping回数
COUNT     = 10
TIMEOUT   = 1.0
INTERVAL  = 0.2
# 結果表示
SUCCESS   = 0
FAILURE   = 0

#===============================================================================
# ここからプログラム部
import socket
import time
import datetime

# socket作成
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
sock.settimeout(TIMEOUT)

# ICMPデータグラム作成(0)

ICMP_REQ[0] = ICMP_TYPE
ICMP_REQ[1] = ICMP_CODE
ICMP_REQ.extend(ICMP_MSG)

for j in range(0,COUNT):

    # ICMPデータグラム作成(1)

    ICMP_REQ[2] = 0x00
    ICMP_REQ[3] = 0x00
    ICMP_REQ[4] = ((0xff00)&ICMP_ID)>>8
    ICMP_REQ[5] = (0x00ff)&ICMP_ID
    ICMP_REQ[6] = ((0xff00)&ICMP_SEQ)>>8
    ICMP_REQ[7] = (0x00ff)&ICMP_SEQ

    # チェックサム計算
    checksum = 0
    for i in range(len(ICMP_REQ)):
        if( i % 2 == 0 ):
            checksum += ICMP_REQ[i]<<8
        else:
            checksum += ICMP_REQ[i]

    checksum = (0xffff&checksum) + (checksum>>16)
    checksum = (0xffff&checksum) + (checksum>>16)  # 足し算で桁あふれした場合の対策
    checksum = 0xffff - checksum

    # ICMPデータグラム作成(2)

    ICMP_REQ[2] = ((0xff00)&checksum)>>8
    ICMP_REQ[3] = (0x00ff)&checksum

    # データの送信
    TIME_SEND = datetime.datetime.now()
    TIME_SEND_STR = TIME_SEND.strftime('%Y-%m-%d %H:%M:%S.%f')
    sock.sendto( bytes(ICMP_REQ), (IPADDR,0) )

    # データの受信
    try:
        ICMP_RES = sock.recv(255)
        TIME_DELTA = datetime.datetime.now() - TIME_SEND

        # ICMP TYPEが0だったらpingOK
        if( ICMP_RES[20] == 0x00 ):
            print("OK {0} {1} {2:.3f}s".format(TIME_SEND_STR, IPADDR, TIME_DELTA.microseconds / 1000000))
            SUCCESS += 1
        else:
            print("NG {0} {1} {2:.3f}s".format(TIME_SEND_STR, IPADDR, TIME_DELTA.microseconds / 1000000))
            FAILURE += 1
    
    except socket.timeout:
        TIME_DELTA = datetime.datetime.now() - TIME_SEND
        print("NG {0} {1} (timeout) {2:.3f}s".format(TIME_SEND_STR, IPADDR, TIME_DELTA.seconds + TIME_DELTA.microseconds / 1000000))
        FAILURE += 1

    ICMP_ID += 1
    ICMP_SEQ += 1
    time.sleep(INTERVAL)

print("成功 {0:d}回、失敗 {1:d}回".format(SUCCESS, FAILURE))

exit()
