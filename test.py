from process_details import sgpa
import numpy as np
import time

grades=[]
credits=[]
sgpas = []

#calculate time taken to process the pdfs
start_time = time.time()

for i in range(1,6):
    #checkpoint for each pdf time
    start_time_pdf = time.time()
    sgpa_obj=sgpa("sem"+str(i)+".pdf")
    sgpa_obj.perform_ocr()
    sgpa_obj.calculate_sgpa()
    sgpas.append(sgpa_obj.sgpa)
    grades.append(sgpa_obj.grades)
    credits.append(sgpa_obj.credits)
    print("SGPA for sem"+str(i)+": "+str(sgpa_obj.sgpa))
    print("Time taken for sem"+str(i)+": "+str(time.time()-start_time_pdf))





print(sgpas)
grades=np.concatenate(grades)
credits=np.concatenate(credits)
total_credits=np.sum(credits)
cgpa= (np.matmul(grades,np.reshape(credits,(len(grades),-1)))/total_credits)[0]
print(cgpa)
print("Time taken for all pdfs: "+str(time.time()-start_time))



