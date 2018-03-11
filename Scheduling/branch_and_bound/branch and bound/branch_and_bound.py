#coding = utf-8

def read_data(data_name):
	job_id_list = []
	processing_time_list = []
	release_time_list = [] 
	due_time_list = []
	jobs_dict = dict()
	for job in open(data_name,'r'):
		job_id, processing_time, release_time, due_time = job.split(",")
		processing_time = int(processing_time)
		release_time = int(release_time)
		due_time = int(due_time)
		job_id_list.append(job_id)
		processing_time_list.append(processing_time)
		release_time_list.append(release_time)
		due_time_list.append(due_time)
		jobs_dict[job_id] = [processing_time, release_time, due_time]

	return job_id_list, processing_time_list, release_time_list, due_time_list, jobs_dict

def branch_and_bound(job_id_list, processing_time_list, release_time_list, due_time_list, jobs_dict):
	tree = []
	level = 0

	while level < (len(job_id_list)-1):

		if level == 0 :

			level += 1
			str(level)
			print('level'+str(level))
			t = 0
			distin = []
			
			locals()['level'+str(level)] = []
			"""根据rjk < min(max(t, rl) + pl)判断是否可以生成该分支"""
			for job in job_id_list:
				first_place = []
				on_schedule = job_id_list.copy()
				on_schedule.remove(job)
				for on_schedule_job in on_schedule:
					if jobs_dict[on_schedule_job][1] > t:
						score = jobs_dict[on_schedule_job][1] + jobs_dict[on_schedule_job][0]
						distin.append(score)
					else:
						score = t + jobs_dict[on_schedule_job][0]
						distin.append(score)
				min_score = distin.pop(distin.index(min(distin)))
				if min_score > jobs_dict[job][1]:
					first_place.append(job)
					locals()['level'+str(level)].append(first_place)
			print ('branch:',locals()['level'+str(level)])
			locals()['level'+str(level)] = lower_bound(locals()['level'+str(level)], job_id_list, jobs_dict)
			
		if 0 < level < (len(job_id_list)-1):
			level += 1	
			print ('level'+str(level))
			scheduling = []
			distin = []
			locals()['level'+str(level)] = []
			"""计算时间已经排好的工序的时间t,例如从第一层向第二层进发是，工序1已经排好，所以现在时间t为4，
			从第二层向第三层进发时，1,3已经排好，所以现在的时间t为4+6=10"""
			t = 0  #
			for index in range(len(locals()['level'+str(level-1)])):
				if index == 0:
					t = jobs_dict[job_id_list[index]][0] + jobs_dict[job_id_list[index]][1]
				else:
					if jobs_dict[job_id_list[index]][1] <= t:
						t = t + jobs_dict[job_id_list[index]][0]
					else:
						t = jobs_dict[job_id_list[index]][0] + jobs_dict[job_id_list[index]][1]

			for job in job_id_list:
				if job not in locals()['level'+str(level-1)]:
					scheduling.append(job)			
			"""根据rjk < min(max(t, rl) + pl)判断是否可以生成该分支"""
			for job in scheduling:
				on_schedule = scheduling.copy()
				on_schedule.remove(job)
				for on_schedule_job in on_schedule:
					if jobs_dict[on_schedule_job][1] > t:
						score = jobs_dict[on_schedule_job][1] + jobs_dict[on_schedule_job][0]
						distin.append(score)
					else:
						score = t + jobs_dict[on_schedule_job][0]
						distin.append(score)
				min_score = distin.pop(distin.index(min(distin)))
				if min_score > jobs_dict[job][1]:
					feasible_procedure = locals()['level'+str(level-1)].copy()
					feasible_procedure.append(job)
					locals()['level'+str(level)].append(feasible_procedure)
			print ('branch:',locals()['level'+str(level)])
			locals()['level'+str(level)] = lower_bound(locals()['level'+str(level)], job_id_list, jobs_dict)
	
		
		if level == (len(job_id_list)-1):
			#print ('aaaaaaa')
			for job in job_id_list:
				if job not in locals()['level'+str(level)]:
					locals()['level'+str(level)].append(job)
					break
		print ('level_final', level)

		
	print ('工作序列：',locals()['level'+str(level)])
	



def lower_bound(level_n, job_id_list, jobs_dict):
	L_max_list = []
	level_n_scheduled = []

	for branch in level_n:  #遍历第n层的所有分支
		now_time = 0
		scheduling = job_id_list.copy()
		due_times = []
		edd = []  #按照early due date 的规则对工序进行排序
		processing_times = []  # 排序后的工序的processing_time，随着时间递减，当processing_time为0时，工序加工完成
		scheduled = []
		finish_time = []
		lateness = []
		for job in branch:     
			if job in scheduling:
				scheduling.remove(job)
		for job in scheduling:
			due_times.append(jobs_dict[job][2])
		for i in range(len(due_times)):
			
			early_due_date = scheduling.pop(due_times.index(min(due_times)))
			due_times.pop(due_times.index(min(due_times)))
			edd.append(early_due_date)
		for job in edd:
			processing_times.append(jobs_dict[job][0])


		for index in range(len(branch)):
			if index == 0:
				now_time = jobs_dict[branch[index]][0] + jobs_dict[branch[index]][1]
				finish_time.append(now_time)
			else:
				if jobs_dict[branch[index]][1] <= now_time:
					now_time = now_time + jobs_dict[branch[index]][0]
					finish_time.append(now_time)
				else:
					now_time = jobs_dict[branch[index]][0] + jobs_dict[branch[index]][1]
					finish_time.append(now_time)
	
		while edd:
			tag = 0
		
			for index in range(len(edd)):
				if jobs_dict[edd[index]][1] <= now_time:
					processing_times[index] = processing_times[index] - 1
					now_time += 1
					tag += 1
					if processing_times[index] == 0 :
						processing_times.pop(index)
						scheduled.append(edd.pop(index))
						finish_time.append(now_time)
					break
			if tag == 0 :
				now_time += 1
		scheduled = branch + scheduled
		for index in range(len(scheduled)):
			if finish_time[index] <= jobs_dict[scheduled[index]][2]:
				lateness.append(0)
			else:
				lateness.append((finish_time[index]-jobs_dict[scheduled[index]][2]))
		level_n_scheduled.append(scheduled)
		L_max_list.append(lateness.pop(lateness.index(max(lateness))))


				
		#print (scheduled, finish_time)

	print ('level_n_scheduled:',level_n_scheduled, 'lower_bound:',L_max_list)
	print ('level_n[L_max_list.index(min(L_max_list))]',level_n[L_max_list.index(min(L_max_list))])
	return level_n[L_max_list.index(min(L_max_list))]
	
if __name__ == '__main__':
	data_name = 'data.txt'
	job_id_list, processing_time_list, release_time_list, due_time_list, jobs_dict = read_data(data_name)
	print (job_id_list)
	branch_and_bound(job_id_list, processing_time_list, release_time_list, due_time_list, jobs_dict)
	# level_n = [['1','2'],['1','3'],['1','4']]
	# lower_bound(level_n, job_id_list, jobs_dict)



