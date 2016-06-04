import numpy as np
import matplotlib.pyplot as plt
from cvip import *

def tohomogeneous(data):
    return np.append(data, np.ones((1, data.shape[1])), 0)

def dehomogeneous(data):
    return data[0:-1, :]

def makepolygon(data):
    return np.append(data, np.reshape(data[:, 0], (-1, 1)), 1)

##########################################
# Data
##########################################

# Set model
model = makepolygon(tohomogeneous(np.array([[0, 5, 0], [-1, 8, 0], [1, 8, 0]]).transpose()))

# Set target
Rangle = 60
Rs = tf.rotation_matrix(np.deg2rad(Rangle), [0, 0, 1])
Tt = np.reshape(np.asarray([3, 1, 0, 0]), (-1, 1))
target = Rs.dot(model) + Tt

# Set camera
cameramodel = makepolygon(tohomogeneous(np.array([[-1, 0, 0], [-3, 2.5, 0], [3, 2.5, 0], [1, 0, 0], [4, 0, 0], [4, -4, 0], [-4, -4, 0], [-4, 0, 0]]).transpose() / 8.0))

##########################################
# Model transformation: model to target
##########################################

modelR = Rs.dot(model)

plt.figure()
plt.subplot(2, 3, 1)
plt.plot(model[0, :], model[1, :], 'b', linewidth = 2.0)
plt.plot(target[0, :], target[1, :], 'r', linewidth = 2.0)
plt.plot(modelR[0, :], modelR[1, :], 'b', linewidth = 1.0)
plt.plot(cameramodel[0, :], cameramodel[1, :], 'k', linewidth = 1.0)
plt.gca().annotate('', xy = (modelR[0, 0], modelR[1, 0]), xycoords = 'data',
                   xytext = (model[0, 0], model[1, 0]), textcoords = 'data',
                   arrowprops = dict(arrowstyle = "-", connectionstyle = "angle3,angleA=0,angleB=%f" % Rangle))
plt.gca().annotate('', xy = (target[0, 0], target[1, 0]), xycoords = 'data',
                   xytext = (modelR[0, 0], modelR[1, 0]), textcoords = 'data',
                   arrowprops = dict(arrowstyle = "->", connectionstyle = "angle,angleA=%f,angleB=%f,rad=0" % (0, -90)))
plt.legend(('Pm', 'Pt', 'R*Pm'), prop={'size': 12})
plt.title('Model to target: Pt = R*Pm + T')
plt.grid()
plt.axis('scaled')
plt.xlim((-8, 8))
plt.ylim((-2, 10))
plt.ylabel('Scene', fontsize = 20)

##########################################
# Model transformation: target to model
##########################################

targetRinv = Rs.transpose().dot(target)

plt.subplot(2, 3, 2)
plt.plot(model[0, :], model[1, :], 'b', linewidth = 2.0)
plt.plot(target[0, :], target[1, :], 'r', linewidth = 2.0)
plt.plot(targetRinv[0, :], targetRinv[1, :], 'r', linewidth = 1.0)
plt.plot(cameramodel[0, :], cameramodel[1, :], 'k', linewidth = 1.0)
plt.gca().annotate('', xy = (targetRinv[0, 0], targetRinv[1, 0]), xycoords = 'data',
                   xytext = (target[0, 0], target[1, 0]), textcoords = 'data',
                   arrowprops = dict(arrowstyle = "-", connectionstyle = "arc3,rad=-0.3"))
plt.gca().annotate('', xy = (model[0, 0], model[1, 0]), xycoords = 'data',
                   xytext = (targetRinv[0, 0], targetRinv[1, 0]), textcoords = 'data',
                   arrowprops = dict(arrowstyle = "->", connectionstyle = "angle,angleA=%f,angleB=%f,rad=0" % (-Rangle, -90-Rangle)))
plt.legend(('Pm', 'Pt', 'Rinv*Pt'), prop={'size': 12})
plt.title('Target to model: Pm = Rinv*Pt - Rinv*T')
plt.grid()
plt.axis('scaled')
plt.xlim((-8, 8))
plt.ylim((-2, 10))

##########################################
# Model transformation: target to model
##########################################

targetTinv = target - Tt

plt.subplot(2, 3, 3)
plt.plot(model[0, :], model[1, :], 'b', linewidth = 2.0)
plt.plot(target[0, :], target[1, :], 'r', linewidth = 2.0)
plt.plot(targetTinv[0, :], targetTinv[1, :], 'r', linewidth = 1.0)
plt.plot(cameramodel[0, :], cameramodel[1, :], 'k', linewidth = 1.0)
plt.gca().annotate('', xy = (targetTinv[0, 0], targetTinv[1, 0]), xycoords = 'data',
                   xytext = (target[0, 0], target[1, 0]), textcoords = 'data',
                   arrowprops = dict(arrowstyle = "-", connectionstyle = "angle,angleA=%f,angleB=%f,rad=0" % (90, 0)))
plt.gca().annotate('', xy = (model[0, 0], model[1, 0]), xycoords = 'data',
                   xytext = (targetTinv[0, 0], targetTinv[1, 0]), textcoords = 'data',
                   arrowprops = dict(arrowstyle = "->", connectionstyle = "arc3,rad=-0.3"))
