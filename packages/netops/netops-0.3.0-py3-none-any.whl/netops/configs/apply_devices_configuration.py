import json
import os
from socket import timeout

from nornir.core.exceptions import ConnectionNotOpen, NornirExecutionError
from nornir_pyez.plugins.tasks import pyez_config, pyez_diff, pyez_commit
from nornir_netmiko import netmiko_send_config, netmiko_commit, netmiko_send_command, netmiko_multiline
from nornir_utils.plugins.functions import print_result
from contextlib import redirect_stdout
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError
from jnpr.junos.exception import LockError
from jnpr.junos.exception import RpcError
from jnpr.junos.exception import CommitError
from jnpr.junos.exception import UnlockError

from ..utils.utils import print_json, remove_empty_lines
from ..api.netbox.netbox_manager import NetboxManager
from ..api.netbox.util import get_sot_filter_parameters
from .models import EXECUTION_STATUS, CONFIG_SCENARIO

cfg_mode_flag = True

def try_apply_config(config_file_path, retries=3, check_params=None, commit=False, rollback_error=True):
    """
	TODO: write docstrings
	"""

    diff_file = '/tmp/show_compare.txt'
    ntry = 1 # number of exec try
    while ntry <= int(retries):
        # Necessario que as funcoes raise_on_error estejam funcionais para a checagem de tentativas funcionarem
        result = apply_config(config_file_path, diff_file=diff_file, check_params=check_params, commit=commit)
        exec_status = result['execution_status']
        config_scenario = result['config_scenario']
        if exec_status == EXECUTION_STATUS['SUCCESSFULL']:
            break
        ntry += 1
    
    if commit:
        dev_config = json.load(fp=open(config_file_path, "r"))
        for sequencial_task in dev_config["sequential"]:
            for config in sequencial_task["configuration"]:
                if config["metadata"]["commited"] == "nok":
                    print(f"Error configuring devices after {retries} retries")
                    exit(1)

    if exec_status == EXECUTION_STATUS['FAILED']:
        print("Configuration apply has FAILED!")
        exit(1)
    if config_scenario == CONFIG_SCENARIO['ROLLBACK']:
        print("Configuration databases has been ROLLBACKED!")
        print("Raise error on rolling back configuration: ", rollback_error)
        if rollback_error:
            # If it must generate an error state when rollbacked
            print("Please, check what happened in previous tests!")
            exit(1)
        else:
            # When it must not generate error state when rollbacked
            exit(0)
 
    return result


def apply_config(config_file_path, diff_file, check_params, commit):
    """
	TODO: write docstrings
	"""
    ro = {}

    # exec_status represents the execution status
    try:
        filter_params = get_sot_filter_parameters()
        netbox_manager = NetboxManager(filter_params=filter_params)

        dev_config = json.load(fp=open(config_file_path, "r"))
        
        stc = 0 #sequential task counter
        for sequencial_task in dev_config["sequential"]:
            device_name = sequencial_task["device_name"]
            host = netbox_manager.get_nornir().filter(name=device_name)
            device_platform = host.inventory.hosts[device_name].platform
            
            cc = 0 # configuration counter
            for config in sequencial_task["configuration"]:
                #dev_config["sequential"][stc]["configuration"][cc]
                if config["metadata"]["commited"] == "nok":
                    config_scenario = CONFIG_SCENARIO["DEFAULT"]
                    if device_platform == "junos":
                        config_scenario, commit_status = junos_config(config_scenario, host, config, device_name, diff_file, check_params, commit)
                    elif device_platform == "huawei_vrpv8":
                        config_scenario, commit_status = huawei_vrpv8_config(config_scenario, host, config, diff_file, check_params, commit)
                    elif device_platform == "huawei":
                        if not commit:
                            #Dry runs sao ignoradas em equipamentos com platform Huawei
                            print("Huawei platform doesn't have commit option. Skipping dry-run")
                            commit_status = False
                        #Huawei platform doesn't have commit option. Each commands is applied immediately. 
                        config_scenario, commit_status, result = huawei_config(config_scenario, host, config)
                        if result is not None:
                            ro['huawei_failed_command'] = result['command']
                            ro['huawei_fail_context'] = result['context']
                            raise Exception(f"Error configuring device: {device_name}")
                    else:
                        if device_platform:
                            raise Exception(f"Error configuring device {device_name}: platform {device_platform} not supported")
                        else:
                            raise Exception(f"Error configuring device {device_name}: platform field not set")
                    exec_status = EXECUTION_STATUS['SUCCESSFULL']
                    if commit_status:
                        # Somente e executado se nao for gerado erro de configuracao
                        dev_config["sequential"][stc]["configuration"][cc]["metadata"]["commited"] = "ok"
                        # A cada iteracao o estado do dev_config e gravado para que em erros subsequentes o estado seja armazenado
                        print_json(dev_config, config_file_path)
                        print("Device configuration object after commit: ")
                        print_json(dev_config)
                    if config_scenario == CONFIG_SCENARIO["ROLLBACK"]:
                        break
                cc += 1
            host.close_connections()
            stc += 1
        
        print_json(dev_config, config_file_path)

    except NornirExecutionError as e:
        exec_status = EXECUTION_STATUS['FAILED']
        print("Error NornirExecutionError !", str(e))
        try:
            host.close_connections()
        except ConnectionNotOpen as e:
            print("Error ConnectionNotOpen !", str(e))
        #Nao utilizado quando realizando multiplas tentativas de execucao
        #exit(1)
    except Exception as e:
        exec_status = EXECUTION_STATUS['FAILED']
        print("Error!", str(e))

    #Return object
    ro['config_scenario'] = config_scenario
    ro['execution_status'] = exec_status
    print(ro)

    return ro


