

tag AirDox_ add convention.debug
execute as @a[tag=convention.debug] run function technicalutils:impl/print_version



scoreboard objectives add technicalutils.data dummy

function technicalutils:impl/load_worldgen


schedule function technicalutils:impl/tick 1t replace
