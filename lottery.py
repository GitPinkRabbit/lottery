# lottery.py. Version 20250803-v8
version = '20250803-v8'

import sys
import csv
import random
import getpass
import time
import json
import math


# MXOJ produces such CSV file
csv_file_encoding_mxoj = 'utf-8-sig'
# Luogu produces such CSV file
csv_file_encoding_luogu = 'utf-8-sig'

# Settings
contest_types = ['J', 'S', 'X']
contest_platforms = ['MX', 'LG']
parameters = {platform: {type: [] for type in contest_types} for platform in contest_platforms}
parameters['MX']['X'] = [2, 3, 300]
parameters['MX']['J'] = [3, 4, 100]
parameters['LG']['X'] = [3, 4, 100]
parameters['LG']['J'] = [4, 5, 30]
# prizes for type S is not determined


def get_name_score_rank_from_index_participant_platform(index, participant, platform):
	rank = index + 1
	name = participant[1] if platform == 'MX' else participant[0] if platform == 'LG' else None
	score = int(participant[2] if platform == 'MX' else participant[1] if platform == 'LG' else None)
	return (name, score, rank)


assert len(sys.argv) in [4, 5]
assert sys.argv[1] in contest_types
assert sys.argv[2] in contest_platforms

contest_type = sys.argv[1]
contest_platform = sys.argv[2]
filename = sys.argv[3]
csv_file_encoding = csv_file_encoding_mxoj if contest_platform == 'MX' else csv_file_encoding_luogu if contest_platform == 'LG' else None
time_seed = sys.argv[4] if len(sys.argv) == 5 else str(int(time.time() * 1000))


with open(filename, encoding=csv_file_encoding, newline='') as csv_file:
	reader = csv.reader(csv_file)

	participants = []
	for row in reader:
		participants.append(row)

	rand_seed = ''.join(map(lambda l: ''.join(l), participants))
	random.seed(version + rand_seed + time_seed)
	participants.pop(0)

	number_of_valid_participants = 0
	prize_list = []
	choices = []
	weights = []
	for index, participant in enumerate(participants):
		name, score, rank = get_name_score_rank_from_index_participant_platform(index, participant, contest_platform)
		if score > 0:
			number_of_valid_participants += 1
			choices.append([name, score, rank])
			weights.append(score ** 2)

	X = number_of_valid_participants
	r_rank, r_lucky, champion_prize = parameters[contest_platform][contest_type]
	T_rank = math.floor(math.pow(X, 1 / r_rank))
	T_lucky = math.floor(math.pow(X, 1 / r_lucky))

	prize_list = choices[:T_rank]
	choices = choices[T_rank:]
	weights = weights[T_rank:]
	for _ in range(T_lucky):
		chosen_participant = random.choices(choices, weights)[0]
		prize_list.append(chosen_participant)
		index = choices.index(chosen_participant)
		choices.pop(index)
		weights.pop(index)
	prize_list.sort(key=lambda x: x[2])

	print(f'\t本场比赛为 {contest_type} 组别，请确认！')
	print(f'\t本场比赛平台为 {contest_platform}，请确认！')
	print(f'\t随机种子为 {{{time_seed}}}，发在梦熊周赛选手 QQ 群（650703713）帮助我们记录！', end='\n\n')
	print('', '名次', '分数', '奖金', '用户名', sep='\t', end='', flush=True)
	for index, participant in enumerate(prize_list):
		prize = 0
		if index < T_rank:
			prize = math.ceil(10 * math.pow(champion_prize / 10, 1 - index / T_rank))
		else:
			prize = 10
		name, score, rank = participant
		participant.append(prize)
		if index < T_rank:
			print()
		else:
			getpass.getpass('')
		print('', rank, score, prize, name, sep='\t', end='', flush=True)

	print()
	print()
	print('', '抽奖结束！', sep='\t')
	print(f'\t随机种子为 {{{time_seed}}}，发在梦熊周赛选手 QQ 群（650703713）帮助我们记录！', end='\n\n')
	print('')

	with open(f'MX_lottery_ver{version}_{filename}_{time_seed}.json', 'x', encoding='utf-8') as output_json:
		json.dump({'version': version, 'seed': time_seed, 'prize_list': prize_list}, output_json, ensure_ascii=False, indent=4)
