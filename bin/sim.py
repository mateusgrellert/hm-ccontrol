import os
from joblib import Parallel, delayed  
import multiprocessing

def geraSim(cfg, seq, qp):
	setup_cfg = '_'.join([cfg, seq, qp])
	cmd = './TAppEncoderStatic -c ../cfg/' + cfg + '.cfg -c ../cfg/per-sequence/' + seq + '.cfg --QP=' + qp + ' > '+setup_cfg+'.out'
	os.system(cmd)


sequences = ['BasketballDrill','BasketballDrillText','BasketballDrive','BasketballPass','BlowingBubbles','BQMall','BQSquare','BQTerrace','Cactus','ChinaSpeed','FourPeople','Johnny','Kimono','KristenAndSara','ParkScene','PartyScene','PeopleOnStreet', 'RaceHorses','RaceHorsesC','SlideEditing','SlideShow','Traffic']
cfgs = ['encoder_lowdelay_main']
qps = ['22','27','32','37']



output_vet = []

num_cores = 4

for cfg in cfgs:
	for qp in qps:
		Parallel(n_jobs=num_cores)(delayed(geraSim)(cfg, seq, qp) for seq in sequences)


