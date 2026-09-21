### Star-classifier
<p>The star-classifier is a code to classify stars based on MK system.</p>

## How to use the classifier

Before applying the code, you have to download the template.

To use the code to classify stars, the only thing you need to get is the FITS file of the spectrum of a star. In order to allow the code to fit your spectrum, it is better to get a spectrum from the Sloan Digital Sky Survey. 

https://skyserver.sdss.org/dr20/

To search for a specific star, you can use ‘navigate’ to locate a star (make sure it’s a star but not a galaxy) or use ‘explore’ to search for name, location and spectrum ID. Then, click the ‘optical spectra to down load the FITS document.(The process is also shown in the document)
Then import the package 
```
from stellar_classifier import classify_star
```
Using the function classify_star("star spectrum") to classify the star.
For example,
```
from stellar_classifier import classify_star
result = classify_star("spec-1895-53242-0338.fits")
print(result)
```


## The principle and the outcome of the code

Spectral classification, sometimes referred to as stellar classification, is a general term for the sorting of stars based on their spectral information (Maiz et al., 2024). By examining a star’s spectrum, we can estimate the basic properties, including temperature, luminosity, velocity, and so on, thus classifying them into different types. The widely used Morgan-Keenan System (MK system) classifies stars primarily according to their temperature, and later, scientists added numerical indicators of luminosity and temperature to the system. The MK system divides stars into seven classes — O, B, A, F, G, K, and M—from hottest to coldest. Over time, additional classes have been added to the MK system, such as L and T, which correspond to even cooler stars (Campbell, Josephine, 2022). As people discovered more and more stars, it became difficult to classify each star by hand. Therefore, I wrote code to sort them into 16 classes based on their spectrum.

The classification uses the spectral cross-correlation templates released by SDSS as a classification reference. The first sixteen templates are based on the MK system, First, the dictionary is composed of 23 classes of stars. The first sixteen stars are classified by the MK system, and some of them are transition stars, such as F/A stars. The remaining are magnetic white dwarfs, carbon stars, white dwarfs, and low-metallicity K subdwarfs.(In this classification process, only the first 16 templates will be used)

The second part is for reading the spectrum of the star that is intended to be classified. These are labeled as fluxTarget and waveTarget. 

The third and most crucial section is matching. The principle is finding the minimum chi-square between the star spectrum and the template spectrum. It is composed of three loops. The outer loop is for grid searching every template. The first inner loop is for Doppler shift correction. When the star isn’t stationary relative to the observer, the wavelength changes. To correct this effect, we have to adjust the wavelength. The second inner loop is for normalization. Spectral normalization is a process that adjusts the amplitude of a signal's frequency spectrum to a common scale (Lee, 2025). This allows the comparison between spectra at roughly the same luminosity level. For each pair of velocity and normalization, the code will calculate the chi-square and label the smallest chi-square for each template. The chi-square measures the difference between the real data and the interpolated data on the spectrum. But the ranges of the wave aren’t the same for the template and the real data; the code restricts the wave range so that the two ranges overlap. Lastly, the best template and the normalization parameter corresponding to the minimum chi-square will be noted down.

Finally, the code will print the result, which will be a type of star. The result may not perfectly correspond to the one in SDSS. This doesn’t mean the result is wrong. Instead, some stars are classified as a different type of star in SDSS. For instance, the star with SpecObjID 2455678465655990272 is classified as F9 and K0. But the code classifies it as G type. This may relate to the effective temperature of stars. The teff of this star is 5397.525, which typically lies in the range of G star, which might influence the spectrum, leading to a different result. Moreover, the type G is close to F9, so the various results may be caused by the transition stage between two spectral types.

Since the code classifies stars only based on their spectrum, the results are not perfect, as exemplified. In the future, I plan to add effective temperature, absorption lines, metallicity, and other elements into the classification process.
