
**The directory originization**  
ETL-master/  
----processed_data/  
----saved_embeddings/my/none.txt  
----code_name1.py  
----code_name2.py 

**0. Data preparation:**  
Download the processed data files from Google drive: https://drive.google.com/drive/folders/1oIABLZE0UcEylLwiJrWY5R3rw7t739Zz?usp=sharing   

**1. Requirements:**  
python3.5; pytorch=1.4.0; tqdm=4.27.0; tensorboardX=1.8; pandas=0.25; numpy=1.15; networkx=2.2; logger=1.4; scipy=1.1; scikit-learn=0.20   

**2.Runing commands**  
Run the codes with the following commands on different datasets (amazon means "Movie & Book", amazon2 means "Movie & Music" and amazon3 means "Music & Book").  

-->on Movie & Book dataset: 
CUDA_VISIBLE_DEVICES=gpu_num python main_my.py --dataset=amazon --reg=5.0  

-->on Movie & Music dataset:  
CUDA_VISIBLE_DEVICES=gpu_num python main_my.py --dataset=amazon2 --reg=0.5  

-->on Music & Book dataset:  
CUDA_VISIBLE_DEVICES=gpu_num python main_my.py --dataset=amazon3 --reg=1.0  


