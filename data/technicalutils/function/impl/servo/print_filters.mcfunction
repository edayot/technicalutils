


data modify storage technicalutils:main servo_filters set value []
data modify storage technicalutils:main servo_filters set from entity @s Item.components."minecraft:custom_data".itemio.ioconfig.filters

tellraw @a[tag=technicalutils.me] [{"text": "Filters:","color": "green"},{"text": " [","color": "white"}]
execute if data storage technicalutils:main servo_filters[0] run function technicalutils:impl/servo/print_filters_loop
tellraw @a[tag=technicalutils.me] {"text": "]","color": "white"}

data modify entity @s ItemRotation set value 0b


