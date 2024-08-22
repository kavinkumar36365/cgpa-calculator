from process_details import sgpa
import numpy as np
import time

grades=[]
credits=[]
sgpas=[]

has_arrear=False
#calculate time taken to process the pdfs
start_time = time.time()
cgpa_sem=-1
for i in range(1,7):
    #checkpoint for each pdf time
    start_time_pdf = time.time()
    sgpa_obj=sgpa("sem"+str(i)+".pdf")
    sgpa_obj.calculate_sgpa()
    sgpas.append(sgpa_obj.sgpa)
    grades.append(sgpa_obj.grades)
    credits.append(sgpa_obj.credits)
    has_arrear = has_arrear or sgpa_obj.has_arrear
    if(not has_arrear):
        cgpa_sem=i

    if sgpa_obj.has_arrear:
        print("Arrear in sem"+str(i))

    print("SGPA for sem"+str(i)+": "+str(sgpa_obj.sgpa))
    print("Time taken for sem"+str(i)+": "+str(time.time()-start_time_pdf))


print(sgpas)
grades_temp=np.concatenate(grades[:cgpa_sem])
credits_temp=np.concatenate(credits[:cgpa_sem])
total_credits=np.sum(credits_temp)
cgpa= (np.matmul(grades_temp,np.reshape(credits_temp,(len(grades_temp),-1)))/total_credits)[0]
if has_arrear:
    if cgpa_sem==-1:
        print("Arrear in sem 1 , so CGPA cannot be calculated")
    else:
        print("CGPA up to sem"+str(cgpa_sem)+": "+str(cgpa))
else:
    print("the cgpa is "+str(cgpa))

print("Time taken for all pdfs: "+str(time.time()-start_time))



