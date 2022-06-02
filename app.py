# Azure web API
from datetime import datetime
from datetime import timedelta
import json

from flask import Flask, render_template, request, redirect, url_for

import psycopg2 as psi
import json
import os
import platform
from dotenv import dotenv_values

app = Flask(__name__)

snapshot_at = timedelta(hours=20, minutes=28)


@app.route('/')
def index():
    return "<style>" \
           "button {" \
           "background-color: #66B1FF;" \
           "border: none;" \
           "color: white;" \
           "padding: 15px 32px;" \
           "text-align: center;" \
           "text-decoration: none;" \
           "display: inline-block;" \
           "font-size: 16px;" \
           "}" \
           "</style>" \
           "<script>" \
           "function changeURL(extension) {" \
           "window.location.href = window.location.href + extension" \
           "}" \
           "</script>" \
           "<button onclick=\"changeURL('staked_cpb_snapshot/');\">Staked CPB Snapshot</button><br><br>" \
           "<button onclick=\"changeURL('wallet_checker/0xF8E5a3916019BCdb8f598BBB5C9fDB9A81349C3f/');\">Wallet checker</button><br><br>"


# def get_linux_conn():
#    auth = dotenv_values("/home/en_var.env")
#
#    return psi.connect(
#        host="147.175.150.216",
#        database="dota2",
#        user=auth["DBUSER"],
#        password=auth["DBPASS"])
#
#
# def get_windows_conn():
#    return psi.connect(
#        host="147.175.150.216",
#        database="dota2",
#        user=os.getenv("DBUSER"),
#        password=os.getenv("DBPASS"))
#
#
# def connect_to_database():
#    if platform.system() == "Linux":
#        return get_linux_conn().cursor()
#    return get_windows_conn().cursor()


