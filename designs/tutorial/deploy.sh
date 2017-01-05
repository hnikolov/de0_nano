#!/bin/bash

#
# deploy
#
# This script deploys files on target FPGA board using ssh and scp.
# sshpass is not used because there is no password set to access the HPS.
#

# defaults
REMOTE_IP=192.168.2.200
REMOTE_PATH=/home/root/tutorial
REMOTE_USER_NAME=root

# provide usage information to user
function printUsage
{
    echo "Usage: $0"
    echo " [-a ip_address] (default = $REMOTE_IP)"
    echo " [-p path]       path on target (default = $REMOTE_PATH)"
    echo " [-f filename]   the file to deploy to target"
    echo " [-gf filename]  generate <filename>.rbf from <filename>.sof"
    echo " [-lf filename]  load the FPGA with $REMOTE_PATH/filename (has to be .rbf)"
    echo " [-e 'binary']   execute a command/script on the target from $REMOTE_PATH/'binary'"
    echo " [-u username]   username for target (default = $REMOTE_USER_NAME)"
    echo " [-h]            show this message"
}

# parse commandline arguments
while getopts a:p:f:ghu:e:l flag; do
  case $flag in
    a)
        echo "using IP address: $OPTARG"
        REMOTE_IP=$OPTARG
        ;;
    p)
        echo "using remote path: $OPTARG"
        REMOTE_PATH=$OPTARG
        ;;
    f)
        FILE_NAME=$OPTARG
        ;;
    g)
        GENERATE_RBF=true
        ;;
    h)
        printUsage
        exit
        ;;
    u)
        echo "using username: $OPTARG"
        REMOTE_USER_NAME=$OPTARG
        ;;
    e)
        echo "executing: $OPTARG"
        REMOTE_COMMAND=$OPTARG
        EXECUTE_RCMD=true
        ;;
    l)
        LOAD_RBF=true
        ;;
    ?)
        printUsage
        exit $LINENO
        ;;
  esac
done

shift $(( OPTIND - 1 ));

# check if a specific file exists
# if the file does not exist show a message and exit script
# $1 command name
function verifyIfFileExists
{
    if [ ! -e "$1" ] 
    then
        echo "file: '$1' does not exist!"
        printUsage
        exit $LINENO
    fi
}

# check if a specific command can be executed
# if the command is not avaiable show a message and exit script
# $1 command name
function verifyIfCommandExists
{
    command -v $1 >/dev/null 2>&1
    COMMAND_PRESENT=$?
    
    if [ $COMMAND_PRESENT -eq 1 ] ; then
        echo >&2 "the command \"$1\" is required but it's not installed. Aborting."
        exit $LINENO
    fi
}

function main
{
    if [ "$GENERATE_RBF" = true ] ; then         
        quartus_cpf -c $FILE_NAME.sof $FILE_NAME.rbf
        exit 0
    fi

    if [ "$LOAD_RBF" = true ] ; then         
        ssh $REMOTE_USER_NAME@$REMOTE_IP "cd $REMOTE_PATH; ./load.sh $FILE_NAME"
        exit 0
    fi

    if [ "$EXECUTE_RCMD" = true ] ; then         
        ssh $REMOTE_USER_NAME@$REMOTE_IP "$REMOTE_PATH/$REMOTE_COMMAND"
        exit 0
    fi

    # verify dependencies
    verifyIfFileExists $FILE_NAME
    verifyIfCommandExists ssh
    verifyIfCommandExists scp
    
    # echo "deploying: '$FILE_NAME'"

    # copy the file to the remote location
    scp $FILE_NAME $REMOTE_USER_NAME@$REMOTE_IP:$REMOTE_PATH/$FILE_NAME

    exit 0
}

main
