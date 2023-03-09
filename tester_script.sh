#!/bin/bash

# THIS SCRIPT TAKES USER INPUT

Color1='\033[1;33m' # Bold Yellow
Color2='\033[0;96m'
NC='\033[0m' # No Color

# Make sure flask app is running -> "$ flask --app iss_tracker.py --debug run"

touch tester_script_output.txt
echo "" > tester_script_output.txt

touch tester_script_stderr.txt
echo "" > tester_script_stderr.txt


echo " "
echo -e "${Color1}This test will call all routes in the iss_tracker.py app${NC}"
echo -e "${Color1}See 'tester_script_output.txt' for the output${NC}"
echo -e "${Color1}See 'tester_script_stderr.txt' for the stderr output, (if runs with no errors only linux run data should be shown, i.e errors due to invalid user input are handled ${NC}"
echo " "
echo -e "${Color2}NOTE: Make sure flask app is running${NC}"
echo " "
echo "What Epoch Variable would you like to use? (Example: 1, 60000000000, abc, -50,)"
read epochVar # USER INPUT


echo "THIS IS THE OUTPUT OF ALL THE ROUTES IN THE 'iss_tracker.py' API" >> tester_script_output.txt 
echo "THIS IS THE STDERR OUTPUT OF ALL THE ROUTES IN THE 'iss_tracker.py' API"  >> tester_script_stderr.txt
echo "If the function runs, only linux runtime data should exist, meaning all bad input data is handled in the API program"  >> tester_script_stderr.txt
echo "Example of normal Linux runtime data:"  >> tester_script_stderr.txt
echo -e "\n" >> tester_script_stderr.txt
echo "Testing Route: '/epochs/-1'
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed

  0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
100    52  100    52    0     0   8666      0 --:--:-- --:--:-- --:--:-- 10400" >> tester_script_stderr.txt
echo -e "\n" >> tester_script_stderr.txt
echo -e "\n" >> tester_script_stderr.txt



echo -e "Real stderr starts here: " >> tester_script_stderr.txt
echo "*************************************************************************************" >> tester_script_stderr.txt
echo -e "\n" >> tester_script_stderr.txt
echo "Using epoch variable: $epochVar"
echo "Using epoch variable: $epochVar" >> tester_script_output.txt 
echo "Using epoch variable: $epochVar" >> tester_script_stderr.txt
echo -e "\n" >> tester_script_output.txt 
echo -e "\n" >> tester_script_stderr.txt


# Commented out methods do not provide helpful output
#echo -e "${Color2}Testing Route: '/'${NC}"
#echo -e "Testing Route: '/'" >> tester_script_output.txt
#echo -e "Testing Route: '/'" >> tester_script_stderr.txt
#curl localhost:5000/ 2 > tester_script_stderr.txt

#echo -e "${Color2}Testing Route: '/epochs'${NC}"
#echo -e "Testing Route: '/epochs'" >> tester_script_output.txt
#echo -e "Testing Route: '/epochs'">> tester_script_stderr.txt
#curl localhost:5000/epochs 2 > tester_script_stderr.txt

echo "*************************************************************************************" >> tester_script_output.txt
echo "*************************************************************************************" >> tester_script_stderr.txt
echo -e "${Color2}Testing Route: '/epochs/$epochVar'${NC}"
echo -e "Testing Route: '/epochs/$epochVar'" >> tester_script_output.txt 
echo -e "Testing Route: '/epochs/$epochVar'">> tester_script_stderr.txt
curl localhost:5000/epochs/$epochVar 1>> tester_script_output.txt 2> /dev/null
curl localhost:5000/epochs/$epochVar 2>> tester_script_stderr.txt 1> /dev/null
echo -e "\n" >> tester_script_output.txt 
echo -e "\n" >> tester_script_stderr.txt

