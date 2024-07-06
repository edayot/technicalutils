tag @s remove technicalutils.servo.summoned
execute if entity @s[tag=technicalutils.servo.extract] run tag @s add itemio.servo.extract
execute if entity @s[tag=technicalutils.servo.insert] run tag @s add itemio.servo.insert

tag @s add technicalutils.servo

data merge entity @s {Invulnerable:false,Invisible:true,Fixed:false,Silent:true}

data modify entity @s Item set value {id:"minecraft:furnace",count:1}


scoreboard players set @s itemio.servo.stack_limit 1
scoreboard players set @s itemio.servo.retry_limit 1






function #itemio:calls/servos/init