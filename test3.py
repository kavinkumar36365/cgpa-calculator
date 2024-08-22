import asyncio
import time
from process_details import sgpa
import numpy as np

async def process_semester(sem_number):
    sgpa_obj = sgpa("sem" + str(sem_number) + "a.pdf")
    sgpa_obj.perform_ocr()
    sgpa_obj.calculate_sgpa()
    return sgpa_obj.sgpa, sgpa_obj.grades, sgpa_obj.credits

async def main():
    start_time = time.time()
    tasks = [asyncio.create_task(process_semester(i)) for i in range(1, 6)]
    sgpas = []
    grades = []
    credits = []
    
    for i, task in enumerate(tasks, start=1):
        sgpa_val, grade_val, credit_val = await task
        sgpas.append(sgpa_val)
        grades.append(grade_val)
        credits.append(credit_val)
        print("SGPA for sem" + str(i) + ": " + str(sgpa_val))
    
    grades = np.concatenate(grades)
    credits = np.concatenate(credits)
    cgpa = np.dot(grades, credits) / credits.sum()
    
    print("SGPAs:", sgpas)
    print("CGPA:", cgpa)
    print("Time taken for all PDFs:", time.time() - start_time)

if __name__ == '__main__':
    asyncio.run(main())
