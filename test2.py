from process_details import sgpa
import numpy as np
import time
import concurrent.futures

grades = []
credits = []
sgpas = []

def process_semester(sem_number):
    sgpa_obj = sgpa("sem" + str(sem_number) + "a.pdf")
    sgpa_obj.perform_ocr()
    sgpa_obj.calculate_sgpa()
    return sgpa_obj.sgpa, sgpa_obj.grades, sgpa_obj.credits

if __name__ == '__main__':
        
        start_time = time.time()

        # Using ProcessPoolExecutor to process semesters concurrently
        with concurrent.futures.ProcessPoolExecutor() as executor:
            # Submit tasks for each semester
            future_to_semester = {executor.submit(process_semester, i): i for i in range(1, 6)}
            for future in concurrent.futures.as_completed(future_to_semester):
                sem_number = future_to_semester[future]
                try:
                    sgpa_val, grade_val, credit_val = future.result()
                    sgpas.append(sgpa_val)
                    grades.append(grade_val)
                    credits.append(credit_val)
                    print("SGPA for sem" + str(sem_number) + ": " + str(sgpa_val))
                except Exception as e:
                    print(f"Exception occurred for sem{sem_number}: {e}")

        # Combine lists of grades and credits
        grades = np.concatenate(grades)
        credits = np.concatenate(credits)
        cgpa = np.dot(grades, credits) / credits.sum()

        print(sgpas)
        print(cgpa)
        print("Time taken for all pdfs: " + str(time.time() - start_time))