echo "*************************************************************************************" >> tester_script_output.txt
echo "*************************************************************************************" >> tester_script_stderr.txt
echo -e "${Color2}Testing Route: '/epochs/$epochVar/speed'${NC}"
echo -e "Testing Route: '/epochs/$epochVar/speed'" >> tester_script_output.txt
echo -e "Testing Route: '/epochs/$epochVar/speed'">> tester_script_stderr.txt
curl localhost:5000/epochs/$epochVar/speed 1>> tester_script_output.txt 2> /dev/null
curl localhost:5000/epochs/$epochVar/speed 2>> tester_script_stderr.txt 1> /dev/null
echo -e "\n" >> tester_script_output.txt 
echo -e "\n" >> tester_script_stderr.txt


echo "*************************************************************************************" >> tester_script_output.txt
echo "*************************************************************************************" >> tester_script_stderr.txt
echo -e "${Color2}Testing Route: '/epochs/$epochVar/position'${NC}"
echo -e "Testing Route: '/epochs/$epochVar/position'" >> tester_script_output.txt
echo -e "Testing Route: '/epochs/$epochVar/position'">> tester_script_stderr.txt
curl localhost:5000/epochs/$epochVar/position 1>> tester_script_output.txt 2> /dev/null
curl localhost:5000/epochs/$epochVar/position 2>> tester_script_stderr.txt 1> /dev/null
echo -e "\n" >> tester_script_output.txt 
echo -e "\n" >> tester_script_stderr.txt

echo "*************************************************************************************" >> tester_script_output.txt
echo "*************************************************************************************" >> tester_script_stderr.txt
echo -e "${Color2}Testing Route: '/epochs/$epochVar/velocity'${NC}"
echo -e "Testing Route: '/epochs/$epochVar/velocity'}" >> tester_script_output.txt
echo -e "Testing Route: '/epochs/$epochVar/velocity'">> tester_script_stderr.txt
curl localhost:5000/epochs/$epochVar/velocity 1>> tester_script_output.txt 2> /dev/null
curl localhost:5000/epochs/$epochVar/velocity 2>> tester_script_stderr.txt 1> /dev/null
echo -e "\n" >> tester_script_output.txt 
echo -e "\n" >> tester_script_stderr.txt

echo "*************************************************************************************" >> tester_script_output.txt
echo "*************************************************************************************" >> tester_script_stderr.txt
echo -e "${Color2}Testing Route: '/help'${NC}"
echo -e "Testing Route: '/help'" >> tester_script_output.txt
echo -e "Testing Route: '/help'">> tester_script_stderr.txt
curl localhost:5000/help 1>> tester_script_output.txt 2> /dev/null
curl localhost:5000/help 2>> tester_script_stderr.txt 1> /dev/null
echo -e "\n" >> tester_script_output.txt 
echo -e "\n" >> tester_script_stderr.txt

echo "*************************************************************************************" >> tester_script_output.txt
echo "*************************************************************************************" >> tester_script_stderr.txt
echo -e "${Color2}Testing Route: '/delete-data'${NC}"
echo -e "Testing Route: '/delete-data'" >> tester_script_output.txt
echo -e "Testing Route: '/delete-data'">> tester_script_stderr.txt
curl -X DELETE localhost:5000/delete-data 1>> tester_script_output.txt 2> /dev/null
curl -X DELETE localhost:5000/delete-data 2>> tester_script_stderr.txt 1> /dev/null

echo -e "\n" >> tester_script_output.txt 
echo -e "Now Testing a function, assuming delete-data function worked this should output no data" >> tester_script_output.txt
echo -e "\n" >> tester_script_output.txt 
echo -e "Testing Route: '/epochs/$epochVar/velocity'}" >> tester_script_output.txt
echo -e "\n" >> tester_script_output.txt 
echo -e "OUTPUT: (should be 'Data Set is empty' )" >> tester_script_output.txt 
curl localhost:5000/epochs/$epochVar/velocity 1>> tester_script_output.txt 2> /dev/null

