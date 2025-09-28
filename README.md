# Turing-complete-cellular-automat
There are only 9 necessary cell types to create turing machine: 1.Empty cell, 2.Lever(ON/OFF), 3.Wire(ON/OFF), 4.NOR element(ON/OFF), and 5.Wire with longer distance to activate(also ON/OFF. It useful for intersections and faster signal speed)

Control:
1 - place lever,
2 - place wire,
3 - place NOR,
4 - place wire+,
q - change condition(ON/OFF),
e - clear cell,
w - rotate up,
a - rotate left,
s - rotate down,
d - rotate right,
esc - exit,
space - start/end execution,
9 - save map,
0 - load map,
up/left/down/right - move review

Rules:
lever - you change its condition yourself. Give signal to all directions,
wire - take signal from red side and give it to blue,
NOR - take signal from any side and give it to all sides. OFF if there is signal from any side, else ON,
wire+ - its like wire, but signal is taken 2 cells away,