def check_config(diff_file, check_params):
    """
	TODO: write docstrings
	"""

    with open(diff_file, 'r') as file:  # Use file to refer to the file object
        lines = file.readlines()
        for line in lines:
            print(line.strip('\n'))
            if check_params:
                for param in check_params:
                    if param in line:
                        print("")
                        print("ERRO! Parametro indevido encontrado no DIFF result. Favor verificar.")
                        exit(1)
    
    return


def junos_rollback(host, device_name, rb_id=1):
    """
	TODO: write docstrings
	"""
    
    dev = Device(
        host=host.inventory.hosts[device_name].hostname, 
        user=host.inventory.hosts[device_name].username, 
        passwd=host.inventory.hosts[device_name].password,
        port=host.inventory.hosts[device_name].port
    )
    # open a connection with the device and start a NETCONF session
    try:
        dev.open()
    except ConnectError as err:
        print ("Cannot connect to device: {0}".format(err))
        return EXECUTION_STATUS["FAILED"]

    # Set up config object
    cu = Config(dev)

    # Lock the configuration
    print ("Locking the configuration")
    try:
        cu.lock()
    except LockError as err:
        print ("Unable to lock configuration: {0}".format(err))
        dev.close()
        return EXECUTION_STATUS["FAILED"]
    try:
        print ("Rolling back the configuration")
        cu.rollback(rb_id=rb_id)
        print ("Compare the candidate configuration to the rollback configuration:")
        cu.pdiff()
        print ("Committing the configuration")
        cu.commit(timeout=60)
    except CommitError as err:
        print ("Error: Unable to commit configuration: {0}".format(err))
        dev.close()
        return EXECUTION_STATUS["FAILED"]
    except RpcError as err:
        print ("Unable to roll back configuration changes: {0}".format(err))
        dev.close()
        return EXECUTION_STATUS["FAILED"]
    finally:
        print ("Unlocking the configuration")
        try:
            cu.unlock()
        except UnlockError as err:
            print ("Unable to unlock configuration: {0}".format(err))
            dev.close()
            return EXECUTION_STATUS["FAILED"]
        dev.close()
        return EXECUTION_STATUS["SUCCESSFULL"]

def huawei_vrpv8_rollback(host, rb_number = 1):
    try:
        print ("Locking the configuration")
        result = host.run(task=netmiko_send_config, config_commands=["configuration exclusive","return"], error_pattern=r"Error")
        result.raise_on_error()
    except:
        print ("Unable to lock configuration")
        return EXECUTION_STATUS["FAILED"]
    try:
        rollback_cmds = [
            [f"rollback configuration last {rb_number}", r"Y/N"],
            ["Y", ""]
        ]
        print ("Rolling back the configuration")
        result = host.run(task=netmiko_multiline, commands=rollback_cmds)
        result.raise_on_error()
        print_result(result)
        #After the user logs out, the configuration is unlocked automatically.
        host.close_connections()
        return EXECUTION_STATUS["SUCCESSFULL"]
    except Exception as e:
        print(f"Error in Huawei rollback: {e}")
        return EXECUTION_STATUS["FAILED"]



