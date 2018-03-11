import math
import copy
class Jobs():
	"""将每一个工序视为一个对象"""
	def __init__(self, job, processing_time, func):
		self.job = job
		self.processing_time = processing_time
		self.func = func
	# 	self.weighted_time()

	# def weighted_time(self):
	# 	"""wi/pi，计算weighted time"""
	# 	self.w_time = float(self.weight/self.processing)

def data_input():
	"""从txt文本中读取数据"""
	jobs = []   #工序的序号
	processing_times = [] #加工时间
	h_c = []  #成本的算术式
	jobs_obj = []   #Jobs对象的列表
	for job_data in open('data.txt','r'):
		print (job_data)
		job, processing_time, func = job_data.split(',')
		processing_time = float(processing_time)
		jobs.append(job)
		processing_times.append(processing_time)
		h_c.append(func)
		jobs_obj.append(Jobs(job,processing_time,func))
	
	return jobs, processing_times, h_c, jobs_obj

def unconstrained(jobs_obj):
	final_jobs = []
	final_jobs_obj = []
	while jobs_obj:
		costs = []
		C = 0
		for job in jobs_obj:
			C += job.processing_time
		for job in jobs_obj:
			costs.append(eval(job.func))
		print (costs)
		num = costs.index(min(costs))
		min_cost_job = jobs_obj.pop(num)
		print (min_cost_job.job)
		final_jobs.insert(0,min_cost_job.job)
		final_jobs_obj.insert(0,min_cost_job)

	print ('最优的加工工序为：',final_jobs)
	C = 0 
	total_cost = 0
	for i in final_jobs_obj:
		C += i.processing_time
		total_cost += eval(i.func)
	print ('total_cost:',total_cost)


def constrained(jobs, jobs_obj, chains):
	"""用于求解工序存在链约束时的情况"""
	"""jobs为所有工序id的列表，jobs_obj是所有Jobs对象的列表， chains是输入的链约束列表"""
	chains_job = []  #所有受到链约束的工序的集合
	job_dict = dict()  #所有job及其包含的信息的字典
	jobs_constrained = []   #受链约束的所有job的集合
	jobs_obj_updated = []	#更新后的job对象列表， [2,3]
	final_jobs = [] #排序好的工序列表
	job_num = len(jobs)  #工序的数量
	for job in jobs_obj:    #用job_obj对象填充job字典
		job_dict[job.job] = [job.processing_time, job.func]

	for chain in chains:
		for job in chain:
			if job not in chains_job:
				chains_job.append(job)
	for job in chains_job:
		jobs.remove(job)
	

	while len(final_jobs)<job_num: #终止条件
		jobs_scheduling = [] #正在进行排序的工序
		chains_job_select = [] #对链中的工序进行分析，可以进行排序的放入到该列表中
		jobs_cost = []  #正在排序的工序计算出的cost的列表
		C = 0    # 正在进行排序的工序的完成时间
		
		if jobs:
			jobs_scheduling = jobs.copy()
		chains_copy = copy.deepcopy(chains) #chains副本
		#print ('chains_job:')
		#print (chains_copy)
		for chain in chains_copy:
			a = None 
			if chain:
				a = chain.pop(-1)
			if a:
				if a not in chains_job_select:
					chains_job_select.append(a)
		for chain in chains_copy:
			for job in chains_job_select:
				if job in chain:
					chains_job_select.remove(job)
		jobs_scheduling = jobs_scheduling + chains_job_select
		#print ("Job on scheduling:")
		#print (jobs_scheduling)
		for job in jobs_scheduling:
			C += job_dict[job][0]
		for job in jobs_scheduling:
			jobs_cost.append(eval(job_dict[job][1]))
		cost_min = jobs_cost.index(min(jobs_cost))
		job_cost_min = jobs_scheduling.pop(cost_min)
		#print (job_cost_min)
		final_jobs.insert(0,job_cost_min)
		if job_cost_min in jobs:
			jobs.remove(job_cost_min)
		for chain_single in chains:
			if job_cost_min in chain_single:
				chain_single.remove(job_cost_min)
		#print (chains)
		# if len(jobs) == 0 :
		# 	del jobs
	print ('最优的加工工序为：',final_jobs)
	C = 0 
	total_cost = 0
	for i in final_jobs:
		C += job_dict[i][0]
		total_cost += eval(job_dict[i][1])
	print ('total_cost:',total_cost)
	
if __name__=="__main__":
	"""主函数"""
	jobs = []   #工序的序号
	processing_times = [] #加工时间
	h_c = []  #成本的算术式
	jobs_obj = []   #Jobs对象的列表
	chains = [] #链约束
	tag = 'a'
	jobs, processing_times, h_c, jobs_obj = data_input()
	print ("是否有约束？")
	con = input('输入y/n:')
	if con == 'y':
		print ("请输入链约束，格式为job1,job2,job3,···,jobn")	
		print ("一条链约束输入完成后回车，所有链约束输入完成后按'q'结束输入。")
		while tag!='q':
			c=input()
			tag = str(c)
			if tag!='q':
				chain = [items for items in c.split(',')]
				chains.append(chain)
		constrained(jobs, jobs_obj, chains)
	else:
		unconstrained(jobs_obj)