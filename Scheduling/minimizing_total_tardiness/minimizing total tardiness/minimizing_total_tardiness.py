#coding = utf-8
import numpy as np
import copy
class Jobs():
	"""将每一个工序视为一个对象"""
	def __init__(self, job, processing_time, due_date):
		self.job = job
		self.processing_time = processing_time
		self.due_date = due_date

def read_data():
	'''从txt文本中读取数据'''
	job_obj_list = [] #工序对象列表
	job_id_list = [] #工序序号列表
	job_dict = dict() #工序信息字典
	pro_time_list = [] #加工时间列表
	due_date_list = [] #到期时间列表
	for job in open('data1.txt','r'):
		job_id, processing_time, due_date = job.split(",")
		processing_time = int(processing_time)
		due_date = int(due_date)
		job_obj = Jobs(job_id, processing_time, due_date)
		pro_time_list.append(processing_time)
		due_date_list.append(due_date)
		job_id_list.append(job_id)
		job_obj_list.append(job_obj)
		job_dict[job_id]=[processing_time, due_date]

	return job_id_list, pro_time_list, due_date_list, job_obj_list, job_dict 

def subsets(job_id_list, pro_time_list, job_dict):
	"""找出所有工序中加工时间最长的一个，并将剩下的工序分成两个子集"""
	subset_1 = []
	subset_2 = []
	
	num = pro_time_list.index(max(pro_time_list))
	m_p = job_id_list[num]
	for i in range(num):
		subset_1.append(job_id_list[i])
	for i in range(num+1,len(job_id_list)):
		
		subset_2.append(job_id_list[i])
	
	return m_p, subset_1, subset_2

def matrix(subset, job_dict):
	chain_matrix = np.zeros([len(subset),len(subset)], dtype = int)
	for i in range(len(subset)):
		job_now = i
		job_next = i+1
		while job_next < len(subset):
			if job_dict[subset[job_now]][0]<=job_dict[subset[job_next]][0]:
				chain_matrix[job_now][job_next] = 1
				job_next += 1
			else:
				job_next +=1
	return chain_matrix	




def chain_constrained(subset,job_dict):

	chain_list = []  #受到约束的链的集合，dj<=dk, pj<=pk	
	chain_matrix = matrix(subset, job_dict)
	    #单条约束链
	for j in range((len(subset)-1)):
		chains_copy = copy.deepcopy(chain_list)
		for k in range(j+1,len(subset)):
			single_chain = []
			if chain_matrix[j][k] == 1:
				single_chain.append(subset[j])
				single_chain.append(subset[k])	
					
				if chain_list:
					n=0					
					for i in range(len(chains_copy)):
						if single_chain:
							if single_chain[0] == chains_copy[i][(len(chains_copy[i])-1)]:
								
								a = copy.deepcopy(chains_copy[i])
								a.append(single_chain[1]) 
								chain_list.insert(i,a)
								n=n+1
					if n==0:
						chain_list.append(single_chain)
					else:
						pass
				else:
					chain_list.append(single_chain)
	
	chain_duplicate = []
	chain_copy2 = copy.deepcopy(chain_list)
	for i in range(len(chain_list)):
		m=0
		chain = chain_copy2.pop(0)
		for chain2 in chain_copy2:
			if set(chain).issubset(set(chain2)):
				m += 1
		if m == 0:
			chain_duplicate.append(chain)
			chain_copy2.append(chain)
	return chain_list


