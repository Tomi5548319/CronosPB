# Azure web API for CPB
# Made by maCRO Tomi

from urllib.request import urlopen
from datetime import datetime
from datetime import timedelta
import json
import math

from flask import Flask, render_template, request, redirect, url_for

import psycopg2 as psi
import json
import os
import platform
from dotenv import dotenv_values

app = Flask(__name__)

snapshot_at = timedelta(hours=20, minutes=28)

css = "<style>" \
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
      "</style>"

table_css = '<style>' \
            'table {' \
            '  font-family: Arial, Helvetica, sans-serif;' \
            '  border-collapse: collapse;' \
            '  width: 100%;' \
            '}' \
            'table td, table th {' \
            '  border: 1px solid #ddd;' \
            '  padding: 8px;' \
            '}' \
            'table tr:nth-child(even){background-color: #f2f2f2;}' \
            'table tr:hover {background-color: #ddd;}' \
            'table th {' \
            '  padding-top: 12px;' \
            '  padding-bottom: 12px;' \
            '  text-align: left;' \
            '  background-color: #66B1FF;' \
            '  color: white;' \
            '}' \
            '</style>'


@app.route('/')
def index():
    return css + "<script>" \
                 "function changeURL(extension) {" \
                 "window.location.href = window.location.href + extension" \
                 "}" \
                 "</script>" \
                 "<button onclick=\"changeURL('staked_cpb_snapshot/');\">Staked CPB Snapshot</button><br><br>" \
                 "<button onclick=\"changeURL('wallet_checker/');\">Wallet checker</button><br><br>" \
                 "<button onclick=\"changeURL('snapshot_maker/');\">Snapshot maker</button><br><br>"


@app.route('/staked_cpb_snapshot/view/', methods=['GET'])
def staked_snapshot_view():
    try:
        with open(get_file_route('staking.txt'), "r") as all_staking_snapshots:
            try:
                snapshots = all_staking_snapshots.readlines()
                ret = table_css + '<table><tr><th>Date</th><th>Time (UTC)</th><th>CMB staked (old)</th><th>CGB staked (old)</th><th>CMB staked (new)</th><th>CGB staked (new)</th><th>$CPB earned from staking</th><th>$CPB to be minted</th></tr>'

                for snapshot in snapshots:
                    timestamp = str(str(snapshot).split(',')[0])
                    timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
                    date = str(timestamp.strftime("%d. %b. %Y"))
                    time = str(timestamp.strftime("%H:%M"))

                    CMB_staked_old = str(str(snapshot).split(',')[1])
                    CGB_staked_old = str(str(snapshot).split(',')[2])
                    try:
                        CMB_staked_new = str(str(snapshot).split(',')[3])
                        CGB_staked_new = str(str(snapshot).split(',')[4])
                    except Exception:
                        CMB_staked_new = str(0)
                        CGB_staked_new = str(0)

                    CPB_earned_int = (int(CMB_staked_old) + int(CMB_staked_new)) * 30 + (
                            int(CGB_staked_old) + int(CGB_staked_new)) * 8
                    CPB_earned = str(CPB_earned_int) + ' $CPB'
                    CPB_minted = str(CPB_earned_int / 4) + ' $CPB'

                    ret += '<tr><td>' + date + '</td><td>' + time + '</td><td>' + CMB_staked_old + '</td><td>' + CGB_staked_old + '</td><td>' + CMB_staked_new + '</td><td>' + CGB_staked_new + '</td><td>' + CPB_earned + '</td><td>' + CPB_minted + '</td></tr>'

                ret += '</table>'

                return ret

            except Exception:
                return 'Error occured while searching for snapshots'

    except Exception as e:
        return '---Error occured while searching for snapshots---<br>' + str(e)


