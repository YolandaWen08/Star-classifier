import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import numpy as np    
from astropy.io import fits


def classify_star(filename):
    a=filename
    starType={'spDR2-000.fit':'O','spDR2-001.fit':'O/B','spDR2-002.fit':'B','spDR2-003.fit':'A',
             'spDR2-004.fit':'A','spDR2-005.fit':'F/A','spDR2-006.fit':'F','spDR2-007.fit':'F',
             'spDR2-008.fit':'G','spDR2-009.fit':'G','spDR2-010.fit':'K','spDR2-011.fit':'M1',
             'spDR2-012.fit':'M3','spDR2-013.fit':'M5','spDR2-014.fit':'M8','spDR2-015.fit':'L1',
    }
    path1='' # add the file path of your template
    path=''# add the file path of your stars spectra
    sci=fits.open(path+a)

    fluxTarget = sci[1].data['flux']*1e-17  
    waveTarget = 10**sci[1].data['loglam']   

    minx=999999999999
    bestChi=99999999999
    for i in range(0,15):
        if i==0:
            print('loading...')
        minx=99999999999
        b=f'spDR2-0{i:02d}.fit'
        template = fits.open(path1+b)  
        flux = template[0].data[0, :] * 1e-17    
        wave = 10**template[0].header['CRVAL1'] + np.arange(len(flux))*10**template[0].header['CD1_1']    
        try: 
            wave *= 1/(1 + template[0].header['Z'])
        except: 
            wave *= 1
    
        vrange=np.linspace(-1000,1000,600)
        for v in vrange:
            waveChange=wave * (1 + (v) / 299792.458)
            nrange=np.logspace(-3,3,600,5)
            for n in nrange:
                if np.min(waveChange)<=np.min(waveTarget):
                    minWave=np.min(waveTarget)
                else:
                    minWave=np.min(waveChange)
                if np.max(waveChange)<=np.max(waveTarget):
                    maxWave=np.max(waveChange)
                else:
                    maxWave=np.max(waveTarget)
                mask=(waveTarget>=minWave)&(waveTarget<=maxWave)
                waveCut=waveTarget[mask]
                fluxCut=fluxTarget[mask]
                fluxChange=np.interp(waveCut,waveChange,flux)*n
                chicurrent=abs(np.sum(((fluxCut-fluxChange)**2)/fluxCut))
                if(chicurrent<minx):
                    minx=chicurrent
                    fluxBest=flux
                    waveBest=waveChange
                    bestn=n
        if(minx<bestChi):
            bestChi=minx
            bestTemp=b
            wave2=waveBest
            flux2=fluxBest
            supern=bestn
    return starType[bestTemp]
    