echo -e "\n" >> tester_script_output.txt 
echo -e "\n" >> tester_script_stderr.txt

echo "*************************************************************************************" >> tester_script_output.txt
echo "*************************************************************************************" >> tester_script_stderr.txt
echo -e "${Color2}Testing Route: '/post-data'${NC}"
echo -e "Testing Route: '/post-data'" >> tester_script_output.txt
echo -e "Testing Route: '/post-data'">> tester_script_stderr.txt
curl -X POST localhost:5000/post-data 1>> tester_script_output.txt 2> /dev/null
curl -X POST localhost:5000/post-data 2>> tester_script_stderr.txt 1> /dev/null
echo -e "\n" >> tester_script_output.txt 
echo -e "\n" >> tester_script_stderr.txt

echo "*************************************************************************************" >> tester_script_output.txt
echo "*************************************************************************************" >> tester_script_stderr.txt
echo -e "${Color2}Testing Route: '/comment'${NC}"
echo -e "Testing Route: '/comment'" >> tester_script_output.txt
echo -e "Testing Route: '/comment'">> tester_script_stderr.txt
curl localhost:5000/comment 1>> tester_script_output.txt 2> /dev/null
curl localhost:5000/comment 2>> tester_script_stderr.txt 1> /dev/null
echo -e "\n" >> tester_script_output.txt 
echo -e "\n" >> tester_script_stderr.txt

echo "*************************************************************************************" >> tester_script_output.txt
echo "*************************************************************************************" >> tester_script_stderr.txt
echo -e "${Color2}Testing Route: '/header'${NC}"
echo -e "Testing Route: '/header'" >> tester_script_output.txt
echo -e "Testing Route: '/header'">> tester_script_stderr.txt
curl localhost:5000/header 1>> tester_script_output.txt 2> /dev/null
curl localhost:5000/header 2>> tester_script_stderr.txt 1> /dev/null
echo -e "\n" >> tester_script_output.txt 
echo -e "\n" >> tester_script_stderr.txt

echo "*************************************************************************************" >> tester_script_output.txt
echo "*************************************************************************************" >> tester_script_stderr.txt
echo -e "${Color2}Testing Route: '/metadata'${NC}"
echo -e "Testing Route: '/metadata'" >> tester_script_output.txt
echo -e "Testing Route: '/metadata'">> tester_script_stderr.txt
curl localhost:5000/metadata 1>> tester_script_output.txt 2> /dev/null
curl localhost:5000/metadata 2>> tester_script_stderr.txt 1> /dev/null
echo -e "\n" >> tester_script_output.txt 
echo -e "\n" >> tester_script_stderr.txt

echo "*************************************************************************************" >> tester_script_output.txt
echo "*************************************************************************************" >> tester_script_stderr.txt
echo -e "${Color2}Testing Route: '/epochs/$epochVar/location'${NC}"
echo -e "Testing Route: '/epochs/$epochVar/location'" >> tester_script_output.txt
echo -e "Testing Route: '/epochs/$epochVar/location'">> tester_script_stderr.txt
curl localhost:5000/epochs/$epochVar/location 1>> tester_script_output.txt 2> /dev/null
curl localhost:5000/epochs/$epochVar/location 2>> tester_script_stderr.txt 1> /dev/null
echo -e "\n" >> tester_script_output.txt 
echo -e "\n" >> tester_script_stderr.txt

### This takes really long, not sure why but excluding for now. 
#echo -e "${Color2}Testing Route: '/now'${NC}"
#echo -e "Testing Route: '/now'" >> tester_script_output.txt
#echo -e "Testing Route: '/now'">> tester_script_stderr.txt
#curl localhost:5000/now 1 >> tester_script_output.txt 2> /dev/null
#curl localhost:5000/now 2 >> tester_script_stderr.txt 1> /dev/null

# IDEA - put tester files in folder ? will it rewrite existing files?
# mkdir tester_files
# mv tester_script_output.txt tester_script_stderr.txt tester_files
# 