# TODO update
@app.route('/staked_cpb_snapshot/', methods=['GET'])
def staked_snapshot():
    return "<head>\n" \
           "<title>Staked CPB snapshot</title>\n" \
           "</head>\n" \
           "<body>\n" + \
           css + "<button id=\"btn\" onclick=\"main()\">Make a snapshot of staked CPB</button>\n" \
                 "<button id=\"btn_view\" onclick=\"view_snapshots()\">View snapshots of staked CPB</button>\n" \
                 "<script>\n" \
                 "const start_CMB = 1;\n" \
                 "const end_CMB = 1000;\n" \
                 "const start_CGB = 1;\n" \
                 "const end_CGB = 6100;\n" \
                 "const fetch_limit = 5;\n" \
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
                 "function view_snapshots(){" \
                 "window.location.href = window.location.href + 'view/'" \
                 "}" \
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


@app.route('/wallet_checker/', methods=['GET'])
def wallet_check():
    return css + '<label for="wallet_address">Wallet address:</label>' \
                 '<input id="wallet_address" size="45"><br><br>' \
                 '<button onclick="check_wallet();">Check wallet</button><br>' \
                 '' \
                 '<script>' \
                 '	function check_wallet(){' \
                 '	var wallet_address = document.getElementById(\'wallet_address\').value;' \
                 '   if(wallet_address != ""){' \
                 '	    window.location.href = window.location.href + wallet_address + \'/\';' \
                 '   }' \
                 '	}' \
                 '</script>'


def get_last_update() -> str:
    try:
        with open(get_file_route('staking_last.txt'), "r") as f:
            last_snap = f.readline()
            if last_snap:
                last_timestamp = datetime.strptime(last_snap.split(',')[0], '%Y-%m-%d %H:%M:%S')
                now = datetime.strptime(
                    urlopen('http://just-the-time.appspot.com/').read().strip().decode('utf-8'),
                    '%Y-%m-%d %H:%M:%S')

                time_passed = now - last_timestamp

                return str(time_passed.days) + 'days ' + str(math.floor(time_passed.seconds / 3600)) + 'h ' + str(
                    math.floor(time_passed.seconds / 60) % 60) + 'min'
    except:
        return "---"
    return "---"


@app.route('/wallet_checker/<string:wallet_address>/', methods=['GET'])
def wallet_checker(wallet_address: str):
    try:
        with open(get_file_route('all_cpb.json'), "r") as json_file:
            try:
                holders = json.load(json_file)
                counts = {'CMB': 0, 'CGB': 0}
                staked_counts = {'old': {'CMB': 0, 'CGB': 0},
                                 'new': {'CMB': 0, 'CGB': 0}}

                for collection in holders:
                    for nft_id in holders[collection]:
                        if 'owner' in holders[collection][nft_id] and str(
                                holders[collection][nft_id]['owner']).lower() == str(
                                wallet_address).lower() and collection in counts:
                            counts[collection] += 1
                            if 'staked' in holders[collection][nft_id]:
                                if not holders[collection][nft_id]['staked']:
                                    continue
                                elif holders[collection][nft_id]['staked'] == 'new':
                                    staked_counts['new'][collection] += 1
                                else:
                                    staked_counts['old'][collection] += 1

                return "Wallet: <b>" + str(
                    wallet_address) + '</b><br>(last update ' + get_last_update() + ' ago)<br><br>' \
                       + table_css + '<table><tr><th>Collection</th><th>Available</th><th>Staked (old)</th><th>Staked (new)</th><th>Total</th></tr>' \
                       + '<tr><td>CMB</td><td>' + str(
                    counts['CMB'] - staked_counts['old']['CMB'] - staked_counts['new'][
                        'CMB']) + '</td><td>' + str(staked_counts['old']['CMB']) + '</td><td>' + str(
                    staked_counts['new']['CMB']) + '</td><td>' + str(counts['CMB']) + '</td></tr>' \
                       + '<tr><td>CGB</td><td>' + str(
                    counts['CGB'] - staked_counts['old']['CGB'] - staked_counts['new'][
                        'CGB']) + '</td><td>' + str(staked_counts['old']['CGB']) + '</td><td>' + str(
                    staked_counts['new']['CGB']) + '</td><td>' + str(counts['CGB']) + '</td></tr></table>'

            except Exception as e:
                return "Wallet: " + wallet_address + '<br>---Error 1 occured while searching for NFTs---<br>' + str(e)

    except Exception as e:
        return "Wallet: " + wallet_address + '<br>---Error 2 occured while searching for NFTs---<br>' + str(e)


