import serial
import time
import solve

# Arduinoのポートを指定
arduino = serial.Serial('COM6', 9600, timeout=1)
time.sleep(2)  # Arduinoとの接続待ち

x_angles = [155, 125, 103, 70]
y_angles = [(73,151), (68,145), (63,132), (56,124)]

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]
# dir = 0:右, 1:下, 2:左, 3:上

def send_angles(x_angle, y0_angle, y1_angle):
    #角度をArduinoに送信
    command = f"{x_angle},{y0_angle},{y1_angle}\n"
    arduino.write(command.encode())  # 送信
    response = arduino.readline().decode().strip()  # 応答を受信
    print(f"Arduino: {response}")

def move(y, x, dir):
    #(y, x) を dir 方向に1マス移動
    angle0 = (x_angles[x], y_angles[y][0], y_angles[y][1])
    angle0_f = (x_angles[x], y_angles[y][0]+20, y_angles[y][1])
    send_angles(angle0_f[0], angle0_f[1], angle0_f[2])
    time.sleep(1)
    send_angles(angle0[0], angle0[1], angle0[2])
    time.sleep(0.7)
    
    y += dy[dir]
    x += dx[dir]
    angle1 = (x_angles[x]-dx[dir]*40, y_angles[y][0], y_angles[y][1]-dy[dir]*15)
    angle1_f = (x_angles[x]-dx[dir]*40, y_angles[y][0]+20, y_angles[y][1]-dy[dir]*15)
    send_angles(angle1[0], angle1[1], angle1[2])
    time.sleep(0.8)
    send_angles(angle1_f[0], angle1_f[1], angle1_f[2])
    time.sleep(0.3)

def init():
    #初期位置に移動
    send_angles((x_angles[1]+x_angles[2])//2, (y_angles[1][0]+y_angles[2][0])//2+20, (y_angles[1][1]+y_angles[2][1])//2)
    time.sleep(3)
    
def finish():
    #完成のポーズ
    send_angles(90,90,90)
    time.sleep(1)
    for _ in range(10):
        send_angles(90,90,90)
        time.sleep(0.1)
        send_angles(90,90,80)
        time.sleep(0.1)

def main():
    path = solve.solve_puzzle()
    init()
    for y, x, dir in path:
        try:
            print(y,x,dir)
            move(y, x, dir)
        except ValueError:
            print("Invalid input. Please enter three integers (y, x, dir).")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
    finish()
    arduino.close()

if __name__ == "__main__":
    main()