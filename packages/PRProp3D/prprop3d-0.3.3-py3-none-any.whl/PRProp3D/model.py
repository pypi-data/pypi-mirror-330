import torch

# Check if CUDA (GPU support) is available
if torch.cuda.is_available():
    import cupy as cp  
    from cupyx.scipy.ndimage import zoom, gaussian_filter
    from cupyx.scipy.signal.windows import tukey
    processor = "gpu"
    print("Running on GPU")
else:
    print("No GPU detected, Running on CPU.")
    import numpy as cp #all references to cp will be aliases to np
    from scipy.ndimage import zoom, gaussian_filter
    from scipy.signal.windows import tukey
    processor = "cpu"

import numpy as np

import time
from tqdm import tqdm


#general classes
class Dict2Class(object):
  def __init__(self, my_dict):
    for key in my_dict:
        setattr(self, key, my_dict[key])

class NewClass(object): pass


class Beam: #individual beam characteristics  ###required
  def genrot(self,rlen,refin,thout,phi,x,y): # Add self as the first argument
    """

    Args:
      rlen: crystal length (um)
      thout: beam input polar angle radians, 0 for normal incidence
      phi: beam azimuth, zero for beam in xz plane
      x: crystal coordinates array 1D float
      y: crystal coordinates array 1D float

    Returns: rotated coordinates xp,yp,zp 1D arrays used in beam generator gaus

    """
    #generate coordinate frames rotated by input angles
    xs=len(x)
    ys=len(y)
    xp=cp.zeros((xs,ys))
    yp=cp.zeros((xs,ys))
    zp=cp.zeros((xs,ys))
    el=rlen/2.0 #half interaction length
    #el=0  ###soliton
    th=cp.arcsin(cp.sin(thout)/refin) #internal propagation angle
    sP=cp.sin(phi)
    cP=cp.cos(phi)
    st=cp.sin(th)
    ct=cp.cos(th)
    s2p=2*sP*cP
    c2p=cP**2-sP**2
    xp=x[:,None]+cP*(1-ct)*(-x[:,None]*cP+y[None,:]*sP)-el*cP*st
    yp=y[None,:]+sP*(1-ct)*(x[:,None]*cP-y[None,:]*sP)+el*sP*st
    zp=(-el)*ct+(-x[:,None]*cP+y[None,:]*sP)*st
    return xp,yp,zp

  def __init__(self,prdata,beam_no,w0,th,phi):
    self.w0=w0
    self.th=th
    self.phi=phi
    lm=prdata.lm
    refin=prdata.refin
    rlen=prdata.rlen
    transp=prdata.image_on_beam
    x=cp.linspace(-prdata.xaper/2,prdata.xaper/2,prdata.xsamp,endpoint=False)
    y=cp.linspace(-prdata.yaper/2,prdata.yaper/2,prdata.ysamp,endpoint=False)

    if beam_no == 1:
      self.transp=transp=='Beam 1'or transp=='Beams 1 & 2'
    elif beam_no == 2:
      self.transp=transp=='Beam 2'or transp=='Beams 1 & 2'
    self.coord=cp.asarray(self.genrot(rlen,refin,th,phi,x,y)) 