def get_safe_url(endpoint: str):
    url = url_for(endpoint, _external=True)
    if url.startswith('http:'):
        return 'https:' + url[5:]
    return url


@app.route('/snapshot_maker/', methods=['GET'])
def snapshot_maker():
    return table_css + css + '<h1>Snapshot maker</h1>' \
                             '<label for="min_cmb">Minimum CMB:</label>' \
                             '<input type="number" id="min_cmb" value="0"><br><br>' \
                             '<label for="min_cgb">Minimum CGB:</label>' \
                             '<input type="number" id="min_cgb" value="0"><br><br>' \
                             '<label for="avlbl">Include available (not staked)</label>' \
                             '<input type="checkbox" id="avlbl" checked="true"><br>' \
                             '<label for="staked_old">Include staked (old)</label>' \
                             '<input type="checkbox" id="staked_old" checked="true"><br>' \
                             '<label for="staked_new">Include staked (new)</label>' \
                             '<input type="checkbox" id="staked_new" checked="true"><br><br>' \
                             '<button onclick="make_snapshot(\'table\');">Make snapshot (table)</button><br><br>' \
                             '<button onclick="make_snapshot(\'list\');">Make snapshot (list of eligible wallets)</button><br><br>' \
                             '<button onclick="make_snapshot(\'dictionary\');">Make snapshot ({\'wallet\': {\'CMB\':{\'available\': x, \'staked_old\': x, \'staked_new\': x, \'total_eligible\': x}, CGB:{...}}, \'wallet2\'{...}, ...})</button><br><br>' \
                             '<p id="snapshot_result"></button></p>' \
                             '' \
                             '<script>' \
                             '  function post(url, data) {' \
                             '    return fetch(url, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(data)});' \
                             '  }' \
                             '	function make_snapshot(table_view){' \
                             '	    var min_cmb = document.getElementById(\'min_cmb\').value;' \
                             '	    var min_cgb = document.getElementById(\'min_cgb\').value;' \
                             '	    var available = document.getElementById(\'avlbl\').checked;' \
                             '	    var staked_old = document.getElementById(\'staked_old\').checked;' \
                             '	    var staked_new = document.getElementById(\'staked_new\').checked;' \
                             '      post("' + get_safe_url('make_snapshot') + '", {"table_view": table_view, "min_cmb": min_cmb, "min_cgb": min_cgb, "available": available, "staked_old": staked_old, "staked_new": staked_new}).then(res => {' \
                                                                        '          res.text().then(function(text) {' \
                                                                        'document.getElementById(\'snapshot_result\').innerHTML = text;' \
                                                                        '});' \
                                                                        '      });' \
                                                                        '	    /*console.log("".concat(min_cmb, ",", min_cgb, ",", available, ",", staked_old, ",", staked_new));*/' \
                                                                        '	}' \
                                                                        '</script>'


