import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import scipy.optimize as spopt
import scipy.fftpack as spfft
import scipy.ndimage as spimg
import cvxpy as cvx
from scipy import linalg, optimize
import lbfgs as lb
from PIL import Image

def dct2(x):
	return spfft.dct(spfft.dct(x.T, norm = 'ortho', axis =0).T, norm = 'ortho', axis = 0)

def idct2(x):
	return spfft.idct(spfft.idct(x.T, norm='ortho', axis =0 ).T, norm = 'ortho', axis =0 )



def evaluate(x, g, step):
	"""An in-memory evaluation callback."""

	# we want to return two things:
	# (1) the norm squared of the residuals, sum((Ax-b).^2), and
	# (2) the gradient 2*A'(Ax-b)

	# expand x columns-first
	x2 = x.reshape((nx, ny)).T

	# Ax is just the inverse 2D dct of x2
	Ax2 = idct2(x2)

	# stack columns and extract samples
	Ax = Ax2.T.flat[ri].reshape(b.shape)

	# calculate the residual Ax-b and its 2-norm squared
	Axb = Ax - b
	fx = np.sum(np.power(Axb, 2))

	# project residual vector (k x 1) onto blank image (ny x nx)
	Axb2 = np.zeros(x2.shape)
	Axb2.T.flat[ri] = Axb # fill columns-first

	# A'(Ax-b) is just the 2D dct of Axb2
	AtAxb2 = 2 * dct2(Axb2)
	AtAxb = AtAxb2.T.reshape(x.shape) # stack columns

	# copy over the gradient vector
	np.copyto(g, AtAxb)

	return fx

# fractions of the scaled image to randomly sample at
sample_sizes = (0.001, 0.001)

# Read in the image as an array of array of array.
# The lowest element is the RGB value. The array is NxMxRGB, where N and M are size of pixels in pic.
Xorig = spimg.imread('C:\\Users\\adehghankooshkghazi\\Desktop\\DevelopmentV2\\SandBox\\CpmSens\\test.jpg')

# Get the dimentions of the data, ncahn would be three, since it is RGB
ny,nx,nchan = Xorig.shape

"""
Create two lists. Z and masks.
Both are of length 2, for each smaple size, and each element is a NxMXRGB.
so, z --> [MxNxRGB , NxMxRGB]
of all zeros.
"""
Z = [np.zeros(Xorig.shape, dtype='uint8') for s in sample_sizes]
masks = [np.zeros(Xorig.shape, dtype='uint8') for s in sample_sizes]


for i,s in enumerate(sample_sizes):
	# create random sampling index vector
	k = round(nx * ny * s)
	ri = np.random.choice(nx * ny, k, replace=False) # random sample of indices
	print(ri)

	# for each color channel
for j in range(nchan):

	# extract channel
	X = Xorig[:,:,j].squeeze()

	# create images of mask (for visualization)
	Xm =   np.zeros(X.shape)
	Xm.T.flat[ri] = X.T.flat[ri]
	masks[i][:,:,j] = Xm

	# take random samples of image, store them in a vector b
	b = X.T.flat[ri].astype(float)

	# perform the L1 minimization in memory
	##Xat2 = owlqn(nx*ny, evaluate, None, 5)
	x0 = np.ones(X.shape);
	Xat2 = lb.fmin_lbfgs(evaluate, x0,args =(5,),orthantwise_c=5, line_search='wolfe')
	#Xat2 = lb.fmin_lbfgs(
	#Xat2 = lb.fmin_lbfgs(evaluate, x0, orthantwise_c = 5)
	# transform the output back into the spatial domain
	Xat = Xat2.reshape(nx, ny).T # stack columns
	Xa = idct2(Xat)
	#Create an RGB Image
	Z[i][:,:,j] = Xa.astype('uint8')
	rgbArray = np.zeros((ny,nx,3),'uint8')
	rgbArray[..., 0] = Z[1][:,:,0]
	rgbArray[..., 1] = Z[1][:,:,1]
	rgbArray[..., 2] = Z[1][:,:,2]
	img = Image.fromarray(rgbArray)

	rgbMask = np.zeros((ny,nx,3), 'uint8')
	rgbMask[...,0] = masks[1][:,:,0]
	rgbMask[...,1] = masks[1][:,:,1]
	rgbMask[...,2] = masks[1][:,:,2]
	
f, ax = plt.subplots(1, 3, figsize=(14, 4))
ax[0].imshow(Xorig, cmap='hot', interpolation='none')
plt.title('Original')
ax[1].imshow(rgbMask, cmap='gray', interpolation='none')
plt.title('Randomly Sampled')
ax[2].imshow(img, cmap='hot', interpolation='none')
plt.title('Reconstructed')
plt.show()
