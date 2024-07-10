# @public

execute 
    if data storage smithed.crafter:input {flags:["technicalutils:filter_not_consume"]} 
    unless items entity @s weapon.mainhand *[minecraft:custom_data~{smithed: {id: "technicalutils:id_filter"}}]
    run scoreboard players set $temp smithed.data 1