@app.route('/make_snapshot/', methods=['POST'])
def make_snapshot():
    data = request.get_json()
    table_view = data['table_view']
    min_cmb = int(data['min_cmb'])
    min_cgb = int(data['min_cgb'])
    available = data['available']
    staked_old = data['staked_old']
    staked_new = data['staked_new']

    # 1. Load all holders
    with open(get_file_route('all_cpb.json'), "r") as json_file:
        try:
            holders = json.load(json_file)
            # holders = {
            #     collection: {
            #         int(id): {
            #            "owner": address,
            #            "staked": True/False/'old'/'new' (Check True and old as last)
            #         }
            #     }
            # }
            owners = {}

            for collection in holders:
                if collection not in owners:
                    owners[collection] = {}

                for nft_id in holders[collection]:
                    owner = holders[collection][nft_id]['owner']
                    staked = holders[collection][nft_id]['staked']

                    if owner not in owners[collection]:
                        owners[collection][owner] = {
                            'available': 0,
                            'staked_old': 0,
                            'staked_new': 0,
                            'total_eligible': 0
                        }

                    # 2. Calculate available, staked_old and staked_new for each wallet
                    if staked == 'new':
                        owners[collection][owner]['staked_new'] += 1
                    elif not staked:
                        owners[collection][owner]['available'] += 1
                    else:
                        owners[collection][owner]['staked_old'] += 1

                # 3. Calculate total NFTs from this collection that fit the criteria (staked, unstaked...)
                for owner in owners[collection]:
                    if available:
                        owners[collection][owner]['total_eligible'] += owners[collection][owner]['available']
                    if staked_old:
                        owners[collection][owner]['total_eligible'] += owners[collection][owner]['staked_old']
                    if staked_new:
                        owners[collection][owner]['total_eligible'] += owners[collection][owner]['staked_new']

            # print(owners)

            # 4. Save all owners
            eligible_owners = {}
            for collection in owners:  # ['CMB', 'CGB']
                for owner in owners[collection]:
                    if owner not in eligible_owners:
                        eligible_owners[owner] = {}
                    eligible_owners[owner][collection] = owners[collection][owner]

            # 5. Add CMB or CGB collection to eligible wallets missing this key
            eligible_copy = {}
            for owner in eligible_owners:
                eligible_copy[owner] = eligible_owners[owner]
                if 'CMB' not in eligible_owners[owner]:
                    eligible_owners[owner]['CMB'] = {
                            'available': 0,
                            'staked_old': 0,
                            'staked_new': 0,
                            'total_eligible': 0
                        }
                if 'CGB' not in eligible_owners[owner]:
                    eligible_owners[owner]['CGB'] = {
                            'available': 0,
                            'staked_old': 0,
                            'staked_new': 0,
                            'total_eligible': 0
                        }

                # 6. Remove wallets with not enough CMB or CGB
                for collection in eligible_owners[owner]:
                    if collection == 'CMB' and eligible_owners[owner][collection]['total_eligible'] < min_cmb:
                        eligible_copy.pop(owner)
                        break
                    if collection == 'CGB' and eligible_owners[owner][collection]['total_eligible'] < min_cgb:
                        eligible_copy.pop(owner)
                        break


                    # if collection == 'CMB':
                    #     if min_cmb <= 0 or owners[collection][owner]['total_eligible'] >= min_cmb:
                    #         if owner not in eligible_owners:
                    #             eligible_owners[owner] = {}
                    #         eligible_owners[owner][collection] = owners[collection][owner]
                    #     elif owner in eligible_owners:
                    #         eligible_owners.pop(owner)
                    #
                    # elif collection == 'CGB':
                    #     if min_cgb <= 0 or owners[collection][owner]['total_eligible'] >= min_cgb:
                    #         if owner not in eligible_owners:
                    #             eligible_owners[owner] = {}
                    #         eligible_owners[owner][collection] = owners[collection][owner]
                    #     elif owner in eligible_owners:
                    #         eligible_owners.pop(owner)

            eligible_owners = eligible_copy
            # print(eligible_owners)

            # TODO add time of last update of holders
            if table_view == 'table':
                ret = '<h2>Eligible wallets (last update ' + get_last_update() + ' ago)</h2><table><tr><th>Wallet</th><th>Available CMB</th><th>Staked (old) CMB</th><th>Staked (new) CMB</th><th>Eligible CMB</th><th>Available CGB</th><th>Staked (old) CGB</th><th>Staked (new) CGB</th><th>Eligible CGB</th></tr>'

                for owner in eligible_owners:
                    ret += '<tr><td>' + str(owner) + '</td>'
                    if 'CMB' in eligible_owners[owner]:
                        ret += '<td>' + str(eligible_owners[owner]['CMB']['available']) + '</td>'
                        ret += '<td>' + str(eligible_owners[owner]['CMB']['staked_old']) + '</td>'
                        ret += '<td>' + str(eligible_owners[owner]['CMB']['staked_new']) + '</td>'
                        ret += '<td>' + str(eligible_owners[owner]['CMB']['total_eligible']) + '</td>'
                    else:
                        ret += '<td>0</td><td>0</td><td>0</td><td>0</td>'
                    if 'CGB' in eligible_owners[owner]:
                        ret += '<td>' + str(eligible_owners[owner]['CGB']['available']) + '</td>'
                        ret += '<td>' + str(eligible_owners[owner]['CGB']['staked_old']) + '</td>'
                        ret += '<td>' + str(eligible_owners[owner]['CGB']['staked_new']) + '</td>'
                        ret += '<td>' + str(eligible_owners[owner]['CGB']['total_eligible']) + '</td>'
                    else:
                        ret += '<td>0</td><td>0</td><td>0</td><td>0</td>'
                    ret += '</tr>'

                ret += '</table>'
                return ret
            elif table_view == 'list':
                return '<h2>Eligible wallets (last update ' + get_last_update() + ' ago)</h2>' + str(list(eligible_owners.keys()))
            elif table_view == 'dictionary':
                return '<h2>Eligible wallets (last update ' + get_last_update() + ' ago)</h2>' + str(eligible_owners)

        except Exception as e:
            print(str(e))

    return 'An error occured, please contact the developer (maCRO)'