def feasible_procedure(chain_list,subset):
	feasible_chain = []
	chain_length = []
	insert_num = 0 #插入次数
	longest_chain = []
	if len(subset) == 1:
		feasible_chain.append(subset)
	else:
		if chain_list:
			for single_chain in chain_list:
				chain_length.append(len(single_chain))
			longest_chain = chain_list.pop(chain_length.index(max(chain_length)))  #找出所有约束中最长的一条链

			if len(longest_chain) == len(subset):
				feasible_chain.append(longest_chain)
			else:
				locals()['insert_chain'+str(insert_num)] = []
				locals()['insert_chain'+str(insert_num)].append(longest_chain)
				insert_num += 1
				if chain_list:
					for single_chain in chain_list:    #从所有的链约束中取出一条
						for i in range(len(single_chain)):   #链约束的每个元素都进行考虑
							if single_chain[i] not in longest_chain:   #判断该元素是否在最长的链中
								locals()['insert_chain'+str(insert_num)] = []
					
								if i == 0:    #如果是第一个元素
									k=i+1
									upper_bound = len(longest_chain)+1
									while k < len(single_chain):
							
										if single_chain[k] in longest_chain:
											upper_bound = longest_chain.index(single_chain[k])+1
											break
										else:
											k += 1
						
									for insert_chain in locals()['insert_chain'+str((insert_num-1))]:
										for index in range(upper_bound):
											insert_chain_copy = insert_chain.copy()
											insert_chain_copy.insert(index,single_chain[i])
											locals()['insert_chain'+str(insert_num)].append(insert_chain_copy)
									insert_num += 1
									longest_chain.append(single_chain[i])

								elif  0 < i < (len(single_chain)-1):
									j = i-1
									k = i+1
							
									transition = []
									for insert_chain in locals()['insert_chain'+str((insert_num-1))]:
										lower_bound = 0
										while j >= 0:
											if single_chain[j] in insert_chain:
												lower_bound = insert_chain.index(single_chain[j])+1
												break
											else:
												j = j-1

										upper_bound = len(insert_chain)+1
										while k < len(single_chain):
											if single_chain[k] in insert_chain:
												upper_bound = insert_chain.index(single_chain[k])+1
												break
											else:
												k += 1
										
										for index in range(lower_bound, upper_bound):
											insert_chain_copy = insert_chain.copy()
											insert_chain_copy.insert(index,single_chain[i])
											transition.append(insert_chain_copy)
									for t1 in transition:
										locals()['insert_chain'+str(insert_num)].append(t1)
									insert_num += 1
									longest_chain.append(single_chain[i])

								elif i == (len(single_chain)-1):
									k=i-1
						
									transition = []
						
									for insert_chain in locals()['insert_chain'+str((insert_num-1))]:
										lower_bound = 0
										while k >= 0:
											if single_chain[k] in insert_chain:
												lower_bound = insert_chain.index(single_chain[k])+1
												break
											else:
												k = k-1
						
										for index in range(lower_bound,(len(insert_chain)+1)):
											insert_chain_copy = insert_chain.copy()
											insert_chain_copy.insert(index,single_chain[i])
											transition.append(insert_chain_copy)
									for t1 in transition:
										locals()['insert_chain'+str(insert_num)].append(t1)
						
									insert_num += 1					
							else:
								pass
				
							if len(locals()['insert_chain'+str((insert_num-1))][0]) == len(subset):
								for t2 in locals()['insert_chain'+str((insert_num-1))]:
									feasible_chain.append(t2)
								break
				if len(locals()['insert_chain'+str((insert_num-1))][0]) < len(subset):
					nonchain_job = []  #非在链中的job列表
					for job in subset:
						if job not in locals()['insert_chain'+str((insert_num-1))][0]:
							nonchain_job.append(job)
					for job in nonchain_job:
						locals()['insert_chain'+str(insert_num)] = []
						transition = []
						for insert_chain in locals()['insert_chain'+str((insert_num-1))]: 
							for index in range((len(insert_chain)+1)):
								insert_chain_copy = insert_chain.copy()
								insert_chain_copy.insert(index,job)
								transition.append(insert_chain_copy)
						for t1 in transition:
							locals()['insert_chain'+str(insert_num)].append(t1)
						insert_num += 1
					for t2 in locals()['insert_chain'+str((insert_num-1))]:
						feasible_chain.append(t2)
		else:
			for i in range(len(subset)):
				if i == 0 :
					locals()['insert_chain'+str(insert_num)] = []
					locals()['insert_chain'+str(insert_num)].append([subset[i]])
					insert_num += 1
				else:
					locals()['insert_chain'+str(insert_num)] = []
					transition = []
					for insert_chain in locals()['insert_chain'+str((insert_num-1))]:
						lower_bound = 0										
						upper_bound = len(insert_chain)+1				
						for index in range(lower_bound, upper_bound):
							insert_chain_copy = insert_chain.copy()
							insert_chain_copy.insert(index,subset[i])
							transition.append(insert_chain_copy)
					for t1 in transition:
						locals()['insert_chain'+str(insert_num)].append(t1)
					insert_num += 1
			for t2 in locals()['insert_chain'+str((insert_num-1))]:
				feasible_chain.append(t2)

	return feasible_chain		