class Derived: #derived attributes and their functions ###required

  def gaus(self,prdata,beam):
      """

      Args:
        x: input angle rotated x coordinate 1D array
        y: input angle rotated y coordinate 1D array
        z: input angle rotated z coordinate 1D array
        beam: beam number: 2 is pump for 2 beam coupling, 1 for beam 1 signal
        arrin: scaled input image 2D array
        w0x: beam waist in x
        w0y: beam waist in y

      Returns: amp: complex beam amplitude array

      """
      #apply image to gaussian beam focussing at longitudinal center of crystal
      # if called for by value in variable transp
      #x,y,z rotated coordinates, beam = beam number 1 or 2
      #w0x beam waist in x direction
      lm=prdata.lm
      refin=prdata.refin
      arrin=prdata.arrin
      xsamp=prdata.xsamp ; ysamp=prdata.ysamp
      x,y,z=beam.coord  #rotated
      w0x=beam.w0
      w0y=beam.w0
      transp=beam.transp
      #coord=self.coord
      kin=refin*2*cp.pi/lm # wavenumber of beam inside crystal
      z0x=w0x**2*kin/2.0
      z0y=w0y**2*kin/2.0
      eta=(cp.arctan(z/z0x)+cp.arctan(z/z0y))/2
      #inverse radii of curvature
      rlxinv=z/(z**2+z0x**2)
      rlyinv=z/(z**2+z0y**2)
      #rlxinvmn=rlen/(rlen**2+z0x**2) #mean inverse radius of curvature
      wl2x=w0x**2*(1.0+(z/z0x)**2)
      wl2y=w0y**2*(1.0+(z/z0y)**2)
      wlxy=cp.sqrt((1.0+(z/z0x)**2)*(1.0+(z/z0y)**2))
      argx = (x**2)*(1.0/wl2x-1j*kin*rlxinv/2.0)
      argy = (y**2)*(1.0/wl2y-1j*kin*rlyinv/2.0)
      arg=argx+argy
      # w0x<0 is a switch for plane wave input
      if w0x > 0:
        amp1 = cp.exp(-arg+1j*kin*z-1j*eta)/cp.sqrt(wlxy)
      else:
        amp1 = cp.exp(+1j*kin*z)
      transp=beam.transp
      #apply data as phase transparency if false
      phasetransp=prdata.image_type=="phase image"  
      # beam may have the data transparency imposed
      if transp:
        #find beam centers
        lenx,leny=cp.shape(arrin)
        #find beam centers where xp and yp are zero
        xindex1,yindex1=cp.unravel_index(cp.argmin(x**2+y**2),(xsamp,ysamp))
        #xindex1,yindex1=getx0y0(coord)
        # avoidimage magnification taking arrays out of bounds
        ampxlo=max(xindex1-lenx//2,0)
        ampylo=max(yindex1-leny//2,0)
        ampxhi=min(xindex1+lenx//2,xsamp-1)
        ampyhi=min(yindex1+leny//2,ysamp-1)
        arrxlo=lenx//2-(xindex1-ampxlo)
        arrxhi=lenx//2+ampxhi-xindex1
        arrylo=leny//2-(yindex1-ampylo)
        arryhi=leny//2+ampyhi-yindex1
        if not phasetransp:
          amp1[ampxlo:ampxhi,ampylo:ampyhi] \
            = cp.sqrt(arrin[arrxlo:arrxhi,arrylo:arryhi]) \
            *amp1[ampxlo:ampxhi,ampylo:ampyhi]
        else:
          amp1[ampxlo:ampxhi,ampylo:ampyhi] \
            = cp.exp(1j*cp.pi*arrin[arrxlo:arrxhi,arrylo:arryhi]) \
            *amp1[ampxlo:ampxhi,ampylo:ampyhi]
      return amp1

  def a(self,prdata,beam1,beam2):
    """

    Args:
      arrin: scaled input image 2D array
      coord1: rotated coordinates for beam 1 2D array
      coord2: rotated coordinates for beam 2 2D array
    Returns: full input field amplitude

    """
    imtype=prdata.image_type
    rat=prdata.rat
    arrin=prdata.arrin

    # beam contributions from beam ratio
    a1r=cp.sqrt(1.0/(1.0+rat))
    a2r=cp.sqrt(rat/(1.0+rat))
    # for the moment the beams have equal waists in x and y
    # generate beams 1 and 2
    amp1=self.gaus(prdata,beam1)
    amp2=self.gaus(prdata,beam2)
    # add them according to beam ratio
    atot=a1r*amp1+a2r*amp2
    return atot
  def __init__(self,prdata,beam1,beam2):
    xaper=prdata.xaper
    yaper=prdata.yaper
    xsamp=prdata.xsamp
    ysamp=prdata.ysamp
    lm=prdata.lm
    NT=prdata.NT
    epsr=prdata.epsr
    eps0=8.85e-12
    kB=1.38e-23
    T=prdata.T
    qq=1.6e-19
    k0=qq*cp.sqrt(NT/(epsr*eps0*kB*T))*1e-6
    Es=qq*NT/(epsr*eps0*k0*1e6)
    fx=cp.fft.fftfreq(xsamp,xaper/xsamp)   ####np
    fy=cp.fft.fftfreq(ysamp,yaper/ysamp)   ####np
    fxy2=fx[:,None]**2+fy[None,:]**2
    fx1=-cp.cos(beam1.phi)*cp.sin(beam1.th)/lm
    fy1=cp.sin(beam1.phi)*cp.sin(beam1.th)/lm
    fx2=-cp.cos(beam2.phi)*cp.sin(beam2.th)/lm
    fy2=cp.sin(beam2.phi)*cp.sin(beam2.th)/lm
    mask1=cp.zeros((xsamp,ysamp))
    DF1=(fx[:,None]-fx1)**2+(fy[None,:]-fy1)**2
    DF2=(fx[:,None]-fx2)**2+(fy[None,:]-fy2)**2
    mask1=cp.where(DF1<=DF2,1,0)
    windowedge=prdata.windowedge
    refin=prdata.refin

    dz=prdata.dz
    windowx = tukey(xsamp,alpha=windowedge,sym=False)
    windowy = tukey(ysamp,alpha=windowedge,sym=False)
    windowx = cp.asarray(windowx)
    windowy = cp.asarray(windowy)
    windowxy = cp.sqrt(cp.outer(windowx,windowy))
    windowxy=cp.asarray(windowxy)
    niter=int(prdata.rlen/prdata.dz)
    batchnum=prdata.batchnum_spec #specified number of batches
    use_cons_tsteps=prdata.use_cons_tsteps
    tend=prdata.tend
    time_behavior=prdata.time_behavior
    tsteps=prdata.tsteps
    image_type=prdata.image_type
    kmax=2*cp.pi*fx[xsamp//2-1]/k0
    batchsize=niter//batchnum
    if use_cons_tsteps:
      deltat=1/4/kmax**2
    else:
      deltat=tend/tsteps
    self.deltat=deltat
    if time_behavior=="Static":
      self.tsteps=1
    else:
      self.tsteps=int(cp.round(tend/deltat/4))*4 # make sure number of time steps is divisible by 4

    self.niter=niter
    self.x=cp.linspace(-xaper/2,xaper/2,xsamp,endpoint=False)
    self.y=cp.linspace(-yaper/2,yaper/2,ysamp,endpoint=False)
    self.fx=fx
    self.fy=fy
    self.fxy2=fxy2
    self.kx = 2*cp.pi*(cp.tile(fx,(ysamp,1)).T)/k0
    self.k0=qq*cp.sqrt(NT/(epsr*eps0*kB*T))*1e-6
    self.Es=qq*NT/(epsr*eps0*k0*1e6)
    self.E_0=prdata.E_app*1000*100/Es
    self.seeds=cp.random.randint(0,2**32-1,size=niter).tolist()
    self.batchsize=batchsize # number of xy planes in each batch
    self.nbatches=niter//batchsize  #actual number of batches that will fit in niter dz steps
    self.h=cp.where((lm/refin)**2*(fxy2)<1.0,
        cp.exp(2.0j*cp.pi*refin*dz/lm*cp.sqrt(1-(lm/refin)**2*(fxy2))),0)
    self.windowxy=windowxy
    self.amp0=self.a(prdata,beam1,beam2)
    self.kout=2*cp.pi/lm
    self.mask1=cp.fft.fftshift(mask1)  ####np

    #functions required by the propagator
class Nlo:
  def dn_pr_s(self,**kwargs):
    #simple steady state space charge field
    amp=kwargs['amp']
    prdata=kwargs['prdata']
    dv=kwargs['derived']

    lm=prdata.lm
    gl=prdata.gl
    rlen=prdata.rlen
    k0=dv.k0
    kx=dv.kx
    id=prdata.Id
    intens2=abs(amp)**2+id
    id=1+id #current edge background intensity
    kg=2*cp.pi*(cp.sin(beam1.th)-cp.sin(beam2.th))/lm
    ks=kg*cp.sign(kx)/k0
    E_0=dv.E_0
    dn_0=dv.E_0*2*gl/(rlen*2*cp.pi/lm)
    Ik=cp.fft.fft(intens2,axis=0)
    dnft=(1j*ks*Ik)/id/(1+E_0*1j*ks+ks**2)*2*gl/(rlen*2*cp.pi/lm)
    dn=cp.real(cp.fft.ifft(dnft,axis=0))-dn_0
    #index array
    return dn

  def dn_pr_f(self,**kwargs):
    amp=kwargs['amp']
    prdata=kwargs['prdata']
    dv=kwargs['derived']

    id=prdata.Id
    lm=prdata.lm
    gl=prdata.gl
    E_0=dv.E_0
    rlen=prdata.rlen
    dn_0=dv.E_0
    kx=dv.kx
    intens2=abs(amp)**2+id
    if prdata.w01 < 0 or prdata.w02 < 0:
      id=1+id
    Ip=(cp.fft.ifft(1j*kx*cp.fft.fft(intens2,axis=0),axis=0))
    dnft=cp.fft.fft((E_0*id+Ip)/intens2,axis=0)/(1+E_0*1j*kx+kx**2)*2*gl/(rlen*2*cp.pi/lm)
    dn = cp.real(cp.fft.ifft(dnft,axis=0))
    return dn

  def dn_kerr(self,**kwargs):   ###simplified here in PRcoupler2
    """
    Simple Kerr nonlinearity
    Args:
      escsa: space charge field
      kout: optical wavenumber outside crystal (refractive index 1)
      kt: Kerr coefficient, perhaps thermal. Not tested

    Returns: nonlinear refactive index grating (2D real array)

    """
    amp=kwargs['amp']
    prdata=kwargs['prdata']

    intens2=abs(amp)**2+prdata.Id
    dn = prdata.kt*intens2*1e-3 #photorefractive index array
    return dn

  def dndt_s(self,**kwargs):   #amp,escsa,grid,xtal,beam1,Eplane
    """
    Time derivative of space charge field: simplified version linear in space
    charge field. For plane waves only. Not valid for applied fields
    Args:
      amp: optical amplitude 2D complex array
      fx: array of spatial frequencies to generate spatial derivatives in FT space
      k0: characteristic space charge wave number
      escsa: space charge field

    Returns: time derivative of space charge field

    """
    dn_in=kwargs['dn_in']
    amp=kwargs['amp']
    prdata=kwargs['prdata']
    dv=kwargs['derived']
    beam1=kwargs['beam1']
    beam2=kwargs['beam2']

    lm=prdata.lm
    gl=prdata.gl
    rlen=prdata.rlen
    k0=dv.k0
    kx=dv.kx
    id=prdata.Id
    intens2=abs(amp)**2+id
    id=1+id #current edge background intensity
    kg=2*cp.pi*(cp.sin(beam1.th)-cp.sin(beam2.th))/lm
    ks=kg*cp.sign(kx)/k0
    E_0=dv.E_0
    noe=2*gl/(rlen*2*cp.pi/lm)
    ib=1+id #current edge background intensity
    Ik=cp.fft.fft(intens2,axis=0)
    dn_ink=cp.fft.fft(dn_in,axis=0)
    dndt_outk =noe*E_0*ib + dn_ink*(1+1j*ks+ks**2)*ib+E_0*Ik*noe
    dn_out=cp.real(cp.fft.ifft(dndt_outk,axis=0))
    return dn_out

  def dndt_f(self,**kwargs):
    """
    Full theoretical time derivative of space charge field:
    Args:
      amp: optical amplitude 2D complex array
      fx:  array of spatial frequencies to generate spatial derivatives in FT space
      k0:  characteristic space charge wave number
      escsa: space charge field

    Returns: time derivative of space charge field

    """
    dn_in=kwargs['dn_in']
    amp=kwargs['amp']
    prdata=kwargs['prdata']
    dv=kwargs['derived']
    lm=prdata.lm
    gl=prdata.gl
    rlen=prdata.rlen
    rat=prdata.rat
    k0=dv.k0
    kx=dv.kx
    id=prdata.Id
    intens2=abs(amp)**2+id
    id=1+id #current edge background intensity
    E_0=dv.E_0
    noe=2*gl/(rlen*2*cp.pi/lm)
    ib=id
    if prdata.w01 < 0:
      ib=1/(1+rat)+id
    if prdata.w02 < 0:
      ib=ib+rat/(1+rat)
    Ip=cp.real(cp.fft.ifft(1j*kx*cp.fft.fft(intens2,axis=0),axis=0))
    dn_inft=cp.fft.fft(dn_in,axis=0)
    # Calculate transverse derivative of space charge field from previous step
    dn_inp=cp.real(cp.fft.ifft(1j*kx* dn_inft ,axis=0))
    # Calculate second derivative of space charge field from previous step
    dn_inpp=cp.real(cp.fft.ifft(-kx**2* dn_inft ,axis=0))
    dn_out = noe*E_0*ib-((dn_in*intens2-noe*Ip)*(1+dn_inp/noe)-dn_inpp*(intens2))
    return dn_out

def noisexy(m,prdata,seeds):
  """
  scattering noise in x and y directions
  Args:
    m:seed with which to generate scattering noise

  Returns: corrnoise1layer 2D float array

  """
  xsamp=prdata.xsamp ; ysamp=prdata.ysamp ; yaper=prdata.yaper
  xaper=prdata.xaper ; sigma=prdata.sigma ; eps=prdata.eps
  rlen=prdata.rlen ; dz=prdata.dz
  niter=int(rlen/dz)
  niter=int(rlen/dz)
  

  sigmax=sigma*xsamp/xaper
  sigmay=sigma*ysamp/yaper
  cp.random.seed(seeds[m])
  corrnoise1layer_a=cp.random.normal(loc=0,scale=cp.sqrt(eps/niter*4*cp.pi),size=(xsamp,ysamp))
  corrnoise1layer=gaussian_filter(corrnoise1layer_a,sigma=(sigmax,sigmay))*cp.sqrt(sigmax*sigmay)
  return corrnoise1layer

def gain(amp,prdata,derived)  :
  gainout=NewClass()
  amps=[[],[],[],[]]
  rat=prdata.rat
  gl=prdata.gl
  mask1=derived.mask1
  ampft=cp.fft.fft2(amp)
  amp0=derived.amp0
  amp0ft=cp.fft.fft2(amp0)
  ampm=cp.fft.ifft2(ampft*mask1)  #beam 1 intensity
  ampp=amp-ampm  #beam 2 intensity
  amp0p=cp.fft.ifft2(amp0ft*(1-mask1))  #positive spatial frequency input field (beam 2 spatial frequencies)  ####np
  amp0m=cp.fft.ifft2(amp0ft*mask1)  #negative spatial frequency input field ####np
  im0r=cp.sum(cp.sum(abs(amp0m)**2))/cp.sum(cp.sum(abs(amp0)**2)) # normalized beam 2 power
  ip0r=cp.sum(cp.sum(abs(amp0p)**2))/cp.sum(cp.sum(abs(amp0)**2)) # normalized beam 1 power
  imr=cp.sum(cp.sum(abs(ampm)**2))/cp.sum(cp.sum(abs(amp)**2)) # normalized beam 2 total power
  ipr=cp.sum(cp.sum(abs(ampp)**2))/cp.sum(cp.sum(abs(amp)**2)) # normalized beam 1 total power
  imr_norm=imr*(1+rat*cp.exp(2*gl)) #amplified beam 1 power normalized to plane wave steady state
    #gain calculated using plane wave formula
  gain=-cp.log(imr/im0r/(ipr/ip0r)) /2

  amps[0] = ampp
  amps[1] = ampm
  amps[2] = amp0p
  amps[3] = amp0m  
      
  return gain,amps

#platform independent realization

def setup(prdata,derived):
  xsamp=prdata.xsamp ; ysamp=prdata.ysamp
  niter=derived.niter
  skip=prdata.skip
  h=derived.h
  windowxy=derived.windowxy
  dz=prdata.dz
  lm=prdata.lm  
  noisetype=prdata.noisetype
  fxy2=derived.fxy2
  return xsamp,ysamp,niter,skip,h,dz,lm,noisetype,fxy2

def appender_ind(xstr,outputs,xout,xin):
  """
    time dependent beam propagation function
    Args:
      xstr: string representing desired sample eg 'dnxzt'
      outstr: list of requested outputs
      xin: sample to append

    Returns:
      xout: appended output in cpu    
  """   

  if xstr in outputs: 
    if 'xz' in xstr and 't' not in xstr: 
      if len(xout) == 0:
        xout=[xin[:,cp.shape(xin)[1]//2] ]
      else:
        xout = cp.append(xout,[xin[:,cp.shape(xin)[1]//2]],axis=0) 
    else:
      if len(xout) == 0:
        xout=[xin]
      else:
        xout = cp.append(xout,[xin],axis=0)   
  return xout
  

def propagate(prdict,outputs):
  """
  static beam propagation function
  Args:
    prdata: class containing run parameters such as gain, beam ratio etc.
    derived: class containing derived objects 
     such as the linear propagation kernel
    dn: function to calculate nonlinear refractive index change from intensity
    outputs: list of outputs to be returned. options are 'ampxz','dnxz'

  Returns:
    amp: complex output field
    output: class containing output data

  """
  prdata=Dict2Class(prdict)
  beam1=Beam(prdata,beam_no=1,w0=prdata.w01,th=prdata.thout1,phi=prdata.phi1)
  beam2=Beam(prdata,beam_no=2,w0=prdata.w02,th=prdata.thout2,phi=prdata.phi2)
  derived=Derived(prdata,beam1,beam2)
  xsamp,ysamp,niter,skip,h,dz,lm,noisetype,fxy2=setup(prdata,derived)
  
  #maybe multiple dn's
  output=NewClass()
  nlo=Nlo()
  if prdata.planewave:
    dn=nlo.dn_pr_s
  else:
    dn=nlo.dn_pr_f
  
  tic=time.time()
  if 'ampxz' in outputs: ampxz=[]
  if 'dnxz' in outputs: dnxz=[]
  amp=derived.amp0
  ampft=cp.fft.fft2(amp)
  windowxy=derived.windowxy
  fwindowxy=cp.fft.fftshift(windowxy) ####np
  #begin z propagation
  for i in range(niter):
      ampft=ampft*h*fwindowxy
      amp=cp.fft.ifft2(ampft)
      dn1=cp.zeros((xsamp,ysamp),dtype=float)
      #for j in range(len(dn)):
      dn1 = dn(amp=amp,prdata=prdata,derived=derived) #photorefractive index array
      amp=amp*cp.exp(-2j*cp.pi/lm*dn1*dz)*windowxy

      if noisetype=='volume xy':
        noise_xy=noisexy(i,prdata,derived.seeds)
        amp=amp*cp.exp(1j*noise_xy)

      ampft=cp.fft.fft2(amp)
      ampft=cp.where(lm**2*fxy2<1,ampft,0)

      #end of propagation step
      if i%skip == 0:
        
        ampxz=appender_ind('ampxz',outputs,ampxz,amp)
        dnxz=appender_ind('dnxz',outputs,dnxz,dn1)
        
        #if 'ampxz' in outputs: ampxz.append(amp[:,ysamp//2])
        #if 'dnxz' in outputs: dnxz.append(dn1[:,ysamp//2])


  if prdata.backpropagate:
    ampb=amp
    ampbft=cp.fft.fft2(ampb)
    for i in range(niter):
      ampbft=ampbft*cp.conj(h)
      ampb=cp.fft.ifft2(ampbft)*windowxy
    amp=ampb

  toc=time.time()

  print('elapsed time ',toc-tic)
  gainout,ampspm=gain(amp,prdata,derived)
  if processor == 'gpu':
    #if 'ampxz' in outputs:
    #  output.ampxz=cp.stack(ampxz).get()
    #if 'dnxz' in outputs:
    #  output.dnxz=cp.stack(dnxz).get()    
    derived.x=derived.x.get()
    derived.y=derived.y.get()
         
  #else:
    #if 'ampxz' in outputs:
    #  output.ampxz=cp.stack(ampxz)
    #if 'dnxz' in outputs:
    #  output.dnxz=cp.stack(dnxz)
      
  output.amps = ampspm
  output.gain=gainout
  return amp,derived,output


def propagate_t(prdict,outputs):
  #uses external cupy numpy, tqdm, time, cupyx.scipy.fft as spfft, cupy import NaN, scipy.signal.windows import tukey
  #uses internal setup, cl:prdata, cl:derived
  """
  time dependent beam propagation function
  Args:
    prdata: class containing run parameters such as gain, beam ratio etc.
    derived: class conatining derived objects
     such as the linear propagation kernel
    dndt: function to calculate time derivative of nonlinear refractive index
     change from intensity
    outputs: list of outputs to be returned. 
      options are 'ampxyt','dnxyt','ampxzt','dnxzt'

  Returns:
    amp: complex output field
    output: class containing output data including gaint, [timdependent gain
    dependent output intensity]

  """
  prdata=Dict2Class(prdict)
  abort=False
  outputs=outputs.copy()
  beam1=Beam(prdata,beam_no=1,w0=prdata.w01,th=prdata.thout1,phi=prdata.phi1)
  beam2=Beam(prdata,beam_no=2,w0=prdata.w02,th=prdata.thout2,phi=prdata.phi2)
  derived=Derived(prdata,beam1,beam2)
  xsamp,ysamp,niter,skip,h,dz,lm,noisetype,fxy2=setup(prdata,derived)
  output=NewClass()
  nlo=Nlo()
  if prdata.planewave:
    dndt=nlo.dndt_s
  else:
    dndt=nlo.dndt_f
  
  tsteps=prdata.tsteps
  batchnum_spec=prdata.batchnum_spec  #number of batches
  batchsize=niter//batchnum_spec #size of one batch
  nbatches=niter//batchsize  #true number of batches

  deltat=derived.deltat
  windowxy=derived.windowxy
  fwindowxy=cp.fft.fftshift(windowxy)

# allocate storage for space charge field
  if nbatches == 1:
    dnfull=cp.zeros((niter,xsamp,ysamp),dtype=float)   #full 3D space charge field  in gpu
  else:  #if multiple batches, allocate space for full xyz space charge arrays
    dnfull_cpu=np.zeros((niter,xsamp,ysamp),dtype=float)   #full 3D space charge field i####n cpu use numpy
    dnfull = cp.zeros((batchsize,xsamp,ysamp),dtype=float)
  gaint=[]
  #initialize variables
  jt_last_good=0
  tic=time.time()
  ampxzt=cp.zeros((tsteps//skip,xsamp,niter),dtype=complex) #time dependent ampxz
  dnxzt=cp.zeros((tsteps//skip,xsamp,niter))  #time dependet dnxz
  #print('starting')
  for jt in tqdm(range(tsteps)):
    #print(jt)
    if jt%skip==0:
      ampxyt=[] #time dependent output amplitude
      dnxyt=[]   #time dedpendent output dn
      
    if abort==True:
      break
    #Set input field to amp0
    amp=derived.amp0
    ampft=cp.fft.fft2(amp) #for first propagation step at each time step
    #begin z propagation

    jb=0 # base index of first batch
    #loop over all batches inner loop
    for j in range(nbatches):
      
      
      if abort==True: break
      if nbatches != 1:   #load batch  escs from npu if more than one batch
        jb=j*batchsize
        dnfull=cp.asarray(dnfull_cpu[jb:jb+batchsize]) 
      #begin batch
      for i in range(batchsize): # total number of z steps (niter) if one batch
          if abort==True: break
          # linear diffraction of amplitude amp for one dz step
          # ampft is the one saved from previous step (after 1st step)
          amp=cp.fft.ifft2(ampft*h*fwindowxy)
          ampft=cp.fft.fft2(amp)
          dnfull[i] += deltat*dndt(dn_in=dnfull[i],amp=amp,prdata=prdata,derived=derived)
            # calculate photorefractive index at current batch position
            # apply dn to amp
          amp=amp*cp.exp(-2j*cp.pi/lm*dnfull[i]*dz)*windowxy

          if noisetype=='volume xy':
            # apply noise if called for
            noise_xy=noisexy(jb+i,prdata,derived.seeds)
            amp=amp*cp.exp(1j*noise_xy)
          # check for instability in integration
          if cp.isnan(cp.sum(amp)) and abort==False:
            abort=True
            jt_last_good=jt-1
            if jt_last_good<0:
              jt_last_good=0
            print('aborted for time instability at ',jt)

          ampft=cp.fft.fft2(amp)
          ampft=cp.where(lm**2*fxy2<1,ampft,0)

          #end of propagation step

          if jt%skip==0:
            #build batched section of xz output            
            ampxzt[jt//skip,:,j*batchsize+i]=amp[:,ysamp//2]
            dnxzt[jt//skip,:,j*batchsize+i]=dnfull[i,:,ysamp//2]
            
      if nbatches != 1 and processor == 'gpu' :
        #print('batch done')
        dnfull_cpu[jb:jb+batchsize]=dnfull.get()
          #update space charge field in cpu
      #end batch
    if jt%skip == 0:
      #build outputs at time jt
      if prdata.backpropagate:
        ampb=amp
        ampbft=cp.fft.fft2(ampb)
        for i in range(niter):
            ampbft=ampbft*cp.conj(h)
            ampb=cp.fft.ifft2(ampbft)*windowxy
        if 'ampxyt' in outputs: appender_ind('ampxyt',outputs,ampxyt,ampb)
      else:
        if 'ampxyt' in outputs: appender_ind('ampxyt',outputs,ampxyt,amp)
      dnxyt = appender_ind('dnxyt',outputs,dnxyt,dnfull[-1])  

      #build time stack of xz outputs
            
      gainout,ampspm=gain(amp,prdata,derived)
      gaint.append(gainout)

   #end of outer loop
    
  if processor == 'gpu':
    print('from gpu')
    if 'ampxzt' in outputs:
      output.ampxzt=ampxzt.get()
    if 'dnxzt' in outputs:
      output.dnxzt=dnxzt.get()
    if 'ampxyt' in outputs:
      output.ampxyt=ampxyt.get()
    if 'dnxyt' in outputs:
      output.dnxyt=dnxyt.get()
    derived.x=derived.x.get()
    derived.y=derived.y.get()
  else:
    print('from cpu')
    if 'ampxzt' in outputs:
      output.ampxzt=ampxzt
    if 'dnxzt' in outputs:
      output.dnxzt=dnxzt
    if 'ampxyt' in outputs:
      output.ampxyt=ampxyt
    if 'dnxyt' in outputs:
      output.dnxyt=dnxyt    
       
  output.gainout=gain(amp,prdata,derived)
  output.gaint=gaint 
  toc=time.time()
  print('elapsed time ',toc-tic)

  return amp,derived,output