@app.route('/staked_cpb_snapshot/', methods=['GET'])
def staked_snapshot():
    #    kurzor = connect_to_database()
    #    kurzor.execute("SELECT VERSION();")
    #    response_version = kurzor.fetchone()[0]
    #
    #    kurzor.execute("SELECT pg_database_size('dota2')/1024/1024 as dota2_db_size;")
    #    response_db_size = kurzor.fetchone()[0]
    #
    #    moj_dic = {}
    #    moj_vnoreny_dic = {}
    #
    #    moj_vnoreny_dic["version"] = response_version
    #    moj_vnoreny_dic["dota2_db_size"] = response_db_size
    #
    #    moj_dic['pgsql'] = moj_vnoreny_dic
    #
    #    kurzor.close()
    #
    #    return json.dumps(moj_dic)
    return "<head>\n" \
           "<title>Staked CPB snapshot</title>\n" \
           "</head>\n" \
           "<body>\n" \
           "<button id=\"btn\" onclick=\"main()\">Make a snapshot of staked CPB</button>\n" \
           "<script>\n" \
           "const start_CMB = 1;\n" \
           "const end_CMB = 1000;\n" \
           "const start_CGB = 1;\n" \
           "const end_CGB = 6100;\n" \
           "const fetch_limit = 5;\n" \
           "</script>\n" \
           "<script>\n" \
           "function main() {\n" \
           "	var button = document.getElementById('btn');\n" \
           "	button.disabled = true;\n" \
           "	\n" \
           "	var left = document.createElement(\"PRE\");\n" \
           "	left.id = \"left\";\n" \
           "	left.textContent = \"CPB left to check: \".concat(max_count-count);\n" \
           "	document.getElementsByTagName(\"body\")[0].appendChild(left);\n" \
           "	\n" \
           "	\n" \
           "	for (var i = 1; i <= fetch_limit; i++) {\n" \
           "		getHolderCMB(i);\n" \
           "	}\n" \
           "	\n" \
           "}\n" \
           "var total_CMB = end_CMB - start_CMB + 1;\n" \
           "var total_CGB = end_CGB - start_CGB + 1;\n" \
           "var max_count = total_CMB + total_CGB;\n" \
           "var count = 0;\n" \
           "var CMBstaked = 0;\n" \
           "var CGBstaked = 0;\n" \
           "function printResults() {\n" \
           "	var CPB_tokens_from_staking = 30 * CMBstaked + 8 * CGBstaked;\n" \
           "	var CPB_tokens_to_be_minted = CPB_tokens_from_staking / 4;\n" \
           "	\n" \
           "	console.log('CMB staked: '.concat(CMBstaked));\n" \
           "	console.log('CGB staked: '.concat(CGBstaked));\n" \
           "	console.log('Total $CPB earned from staking: '.concat(CPB_tokens_from_staking));\n" \
           "	console.log('Total $CPB to be minted: '.concat(CPB_tokens_to_be_minted));\n" \
           "	\n" \
           "	var output = document.createElement(\"PRE\");\n" \
           "	output.textContent = 'CMB staked: '.concat(CMBstaked, '\\n',\n" \
           "	'CGB staked: ', CGBstaked, '\\n',\n" \
           "	'Total $CPB earned from staking: ', CPB_tokens_from_staking, '\\n',\n" \
           "	'Total $CPB to be minted: ', CPB_tokens_to_be_minted);\n" \
           "	document.getElementsByTagName(\"body\")[0].appendChild(output);\n" \
           "}\n" \
           "function incrementCMB(address, token_id) {\n" \
           "	try {\n" \
           "		count++;\n" \
           "		console.log('CMB #'.concat(token_id, ' Loaded, Fetches left: ', max_count-count));\n" \
           "		document.getElementById('left').textContent = \"CPB left to check: \".concat(max_count-count);\n" \
           "		if (address == '0x3390fb0ad64a9f98f343afde813f2561b3facbe5')\n" \
           "			CMBstaked++;\n" \
           "		\n" \
           "		if (count >= max_count)\n" \
           "			printResults();\n" \
           "		else {\n" \
           "			if (token_id + fetch_limit > end_CMB)\n" \
           "				getHolderCGB(((token_id + fetch_limit) % end_CMB) + start_CGB - 1);\n" \
           "			else\n" \
           "				getHolderCMB(token_id + fetch_limit);\n" \
           "		}\n" \
           "	} catch (error) {\n" \
           "		console.error(error);\n" \
           "	}\n" \
           "}\n" \
           "function incrementCGB(address, token_id) {\n" \
           "	try {\n" \
           "		count++;\n" \
           "		console.log('CGB #'.concat(token_id, ' Loaded, Fetches left: ', max_count-count));\n" \
           "		document.getElementById('left').textContent = \"CPB left to check: \".concat(max_count-count);\n" \
           "		if (address == '0x3390fb0ad64a9f98f343afde813f2561b3facbe5')\n" \
           "			CGBstaked++;\n" \
           "		\n" \
           "		if (count >= max_count)\n" \
           "			printResults();\n" \
           "		else {\n" \
           "			if (token_id + fetch_limit <= end_CGB)\n" \
           "				getHolderCGB(token_id + fetch_limit);\n" \
           "		}\n" \
           "	} catch (error) {\n" \
           "		console.error(error);\n" \
           "	}\n" \
           "}\n" \
           "function getHolderCMB(token_id) {\n" \
           "	token_id = token_id.toString(16).padStart(3, '0');\n" \
           "	\n" \
           "	fetch(\"https://rpc.nebkas.ro/\", {\n" \
           "	  \"headers\": {\n" \
           "		\"accept\": \"*/*\",\n" \
           "		\"accept-language\": \"en,sk-SK;q=0.9,sk;q=0.8,cs;q=0.7,en-US;q=0.6\",\n" \
           "		\"content-type\": \"application/json\",\n" \
           "		\"sec-fetch-dest\": \"empty\",\n" \
           "		\"sec-fetch-mode\": \"cors\",\n" \
           "		\"sec-fetch-site\": \"cross-site\",\n" \
           "		\"sec-gpc\": \"1\"\n" \
           "	  },\n" \
           "	  \"referrer\": \"https://cronoscan.com/\",\n" \
           "	  \"referrerPolicy\": \"origin-when-cross-origin\",\n" \
           "	  \"body\": \"{\\\"jsonrpc\\\":\\\"2.0\\\",\\\"id\\\":1,\\\"method\\\":\\\"eth_call\\\",\\\"params\\\":[{\\\"from\\\":\\\"0x0000000000000000000000000000000000000000\\\",\\\"data\\\":\\\"0x6352211e0000000000000000000000000000000000000000000000000000000000000\".concat(token_id,\"\\\",\\\"to\\\":\\\"0x939b90c529f0e3a2c187e1b190ca966a95881fde\\\"},\\\"latest\\\"]}\"),\n" \
           "	  \"method\": \"POST\",\n" \
           "	  \"mode\": \"cors\",\n" \
           "	  \"credentials\": \"omit\"\n" \
           "	})\n" \
           "	.then(response => response.json())\n" \
           "	.then(data => {\n" \
           "	  incrementCMB('0x'.concat(data['result'].substring(26)), parseInt(token_id, 16));\n" \
           "	})\n" \
           "	.catch((error) => {\n" \
           "	  console.error('Error occured while fetching CMB #'.concat(parseInt(token_id, 16), ' (Trying again in 5 seconds...):'), error);\n" \
           "	  setTimeout(getHolderCMB, 5000, token_id);\n" \
           "	});\n" \
           "}\n" \
           "function getHolderCGB(token_id) {\n" \
           "	token_id = token_id.toString(16).padStart(4, '0');\n" \
           "	\n" \
           "	fetch(\"https://rpc.nebkas.ro/\", {\n" \
           "	  \"headers\": {\n" \
           "		\"accept\": \"*/*\",\n" \
           "		\"accept-language\": \"en,sk-SK;q=0.9,sk;q=0.8,cs;q=0.7,en-US;q=0.6\",\n" \
           "		\"content-type\": \"application/json\",\n" \
           "		\"sec-fetch-dest\": \"empty\",\n" \
           "		\"sec-fetch-mode\": \"cors\",\n" \
           "		\"sec-fetch-site\": \"cross-site\",\n" \
           "		\"sec-gpc\": \"1\"\n" \
           "	  },\n" \
           "	  \"referrer\": \"https://cronoscan.com/\",\n" \
           "	  \"referrerPolicy\": \"origin-when-cross-origin\",\n" \
           "	  \"body\": \"{\\\"jsonrpc\\\":\\\"2.0\\\",\\\"id\\\":2,\\\"method\\\":\\\"eth_call\\\",\\\"params\\\":[{\\\"from\\\":\\\"0x0000000000000000000000000000000000000000\\\",\\\"data\\\":\\\"0x6352211e000000000000000000000000000000000000000000000000000000000000\".concat(token_id,\"\\\",\\\"to\\\":\\\"0xc843f18d5605654391e7edbea250f6838c3e8936\\\"},\\\"latest\\\"]}\"),\n" \
           "	  \"method\": \"POST\",\n" \
           "	  \"mode\": \"cors\",\n" \
           "	  \"credentials\": \"omit\"\n" \
           "	})\n" \
           "	.then(response => response.json())\n" \
           "	.then(data => {\n" \
           "	  incrementCGB('0x'.concat(data['result'].substring(26)), parseInt(token_id, 16));\n" \
           "	})\n" \
           "	.catch((error) => {\n" \
           "	  console.error('Error occured while fetching CGB #'.concat(parseInt(token_id, 16)," \
           " ' (Trying again in 5 seconds...):'), error);\n" \
           "	  setTimeout(getHolderCGB, 5000, token_id);\n" \
           "	});\n" \
           "}\n" \
           "</script>\n" \
           "</body>"