#dynamic_programming()
if __name__=="__main__":
	whole_tardiness = []
	whole_chain = []
	job_id_list, pro_time_list, due_date_list, job_obj_list, job_dict = read_data()
	m_p, subset_1, subset_2 = subsets(job_id_list, pro_time_list, job_dict)
	m_p_index = job_id_list.index(m_p)
	delta = len(job_id_list) - m_p_index 
	for i in range(delta):
		print (i)
		tardiness_1 = [] 
		tardiness_2 = []
		subset_1_min_tardiness = 0
		m_p_tardiness = 0
		subset_2_min_tardiness = 0
		if i == 0:
			pass
		else:
			a=subset_2.pop(0)
			subset_1.append(a)
			m_p_index += 1
		
		print ('subset1',subset_1)
		print ('subset2',subset_2)
		sum_processing = 0
		sum_tardiness = 0
		"""计算工序m_p之前的工序的误工时间"""
		if subset_1:
			chain_list1 = chain_constrained(subset_1,job_dict)
			feasible_chain1 = feasible_procedure(chain_list1,subset_1)
			print ('feasible_chain1:',feasible_chain1)
			for chain in feasible_chain1:
				sum_processing = 0
				sum_tardiness = 0
				for job in chain:
					sum_processing += job_dict[job][0]
					if sum_processing <= job_dict[job][1]:
						sum_tardiness = sum_tardiness + 0
					else:
						sum_tardiness = sum_tardiness + (sum_processing - job_dict[job][1])
				tardiness_1.append(sum_tardiness)
			subset_1_min_tardiness= min(tardiness_1)
			subset_1_min = feasible_chain1.pop(tardiness_1.index(subset_1_min_tardiness))
		
			"""计算工序m_p的误工时间"""
		sum_tardiness = 0
		sum_processing += job_dict[m_p][0]
		if sum_processing <= job_dict[m_p][1]:
			sum_tardiness = sum_tardiness + 0
		else:
			sum_tardiness = sum_tardiness + (sum_processing - job_dict[m_p][1])
		m_p_tardiness = sum_tardiness
		"""计算工序m_p之工序后的误工时间"""
		proccessed = sum_processing
		if subset_2:
			chain_list2 = chain_constrained(subset_2,job_dict)
			feasible_chain2 = feasible_procedure(chain_list2,subset_2)
			print ('feasible_chain2:',feasible_chain2 )
			for chain in feasible_chain2:
				sum_processing = proccessed
				sum_tardiness = 0
				for job in chain:
					sum_processing += job_dict[job][0]
					if sum_processing <= job_dict[job][1]:
						sum_tardiness = sum_tardiness + 0
					else:
						sum_tardiness = sum_tardiness + (sum_processing - job_dict[job][1])
				tardiness_2.append(sum_tardiness)
			subset_2_min_tardiness= min(tardiness_2)
			subset_2_min = feasible_chain2.pop(tardiness_2.index(subset_2_min_tardiness))
		whole_tardiness.append((subset_1_min_tardiness+m_p_tardiness+subset_2_min_tardiness))
		whole_chain.append(subset_1 + list(m_p) + subset_2_min)
		print (whole_tardiness,whole_chain)
		print ('\n')

	index = whole_tardiness.index(min(whole_tardiness))
	optimal_tardiness = whole_tardiness.pop(index)
	optimal_procedure = whole_chain.pop(index)
	print('最小误工时间：',optimal_tardiness)
	print('最优工作序列：',optimal_procedure)

	# chain_list = chain_constrained(subset1,job_dict)
	# feasible_procedure(chain_list,subset)

	#chain_constrained(subset,job_dict)
	