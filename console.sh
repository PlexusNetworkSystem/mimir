#=================danger zone=================#

#api_key=''

#=================danger zone=================#


#=================colors======================#
blink='\e[5m'
cyan='\e[0;36m'
purple='\033[0;35m'
lightcyan='\e[96m'
lightgreen='\e[1;32m'
white='\e[1;37m'
red='\e[1;31m'
yellow='\e[1;33m'
brown='\033[0;33m'
blue='\e[1;34m'
green='\e[0;32m'
tp='\e[0m'
#=================colors======================#

function write_response() {
input_string="$(cat structure/main.system/response.txt)"
output_string=""
counter=1
backtick_count=0
for (( i=0; i<${#input_string}; i++ )); do
  current_char="${input_string:$i:1}"
  if [[ "$current_char" == '`' ]]; then
    backtick_count=$((backtick_count+1))
    if [[ $((backtick_count % 3)) == 0 ]]; then
      if [[ $((counter % 2)) == 1 ]]; then
        output_string+="\e[1;31m"
      else
        output_string+="\e[0;32m"
      fi
      counter=$((counter + 1))
    fi
  else
    output_string+="$current_char"
  fi
done

echo -e "$output_string"

}

function show_animation() {
        loading_anim_list=('/' '-' '\' '|')
        while ! [[ $(cat structure/main.system/check.txt | head -n 1) =~ "1" ]]; do
            for anim in ${loading_anim_list[@]}; do
                echo -ne "\r${tp}[${blue}Thinking${tp}] ${tp}[ ${purple}$anim ${tp}]${tp}"
                sleep 0.2
            done
        done
        echo -ne "\rResponse:                 "
        echo -e "\n${brown}======================================================${green}"
        write_response
        echo "0" > structure/main.system/check.txt
        echo "" > structure/main.system/response.txt
}


while true; do
  read -e -p "$(echo -e "${white}Type the prompt:${cyan} " )" prompt

  if [[ $prompt == "reset context" ]]; then
    python3 structure/main.system/reset_context.py --model-type logical &> /dev/null
    echo -e "${green}Context cleared successfully!"
  :
  elif [[ $prompt == "exit" ]]; then
    echo -e "${red}Exiting...";
    exit
  :
  elif [[ $prompt == "clear" ]]; then
    clear
    echo -e "${blue}Cleared terminal...";
  :
  else
    #echo -e "User: ${blue}$prompt\n"
    python3 structure/main.system/main.py --prompt "$prompt" --model-type logical &> /dev/null &

    show_animation
    echo -e "\n${brown}====================================================== type reset context for reset context" 
  :
  fi
done











