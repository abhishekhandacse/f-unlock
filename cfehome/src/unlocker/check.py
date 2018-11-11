import subprocess

result = subprocess.check_output("python face_comparison.py",universal_newlines=True, shell=True)
print(result)