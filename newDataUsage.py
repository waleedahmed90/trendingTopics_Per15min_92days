#/Users/WaleedAhmed/Documents/THESIS_DS_CODE/June++/dataReadCode_2/hashtag_Usage_Info(3months)

import gzip
import json
import glob
import itertools
from pandas import DataFrame
import matplotlib.pyplot as plt
import ntpath
import time

def Calc_Top_Trends_Func(surge_dict, top_t):

	t = sorted(surge_dict.items(), key = lambda x: x[1], reverse = True)
	
	dict_top_surges = {}
	counter_flag=0
	
	for i in t:
		dict_top_surges[i[0]]=''
		counter_flag = counter_flag + 1

		if counter_flag==top_t:
			#print(dict_top_surges)
			return dict_top_surges

	return dict_top_surges


def calculateSurgeAndTopTrends(prev, curr, usage_thresH, top_t):

	surge_all = {}
	for T in curr.keys():
		if T in prev.keys():
			t_0 = prev[T]
			t_1 = curr[T]

			if t_1>usage_thresH:
				if t_0==0:
					surge_all[T] = t_1
				else:
					surge_all[T] = t_1/t_0

	#print(surge_all)
	temp_return = Calc_Top_Trends_Func(surge_all, top_t)
	return temp_return


def extractUsage_current_stamp(dict_trends):
	current_stamp = {}

	for t in dict_trends.keys():
		current_stamp[t] = len(dict_trends[t])

	return current_stamp


if __name__== "__main__":
	start_time = time.time()
	###########################################################
	#Path to directory containing files
	path_hashtagsDemo = "/Users/WaleedAhmed/Documents/THESIS_DS_CODE/June++/dataReadCode_2/hashtag_Usage_Info(3months)/*.gz"
	#Path String
	list_of_files = sorted(glob.glob(path_hashtagsDemo))
	print("Total Files: ", len(list_of_files))

	#F = list_of_files[1]
	details_top_trends_complete = {}
	#graphName = ntpath.basename(F)+".png"
	file_counter_temp = 1

	usage_threshold = 5
	#usage_threshold = 10
	top_trends  = 10
	
	#F = list_of_files[0]
	#print(ntpath.basename(F))


	stamps_top_trends_dictionary = {}

	#all_files
	for F in list_of_files:

		print(ntpath.basename(F))

		with gzip.open(F, 'rt') as f:
			usageInfo = f.read()
		f.close()
	

		usage_info_list = usageInfo.split("\n")
		total_stamps = len(usage_info_list)-1
		
		

		prev_temp = usage_info_list[0].split("\t")
		temp_time_st = prev_temp[0]
		temp_topics_Usage = json.loads(prev_temp[1])
		
		
		previous_stamp = {}
		#receives a dictionary
		previous_stamp = extractUsage_current_stamp(temp_topics_Usage)
		current_stamp = {}
		
		#per_file
		for s in range(1, total_stamps):
			temp = usage_info_list[s].split("\t")
			time_st = temp[0]
			topics_Usage = json.loads(temp[1])
			
			#dictionary with stamp as key and usage as a value dictionary
			current_stamp = extractUsage_current_stamp(topics_Usage)

			
			#returns a dictionary of top 10 trends until this time stamp {key:''}
			return_value_top_10 = calculateSurgeAndTopTrends(previous_stamp, current_stamp, usage_threshold, top_trends)

			
			#top 10 trends per time stamp for that day
			#stamps_top_trends_dictionary[time_st] = return_value_top_10

			#if type(return_value_top_10) is not None:
			details_top_trends_complete.update(return_value_top_10)
			
			#updating the previous stamp
			previous_stamp = current_stamp
		




	#print(details_top_trends_complete)
	print(len(details_top_trends_complete))


	gend_link = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/June++/dataReadCode_2/Percentage_Demographics/Gender_Percentage_User_Demographics.gz'

	race_link = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/June++/dataReadCode_2/Percentage_Demographics/Race_Percentage_User_Demographics.gz'

	age_link = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/June++/dataReadCode_2/Percentage_Demographics/Age_Percentage_User_Demographics.gz'


	with gzip.open(gend_link, 'rt') as g:
		gend_temp = g.read()
	g.close()

	gend_perc_dict = json.loads(gend_temp)
	
	with gzip.open(race_link, 'rt') as r:
		race_temp = r.read()
	r.close()

	race_perc_dict = json.loads(race_temp)
	
	with gzip.open(age_link, 'rt') as a:
		age_temp = a.read()
	a.close()

	age_perc_dict = json.loads(age_temp)


	GEND_top_Per_TimeStamp = {}
	RACE_top_Per_TimeStamp = {}
	AGE_top_Per_TimeStamp = {}


	for trend in details_top_trends_complete.keys():
		if trend in gend_perc_dict:
			GEND_top_Per_TimeStamp[trend] = gend_perc_dict[trend]
			RACE_top_Per_TimeStamp[trend] = race_perc_dict[trend]
			AGE_top_Per_TimeStamp[trend] = age_perc_dict[trend]


	print(len(GEND_top_Per_TimeStamp))
	print(len(RACE_top_Per_TimeStamp))
	print(len(AGE_top_Per_TimeStamp))

#/Users/WaleedAhmed/Documents/THESIS_DS_CODE/June++/dataReadCode_2/Code_HashtagUsage/Code_per_Time_Stamp/15_min_top
	
	path_15_min_gen = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/June++/dataReadCode_2/Code_HashtagUsage/Code_per_Time_Stamp/15_min_top/'
	path_15_min_race = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/June++/dataReadCode_2/Code_HashtagUsage/Code_per_Time_Stamp/15_min_top/'
	path_15_min_age = '/Users/WaleedAhmed/Documents/THESIS_DS_CODE/June++/dataReadCode_2/Code_HashtagUsage/Code_per_Time_Stamp/15_min_top/'

	with gzip.open(path_15_min_age+'Gend_top_thresH'+str(usage_threshold)+'.gz', 'wb') as f1:
		f1.write(json.dumps(GEND_top_Per_TimeStamp).encode('utf-8'))
	f1.close()
	
	with gzip.open(path_15_min_age+'Race_top_thresH'+str(usage_threshold)+'.gz', 'wb') as f2:
		f2.write(json.dumps(RACE_top_Per_TimeStamp).encode('utf-8'))
	f2.close()
	
	with gzip.open(path_15_min_age+'Age_top_thresH'+str(usage_threshold)+'.gz', 'wb') as f3:
		f3.write(json.dumps(AGE_top_Per_TimeStamp).encode('utf-8'))
	f3.close()


	print("Elapsed Time")
	print("--- %s seconds ---" % (time.time() - start_time))

