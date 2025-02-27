import cv2
import numpy as np
from .space_convert import rgb_to_lab

def delta_e_2000(x,y,textiles=False):

	x = rgb_to_lab(x)
	y = rgb_to_lab(y)

	L1,a1,b1 = cv2.split(x)
	L2,a2,b2 = cv2.split(y)

	C1 = np.hypot(a1,b1)
	C2 = np.hypot(a2,b2)

	Cb = 0.5*(C1+C2)

	Cb7 = Cb**7
	G = 0.5*(1-np.sqrt(Cb7/(Cb7+25**7)))

	ap1 = a1*(1+G)
	ap2 = a2*(1+G)

	hp1 = np.where(
		np.logical_and(b1 == 0,ap1 == 0),
		0,
		np.degrees(np.arctan2(b1,ap1))%360)
	hp2 = np.where(
		np.logical_and(b2 == 0,ap2 == 0),
		0,
		np.degrees(np.arctan2(b2,ap2))%360)

	Cp1 = np.hypot(ap1,b1)
	Cp2 = np.hypot(ap2,b2)

	Cbp = 0.5*(Cp1+Cp2)
	mul_Cp = Cp1*Cp2
	add_hp = hp1+hp2
	sub_hp = hp2-hp1
	abs_sub_hp = np.fabs(sub_hp)
	Hbp = np.select(
		[
			mul_Cp == 0,
			abs_sub_hp <= 180,
			np.logical_and(abs_sub_hp > 180,add_hp < 360),
			np.logical_and(abs_sub_hp > 180,add_hp >= 360),
		],
		[
			add_hp,
			0.5*add_hp,
			0.5*(add_hp+360),
			0.5*(add_hp-360),
		])

	dhp = np.select(
		[
			mul_Cp == 0,
			abs_sub_hp <= 180,
			sub_hp < -180,
			sub_hp > 180,
		],
		[
			0,
			sub_hp,
			sub_hp+360,
			sub_hp-360,
		])
	Lbp = 0.5*(L1+L2)
	T = (
		 1
		-0.17*np.cos(np.deg2rad(Hbp-30))
		+0.24*np.cos(np.deg2rad(2*Hbp))
		+0.32*np.cos(np.deg2rad(3*Hbp+6))
		-0.20*np.cos(np.deg2rad(4*Hbp-63))
	)
	Cbp7 = Cbp**7
	RC = 2*np.sqrt(Cbp7/(Cbp7+25**7))
	dtheta = 30*np.exp(-((Hbp-275)/25)**2)

	dLp = L2-L1
	dCp = Cp2-Cp1
	dHp = 2*np.sqrt(mul_Cp)*np.sin(np.deg2rad(dhp/2))
	KL = 2 if textiles else 1
	KC = 1
	KH = 1
	Lbp2 = (Lbp-50)**2
	SL = 1+((0.015*Lbp2)/np.sqrt(20+Lbp2))
	SC = 1+0.045*Cbp
	SH = 1+0.015*Cbp*T
	RT = -RC*np.sin(np.deg2rad(2*dtheta))

	return np.sqrt(
		(dLp/(KL*SL))**2+
		(dCp/(KC*SC))**2+
		(dHp/(KH*SH))**2+
		RT*(dCp/(KC*SC))*(dHp/(KH*SH)))