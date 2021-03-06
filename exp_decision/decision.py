# -*- coding: utf-8 -*-

import os, time, re, urllib
from PIL import Image
import logging
from subprocess import check_output 

 
def main():
    baseline = str(check_output("ls", shell=True).decode()).strip().split()
    image_filepath1 = '1.jpg'
    image_filepath2 = '2.jpg'
    begin_similarty_compare(image_filepath1,image_filepath2)

def begin_similarty_compare(image_filepath1,image_filepath2):
    t1=time.time()
    similarity = image_similarity_vectors_via_numpy(image_filepath1,image_filepath2)
    duration = "%0.1f"%((time.time() - t1)*1000)
    print("image_similarity_vectors_via_numpy => %s took %s ms"%(similarity,duration ))
    if (similarity > 0.70):
        check_output("mutt -s 'insider detect alert' lonelywave_@gmail.com < ./alert.txt", shell=True)
    print("Comparing images finished")

 
def image_similarity_bands_via_numpy(filepath1, filepath2):
    import math
    import operator
    import numpy
    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)
 
    # create thumbnails - resize em
    image1 = get_thumbnail(image1)
    image2 = get_thumbnail(image2)
    
    # this eliminated unqual images - though not so smarts....
    if image1.size != image2.size or image1.getbands() != image2.getbands():
        return -1
    s = 0
    for band_index, band in enumerate(image1.getbands()):
        m1 = numpy.array([p[band_index] for p in image1.getdata()]).reshape(*image1.size)
        m2 = numpy.array([p[band_index] for p in image2.getdata()]).reshape(*image2.size)
        s += numpy.sum(numpy.abs(m1-m2))
    return s
 
def image_similarity_histogram_via_pil(filepath1, filepath2):
	from PIL import Image
	from six.moves import reduce
	import math
	import operator
	
	image1 = Image.open(filepath1)
	image2 = Image.open(filepath2)

	image1 = get_thumbnail(image1)
	image2 = get_thumbnail(image2)

	h1 = image1.histogram()
	h2 = image2.histogram()

	rms = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
	return rms
 
def image_similarity_vectors_via_numpy(filepath1, filepath2):
    # source: http://www.syntacticbayleaves.com/2008/12/03/determining-image-similarity/
    # may throw: Value Error: matrices are not aligned . 
    import PIL.Image
    from numpy import average, linalg, dot
    import sys
    
    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)
 
    image1 = get_thumbnail(image1, stretch_to_fit=True)
    image2 = get_thumbnail(image2, stretch_to_fit=True)
    
    images = [image1, image2]
    vectors = []
    norms = []
    for image in images:
        vector = []
        for pixel_tuple in image.getdata():
            vector.append(average(pixel_tuple))
        vectors.append(vector)
        norms.append(linalg.norm(vector, 2))
    a, b = vectors
    a_norm, b_norm = norms
    # ValueError: matrices are not aligned !
    res = dot(a / a_norm, b / b_norm)
    return res
 
def image_similarity_greyscale_hash_code(filepath1, filepath2):
    # source: http://blog.safariflow.com/2013/11/26/image-hashing-with-python/
 
    image1 = Image.open(filepath1)
    image2 = Image.open(filepath2)
 
    image1 = get_thumbnail(image1, greyscale=True)
    image2 = get_thumbnail(image2, greyscale=True)
    
    code1 = image_pixel_hash_code(image1)
    code2 = image_pixel_hash_code(image2)
    # use hamming distance to compare hashes
    res = hamming_distance(code1,code2)
    return res
    
def image_pixel_hash_code(image):
    pixels = list(image.getdata())
    avg = sum(pixels) / len(pixels)
    bits = "".join(map(lambda pixel: '1' if pixel < avg else '0', pixels))  # '00010100...'
    hexadecimal = int(bits, 2).__format__('016x').upper()
    return hexadecimal
 
def hamming_distance(s1, s2):
    len1, len2= len(s1),len(s2)
    if len1!=len2: 
        "hamming distance works only for string of the same length, so i'll chop the longest sequence"
        if len1>len2:
            s1=s1[:-(len1-len2)]
        else:
            s2=s2[:-(len2-len1)]
    assert len(s1) == len(s2)
    return sum([ch1 != ch2 for ch1, ch2 in zip(s1, s2)])
 
def get_thumbnail(image, size=(128,128), stretch_to_fit=False, greyscale=False):
    " get a smaller version of the image - makes comparison much faster/easier"
    if not stretch_to_fit:
        image.thumbnail(size, Image.ANTIALIAS)
    else:
        image = image.resize(size); # for faster computation
    if greyscale:
        image = image.convert("L")  # Convert it to grayscale.
    return image
 
def mkdir_p_filepath(path):
    dirpath = os.path.dirname(os.path.abspath(path))
    mkdir_p(dirpath)
 
def mkdir_p(path):
    import errno
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
 
def get_filename(path): 
    # cross plattform filename from a given path
    # source: http://stackoverflow.com/questions/8384737/python-extract-file-name-from-path-no-matter-what-the-os-path-format
    import ntpath
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
 
 
if __name__ == "__main__":
    main()