@app.route('/wallet_checker/<string:wallet_address>/', methods=['GET'])
def wallet_checker(wallet_address):
    return "Wallet: " + wallet_address + " (TBD)"


def access_granted(password: str) -> bool:
    local_pass = None
    if platform.system() == "Linux":
        local_pass = dotenv_values("/home/access.env")["pass"]
    else:
        local_pass = os.getenv("cpb_pass")

    return local_pass == password


def get_file_route(file: str) -> str:
    path = '/' if platform.system() == "Linux" else ''

    if file == 'staking.txt' or file == 'staking_last.txt':
        path += 'home/snapshots'
    elif file == 'all_cpb.json':
        path += 'home/holders'
    elif file == 'logs.txt':
        path += 'home/logs'
    else:
        path += 'home'
        file = 'err.txt'

    if path is not None:
        if not os.path.exists(path):
            os.makedirs(path)
        file_route = path + '/' + file

        f = open(file_route, "a")
        f.close()
        return file_route
    return 'err2.txt'


def log(log_text: str):
    f = open(get_file_route('logs.txt'), "a")
    f.write(str(datetime.now()) + '|' + log_text + '\n')
    f.close()


@app.route('/save_snapshot/<string:password>/<string:date>/<string:time>/<string:cmb_staked>/<string:cgb_staked>/',
           methods=['GET'])