@app.route('/get_holders/', methods=['GET'])
def get_holders():
    with open(get_file_route('all_cpb.json'), "r") as json_file:
        try:
            holders = json.load(json_file)
            return str(holders)
        except:
            return '{}'


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
    f.write(str(datetime.strptime(urlopen('http://just-the-time.appspot.com/').read().strip().decode('utf-8'),
                                  '%Y-%m-%d %H:%M:%S')) + '|' + log_text + '\n')
    f.close()


@app.route('/save_staked_snapshot/', methods=['POST'])
def save_staked_snapshot():
    global snapshot_at

    try:
        data = request.get_json()
        password = str(data['password'])
        date = str(data['date'])
        time = str(data['time'])
        cmb_staked_old = str(data['cmb_staked_old'])
        cgb_staked_old = str(data['cgb_staked_old'])
        cmb_staked_new = str(data['cmb_staked_new'])
        cgb_staked_new = str(data['cgb_staked_new'])

        log('/save_staked_snapshot/' + password + '/' + date + '/' + time + '/' + cmb_staked_old + '/' + cgb_staked_old + '/' + cmb_staked_new + '/' + cgb_staked_new + '/')

        if access_granted(password):
            save_snapshot = False

            with open(get_file_route('staking_last.txt'), "r") as f:
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

            with open(get_file_route('staking_last.txt'), "w") as f:
                f.write(
                    date + " " + time + "," + cmb_staked_old + "," + cgb_staked_old + "," + cmb_staked_new + "," + cgb_staked_new + "\n")

            if save_snapshot:
                with open(get_file_route('staking.txt'), "a") as f:
                    f.write(
                        date + " " + time + "," + cmb_staked_old + "," + cgb_staked_old + "," + cmb_staked_new + "," + cgb_staked_new + "\n")
                return "Snapshot saved | " + date + " " + time + "," + cmb_staked_old + "," + cgb_staked_old + "," + cmb_staked_new + "," + cgb_staked_new + "\n"
            else:
                return "Snapshot not saved | " + date + " " + time + "," + cmb_staked_old + "," + cgb_staked_old + "," + cmb_staked_new + "," + cgb_staked_new + "\n"

        return "Incorrect password"
    except Exception as e:
        log('/save_staked_snapshot/incorrect_format')
        return 'Error occured: ' + str(e)


@app.route('/update_holders/', methods=['POST'])
def update_holders():
    try:
        data = request.get_json()
        password = data['password']
        new_holders = data['holders']

        log('/update_holders/' + password + '/holders={...}')

        if access_granted(password):
            with open(get_file_route('all_cpb.json'), "r") as json_file:
                holders = {}
                try:
                    holders = json.load(json_file)
                except Exception:
                    holders = {}

                # Update the holders
                for collection in new_holders:
                    if collection not in holders:
                        holders[collection] = {}

                    for nft_id in new_holders[collection]:
                        if 'owner' in new_holders[collection][nft_id] and 'staked' in new_holders[collection][nft_id]:
                            holders[collection][nft_id] = new_holders[collection][nft_id]

                # Save
                with open(get_file_route('all_cpb.json'), 'w') as outfile:
                    outfile.write(json.dumps(holders))

            return "Holders updated successfully"
        return "Incorrect password"

    except Exception as e:
        log('/update_holders/incorrect_format')
        return 'Error occured: ' + str(e)


if __name__ == '__main__':
    app.run()
