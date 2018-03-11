#coding = utf-8


def data_input():
	"""从txt文本中读取数据"""
	jobs = []
	
	jobs_list = []
	data = dict()
	for job_data in open('data.txt','r'):
		print (job_data)
		job,processing_time, due_date = job_data.split(',')
		processing_time = float(processing_time)
		due_date = float(due_date)
		jobs_list.append(job)
		data[job] = [processing_time,due_date]
	print (jobs_list)
	return jobs_list,data

def tardy_jobs():
	jobs_list = []   #所有工序的列表
	J = []     #在due data 之前完成的工序集合
	J_d = []   #误工的工序集合
	due_dates = []
	processing_times = []  
	data = dict()   #包含所有工序信息的字典
	jobs_list,data = data_input()
	while jobs_list:
		sum_pro_time = 0
		job = jobs_list.pop(0)
		J.append(job)
		processing_times.append(data[job][0])
		due_dates.append(data[job][1])
		num = len(J)-1
		for i in J:
			sum_pro_time += data[i][0]
		if sum_pro_time > data[job][1]:
			job_num=processing_times.index(max(processing_times))
			td_job = J.pop(job_num)
			J_d.append(td_job)
			del processing_times[job_num]
			del due_dates[job_num]
		print ('未误工工序集合：',J,'误工工序集合：',J_d)
	print ("\n")
	print ("最小误工数为："+str(len(J_d)))
	
tardy_jobs()