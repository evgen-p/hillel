from datetime import datetime
import argparse
import boto3
import requests
import time

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--paragraph", help="Number of paragraphs to request", type = int)
    parser.add_argument("--s3", help="Upload result to S3 bucket", action="store_true")
    args = parser.parse_args()
    if not args.paragraph or args.paragraph < 5:
        par_count = int(input("Enter number of paragpaphs (at least 5): "))
        if par_count < 5:
            print("Less then 5 paragraph requested, force set number of paragraph to 5!")
            par_count = 5
        args.paragraph = par_count
    return (args.paragraph, args.s3)

def save_to_file(p_count:int, data:list):
    today = datetime.now()
    filename = str(int(time.time())) + ".res"

    with open(filename, "w") as open_file:
        open_file.write(f"Author: Yevhen.P {today}\n")
        open_file.write(f"Total pancettas count: {p_count}\n")
        open_file.write('\n'.join(data))
    return filename

def upload_to_s3(bucket_name:str, filename:str):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(filename, bucket_name, 'lesson14/'+filename)
    print(f"File uploaded to {bucket_name}/lesson14/{filename}")


(par_count, s3) = get_args()

url = f"https://baconipsum.com/api/?paras={par_count}&type=meat-and-filler"
r = requests.get(url)

res = r.json()[::-1]

pancetta_count = 0
for par in res:
    if 'Pancetta' in par or 'pancetta' in par:
        pancetta_count += 1

filename = save_to_file(pancetta_count, res)
print(f'Result saved to file: {filename}')

if s3:
    upload_to_s3("yevhen-hillel-homework", filename)
else:
    print("File saved only local")
