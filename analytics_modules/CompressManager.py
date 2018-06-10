import numpy as np;
import matplotlib as mpl;
import matplotlib.pyplot as plt;
import scipy.optimize as spopt;
import scipy.fftpack as spfft;
import scipy.ndimage as spimg;
import cvxpy as cvx;
from scipy import linalg, optimize;
import scipy;
import lbfgs as lb;
from PIL import Image;
import sys, os;


nx = None;
ny = None;
b = None;
ri = None;

def dct2(x):
	return spfft.dct(spfft.dct(x.T, norm = 'ortho', axis =0).T, norm = 'ortho', axis = 0)

def idct2(x):
	return spfft.idct(spfft.idct(x.T, norm='ortho', axis =0 ).T, norm = 'ortho', axis =0 )

def evaluate(x, g, step):
	x2 = x.reshape((nx, ny)).T
	Ax2 = idct2(x2)
	Ax = Ax2.T.flat[ri].reshape(b.shape)
	Axb = Ax - b
	fx = np.sum(np.power(Axb, 2))
	Axb2 = np.zeros(x2.shape)
	Axb2.T.flat[ri] = Axb
	AtAxb2 = 2 * dct2(Axb2)
	AtAxb = AtAxb2.T.reshape(x.shape)
	np.copyto(g, AtAxb)
	return fx
	

def Compress(input_FileName, input_Sample_x, input_Sample_y):
	try:
		global nx;
		global ny;
		global b;
		global ri;
		sample_sizes = (float(input_Sample_x), float(input_Sample_y))
		base_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'web/UploadFiles/'));
		base_path_save = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'web/static/images/SaveFiles/'));
		Xorig = spimg.imread(base_path+"/"+input_FileName+'.jpg')
		ny,nx,nchan = Xorig.shape
		Z = [np.zeros(Xorig.shape, dtype='uint8') for s in sample_sizes]
		masks = [np.zeros(Xorig.shape, dtype='uint8') for s in sample_sizes]
		for i,s in enumerate(sample_sizes):
			k = round(nx * ny * s)
			ri = np.random.choice(nx * ny, k, replace=False)
			for j in range(nchan):
				X = Xorig[:,:,j].squeeze()
				Xm =   np.zeros(X.shape)
				Xm.T.flat[ri] = X.T.flat[ri]
				masks[i][:,:,j] = Xm
				b = X.T.flat[ri].astype(float)
				x0 = np.ones(X.shape);
				Xat2 = lb.fmin_lbfgs(evaluate, x0, args =(5,), orthantwise_c=5, line_search='wolfe')
				Xat = Xat2.reshape(nx, ny).T
				Xa = idct2(Xat)
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
		scipy.misc.imsave(base_path_save+"/"+input_FileName+'_original.jpg', Xorig);
		scipy.misc.imsave(base_path_save+"/"+input_FileName+'_compressed.jpg', rgbMask);
		scipy.misc.imsave(base_path_save+"/"+input_FileName+'_recovered.jpg', img);
		return True;
	except Exception as e:
		return False;


# if __name__=="__main__":
# 	Compress("Test",0.1,0.1)