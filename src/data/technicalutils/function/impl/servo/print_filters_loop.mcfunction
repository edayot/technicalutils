
tellraw @a[tag=technicalutils.me] ["",{"text": "    "},{"nbt": "servo_filters[0]","storage": "technicalutils:main","color": "white"}]

data remove storage technicalutils:main servo_filters[0]
execute if data storage technicalutils:main servo_filters[0] run function technicalutils:impl/servo/print_filters_loop