plt.legend(('Pm', 'Pt', 'Pt-T'), prop={'size': 12})
plt.title('Target to model: Pm = Rinv*(Pt - T)')
plt.grid()
plt.axis('scaled')
plt.xlim((-8, 8))
plt.ylim((-2, 10))

##########################################
# Camera pose: model to target
##########################################

cameratarget = Rs.transpose().dot(cameramodel - Tt)
cameramodelTinv = cameramodel - Tt

plt.subplot(2, 3, 4)
plt.plot(cameramodel[0, :], cameramodel[1, :], 'b', linewidth = 2.0)
plt.plot(cameratarget[0, :], cameratarget[1, :], 'r', linewidth = 2.0)
plt.plot(cameramodelTinv[0, :], cameramodelTinv[1, :], 'b', linewidth = 1.0)
plt.plot(model[0, :], model[1, :], 'k', linewidth = 1.0)
plt.gca().annotate('', xy = (cameramodelTinv[0, 0], cameramodelTinv[1, 0]), xycoords = 'data',
                   xytext = (cameramodel[0, 0], cameramodel[1, 0]), textcoords = 'data',
                   arrowprops = dict(arrowstyle = "-", connectionstyle = "angle,angleA=%f,angleB=%f,rad=0" % (0, -90)))
plt.gca().annotate('', xy = (cameratarget[0, 0], cameratarget[1, 0]), xycoords = 'data',
                   xytext = (cameramodelTinv[0, 0], cameramodelTinv[1, 0]), textcoords = 'data',
                   arrowprops = dict(arrowstyle = "->", connectionstyle = "arc3,rad=-0.3"))
plt.legend(('Cm', 'Ct', 'Cm-T'), prop={'size': 12})
plt.title('Model to target: Ct = Rinv*(Cm - T)')
plt.grid()
plt.axis('scaled')
plt.xlim((-8, 8))
plt.ylim((-2, 10))
plt.ylabel('Camera', fontsize = 20)

##########################################
# Camera pose: model to target
##########################################

cameramodelRinv = Rs.transpose().dot(cameramodel)

plt.subplot(2, 3, 5)
plt.plot(cameramodel[0, :], cameramodel[1, :], 'b', linewidth = 2.0)
plt.plot(cameratarget[0, :], cameratarget[1, :], 'r', linewidth = 2.0)
plt.plot(cameramodelRinv[0, :], cameramodelRinv[1, :], 'r', linewidth = 1.0)
plt.plot(model[0, :], model[1, :], 'k', linewidth = 1.0)
plt.gca().annotate('', xy = (cameramodelRinv[0, 0], cameramodelRinv[1, 0]), xycoords = 'data',
                   xytext = (cameramodel[0, 0], cameramodel[1, 0]), textcoords = 'data',
                   arrowprops = dict(arrowstyle = "-", connectionstyle = "arc3,rad=0.3"))
plt.gca().annotate('', xy = (cameratarget[0, 0], cameratarget[1, 0]), xycoords = 'data',
                   xytext = (cameramodelRinv[0, 0], cameramodelRinv[1, 0]), textcoords = 'data',
                   arrowprops = dict(arrowstyle = "->", connectionstyle = "angle,angleA=%f,angleB=%f,rad=0" % (-Rangle, -90-Rangle)))
plt.legend(('Cm', 'Ct', 'Rinv*Cm'), prop={'size': 12})
plt.title('Model to target: Ct = Rinv*Cm - Rinv*T')
plt.grid()
plt.axis('scaled')
plt.xlim((-8, 8))
plt.ylim((-2, 10))

##########################################
# Camera pose: target to model
##########################################

plt.subplot(2, 3, 6)
plt.plot(cameramodel[0, :], cameramodel[1, :], 'b', linewidth = 2.0)
plt.plot(cameratarget[0, :], cameratarget[1, :], 'r', linewidth = 2.0)
plt.plot(cameramodelTinv[0, :], cameramodelTinv[1, :], 'b', linewidth = 1.0)
plt.plot(model[0, :], model[1, :], 'k', linewidth = 1.0)
plt.gca().annotate('', xy = (cameramodelTinv[0, 0], cameramodelTinv[1, 0]), xycoords = 'data',
                   xytext = (cameratarget[0, 0], cameratarget[1, 0]), textcoords = 'data',
                   arrowprops = dict(arrowstyle = "-", connectionstyle = "arc3,rad=0.3"))
plt.gca().annotate('', xy = (cameramodel[0, 0], cameramodel[1, 0]), xycoords = 'data',
                   xytext = (cameramodelTinv[0, 0], cameramodelTinv[1, 0]), textcoords = 'data',
                   arrowprops = dict(arrowstyle = "->", connectionstyle = "angle,angleA=%f,angleB=%f,rad=0" % (0, 90)))
plt.legend(('Cm', 'Ct', 'R*Ct'), prop={'size': 12})
plt.title('Target to model: Cm = R*Ct + T')
plt.grid()
plt.axis('scaled')
plt.xlim((-8, 8))
plt.ylim((-2, 10))
plt.show()
