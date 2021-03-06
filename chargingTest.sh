###################################
# script for testing the process of charging	#
# write by logic_wei				#
###################################

############# argument #################

# test for testTime second
testTime=7200 #2 hours
# sample rate
deltaTime=10
# board temp file
boardTempFile=/sys/class/meizu/battery/board_temp
# battery temp file
batteryTempFile=/sys/class/power_supply/battery/temp
# battery current file
batteryCurrentFile=/sys/class/power_supply/battery/current_now
# battery voltage file
batteryVoltageFile=/sys/class/power_supply/battery/voltage_now
# input current file
inputCurrentFile=/sys/class/power_supply/battery/input_current_now
# soc file
socFile=/sys/class/power_supply/battery/capacity


############# program ###############

echo "******************************************"
echo "charging test"
echo "logic_wei@163.com"
echo "******************************************"

timeCount=0
while [ $timeCount -lt $testTime ]
do
	echo -n "timeCount=$timeCount "
	echo -n "boardTemp=$(cat $boardTempFile) "
	echo -n "batteryTemp=$(cat $batteryTempFile) "
	echo -n "batteryCurrent=$(cat $batteryCurrentFile) "
	echo -n "batteryVoltage=$(cat $batteryVoltageFile) "
	echo -n "inputCurrent=$(cat $inputCurrentFile) "
	echo -n "soc=$(cat $socFile) "
	echo ""
	sleep $deltaTime
	let timeCount=$timeCount+$deltaTime
done