def junos_config(config_scenario, host, config, device_name, diff_file, check_params, commit):
    if config["type"] == "procedural":
        
        payload = None
        for statement in config["content"]:
            if payload:
                payload = payload + os.linesep + str(statement)
            else:
                payload = str(statement)
        if 'rollback ' in payload:
            config_scenario = CONFIG_SCENARIO["ROLLBACK"]
            print("----------------- Rolling back configuration database... -----------------")
            result = junos_rollback(host, device_name)
            if result == EXECUTION_STATUS["FAILED"]:
                commit_status = False
            else:
                commit_status = True
            return config_scenario, commit_status

        config_response = host.run(
            task=pyez_config, payload=payload, data_format="set")
        print_result(config_response)
        config_response.raise_on_error()
        diff_response = host.run(task=pyez_diff)
        diff_response.raise_on_error()
        #print_result(diff_response)
        with open(diff_file, 'w') as file:  # Use file to refer to the file object
            with redirect_stdout(file):
                print_result(diff_response)
        remove_empty_lines(diff_file)
        check_config(diff_file, check_params)

        # COMMIT----------------------------
        if commit:
            #print_result(diff_response)
            print("----------------- Commiting change... -----------------")
            commit_response = host.run(task=pyez_commit)
            commit_response.raise_on_error()
            print("Exec status commit Juniper: SUCCESS")
            return config_scenario, commit
        # ------------------------------------

        return config_scenario, commit

    if config["type"] == "json-rpc":
        payload = str(config["content"])
        config_response = host.run(
            task=pyez_config, payload=payload, data_format="text")
        print_result(config_response)
        #config_response.raise_on_error()
        diff_response = host.run(task=pyez_diff)
        #diff_response.raise_on_error()
        print_result(diff_response)
        # COMMIT----------------------------
        if commit:
            print("----------------- COMMITING CHANGES... -----------------")
            commit_response = host.run(task=pyez_commit)
            commit_response.raise_on_error()
            return config_scenario, commit
        # ------------------------------------
        return config_scenario, commit

def huawei_vrpv8_config(config_scenario, host, config, diff_file, check_params, commit):
    if config["type"] == "procedural":
        if 'rollback' in config['content']:
            config_scenario = CONFIG_SCENARIO["ROLLBACK"]
            print("----------------- Rolling back configuration database... -----------------")
            result = huawei_vrpv8_rollback(host)
            if result == EXECUTION_STATUS["FAILED"]:
                commit_status = False
            else:
                commit_status = True
            return config_scenario, commit_status

        config_response = host.run(
            task=netmiko_send_config, config_commands=config['content'], error_pattern=r"Error"
        )   
        print_result(config_response)
        config_response.raise_on_error()

        diff_response = host.run(task=netmiko_send_command, command_string="display configuration commit changes last 1")
        with open(diff_file, 'w') as file:  # Use file to refer to the file object
            with redirect_stdout(file):
                print_result(diff_response)
        remove_empty_lines(diff_file)
        check_config(diff_file, check_params)

        # COMMIT----------------------------
        if commit:
            #print_result(diff_response)
            print("----------------- Commiting change... -----------------")
            commit_response = host.run(task=netmiko_commit)
            commit_response.raise_on_error()
            print("Exec status commit huawei: SUCCESS")
            return config_scenario, commit
        # ------------------------------------
        return config_scenario, commit
    else:
        raise Exception("Huawei config type not supported")

def huawei_config(config_scenario, host, config):
    global cfg_mode_flag
    if config["type"] == "procedural":
        commit = True
        cfg_mode_flag = True
        result = send_config_huawei(host, 'base', config['content'])
        return config_scenario, commit, result
    else:
        raise Exception("Huawei config type not supported")
    

def send_config_huawei(host, context, commands):
    '''
    recebe objeto host, contexto e lista de comandos
    retorna None caso a configuracao tenha sido bem sucedida
    retorna dicionario contendo o contexto(view) e comando que falhou, em caso de erro
    '''
    global cfg_mode_flag
    try:
        if context != 'base':
            cmd = context
            config_response = host.run(task=netmiko_send_config, config_commands=[cmd], error_pattern=r"Error", exit_config_mode=False, enter_config_mode = cfg_mode_flag)   
            cfg_mode_flag = False
            config_response.raise_on_error()

        for cmd in commands:
            #Enter subcontexts recursivelly
            if isinstance(cmd, dict):
                for subcontext in cmd:
                    response = send_config_huawei(host, subcontext, cmd[subcontext])
                    if response is not None:
                        return response
                continue
            config_response = host.run(task=netmiko_send_config, config_commands=[cmd], error_pattern=r"Error", exit_config_mode=False, enter_config_mode=cfg_mode_flag)   
            cfg_mode_flag = False
            config_response.raise_on_error()
        
        #quit context
        if context != 'base':
            cmd = 'quit'
            config_response = host.run(task=netmiko_send_config, config_commands=[cmd], error_pattern=r"Error", exit_config_mode=False, enter_config_mode=cfg_mode_flag)   
            config_response.raise_on_error()

        return None

    except Exception as e:
        print(e)
        host.close_connections()
        error_obj = {'context': context, 'command': cmd}
        return error_obj


