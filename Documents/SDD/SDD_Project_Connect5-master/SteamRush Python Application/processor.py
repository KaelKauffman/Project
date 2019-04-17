

gui = open("gui_text.txt", 'r')

lines = gui.readlines()
gui.close()

for line in lines:
    code = line.strip()
    if 'connect' in code:
        print(code)