def save_snapshot(password, date, time, cmb_staked, cgb_staked):
    global snapshot_at

    log('/save_snapshot/' + password + '/' + date + '/' + time + '/' + cmb_staked + '/' + cgb_staked + '/')

    if access_granted(password):
        save_snapshot = False

        f = open(get_file_route('staking_last.txt'), "r")
        last_snap = f.readline()
        if last_snap == '':
            # logs.append('No snapshot made before')
            save_snapshot = True
        else:
            # logs.append('Last snapshot: ' + last_snap)

            last_timestamp_obj = datetime.strptime(last_snap.split(',')[0], '%Y-%m-%d %H:%M:%S')
            # logs.append('Last snapshot timestamp:|' + str(last_timestamp_obj) + '|')

            last_timestamp_reduced = last_timestamp_obj - snapshot_at
            # logs.append('Last snapshot timestamp reduced:|' + str(last_timestamp_reduced) + '|')

            last_snapshot_date = last_timestamp_reduced.date()
            # logs.append('Last snapshot date:|' + str(last_snapshot_date) + '|')

            new_snapshot_date = (datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S') - snapshot_at).date()
            # logs.append('New snapshot date:|' + str(new_snapshot_date) + '|')

            save_snapshot = new_snapshot_date > last_snapshot_date

        f.close()

        if save_snapshot:
            f = open(get_file_route('staking.txt'), "a")
            f.write(date + " " + time + "," + cmb_staked + "," + cgb_staked + "\n")
            f.close()
            f2 = open(get_file_route('staking_last.txt'), "w")
            f2.write(date + " " + time + "," + cmb_staked + "," + cgb_staked + "\n")
            f2.close()
            return "Snapshot saved | " + date + " " + time + "," + cmb_staked + "," + cgb_staked + "\n"
        else:
            return "Snapshot not saved | " + date + " " + time + "," + cmb_staked + "," + cgb_staked + "\n"

    return "Incorrect password"


@app.route('/update_holder/<string:password>/<string:collection>/<string:id>/<string:wallet>/',
           methods=['GET'])
def update_holder(password, collection, id, wallet):
    log('/update_holder/' + password + '/' + collection + '/' + id + '/' + wallet + '/')

    try:
        int(id)
    except Exception:
        return debug_return("ID is not an integer")

    if access_granted(password):
        with open(get_file_route('all_cpb.json')) as json_file:
            holders = {}
            try:
                holders = json.load(json_file)
                if collection in holders:
                    holders[collection][id] = wallet
                else:
                    holders[collection] = {
                        int(id): wallet
                    }


            except Exception:
                holders = {
                    collection: {
                        int(id): wallet
                    }
                }

            # Save
            with open(get_file_route('all_cpb.json'), 'w') as outfile:
                outfile.write(json.dumps(holders))

        return "updating"
    return "Incorrect password"


if __name__ == '__main__':
    app.run()
