# lottery.py. Version 20240830-v4
version = '20240830-v4'

import sys
import csv
import random
import getpass
import time
import json


# Hydro OJ produces such CSV file
csv_file_encoding = 'utf-8-sig'

# Settings
contest_types = ['J', 'S', 'X']
prize_count_by_type = {
	'J': [0, 0, 0],
	'S': [0, 1, 4],
	'X': [1, 4, 9]
}
prize_names = ['特等奖', '一等奖', '二等奖']
additional_prize_name = '幸运奖'


assert len(sys.argv) in [3, 4]
assert sys.argv[1] in contest_types

contest_type = sys.argv[1]
filename = sys.argv[2]
time_seed = sys.argv[3] if len(sys.argv) == 4 else str(int(time.time() * 1000))


with open(filename, encoding=csv_file_encoding, newline='') as csv_file:
	reader = csv.reader(csv_file)

	participants = []
	for row in reader:
		participants.append(row)

	rand_seed = ''.join(map(lambda l: ''.join(l), participants))
	random.seed(rand_seed + time_seed)
	participants.pop(0)

	number_of_valid_participants = 0
	prize_lists = [[] for _ in range(len(prize_names) + 1)]
	choices = []
	weights = []
	for participant in participants:
		rank = int(participant[0])
		name = participant[1]
		score = int(participant[6])
		if score > 0:
			number_of_valid_participants += 1
		chosen = False
		for i in range(len(prize_names)):
			if rank <= prize_count_by_type[contest_type][i]:
				prize_lists[i].append((name, score, rank))
				chosen = True
				break
		if not chosen:
			choices.append((name, score, rank))
			weights.append(score ** 2)
	number_of_additional_prize = number_of_valid_participants // 50
	for _ in range(number_of_additional_prize):
		chosen_participant = random.choices(choices, weights)[0]
		prize_lists[-1].append(chosen_participant)
		index = choices.index(chosen_participant)
		choices.pop(index)
		weights.pop(index)
	prize_lists[-1].sort(key=lambda x: x[2])

	print(f'\t本场比赛为 {contest_type} 组别，请确认！')
	print(f'\t随机种子为 {{{time_seed}}}，发在梦熊 OJ 用户 QQ 群（650703713）帮助我们记录！', end='\n\n')
	for i in range(len(prize_names) + 1):
		if not prize_lists[i]:
			continue
		print('\t' + (prize_names[i] if i < len(prize_names) else additional_prize_name + f'（随机种子为 {{{time_seed}}}，发在梦熊 OJ 用户 QQ 群（650703713）帮助我们记录！）') + '：')
		print('', '名次', '分数', '用户名', sep='\t', end='', flush=True)
		for participant in prize_lists[i]:
			if i == len(prize_names):
				getpass.getpass('')
			else:
				print()
			print('', participant[2], participant[1], participant[0], sep='\t', end='', flush=True)
		print()
		print()

	print('', '抽奖结束！', sep='\t')
	print(f'\t随机种子为 {{{time_seed}}}，发在梦熊 OJ 用户 QQ 群（650703713）帮助我们记录！', end='\n\n')
	print('')

	with open(f'MX_lottery_ver{version}_{filename}_{time_seed}.json', 'x', encoding='utf-8') as output_json:
		json.dump({'version': version, 'seed': time_seed, 'prize_lists': prize_lists}, output_json, ensure_ascii=False, indent=4)
