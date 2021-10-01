#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  estatistica.py
#  
#  Copyright 2017 Alex Santos <Alex@Inspiron7460>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import math

def Media(valores):
	soma = 0.0
	media = 0.0
	if len(valores)==0:
		return 0
	else:
		for i in range(len(valores)):
			soma =soma + valores[i]
		media = soma / float(len(valores))
	return media

def CalculaMediaDesvio(valores):
	if len(valores) < 2:
		return [0,0]
	soma_quadrado = 0.0
	desvio = 0.0
	soma = 0.0
	media = 0.0
	for i in range(len(valores)):
		soma =soma + valores[i]
	media = soma / float(len(valores))
	for i in range(len(valores)):
		soma_quadrado += (valores[i]-media)**2
	desvio = (soma_quadrado / (len(valores)-1))**0.5
	return [media,desvio]

def calcularIC(valores):
    media = Media(valores)
    desvio = CalculaMediaDesvio(valores)
    #somaValores = sum(valores)
    total = int(len(valores))
    #print media, desvio,somaValores

    ic = 1.96 * (int(desvio[1])/math.sqrt(total))
    #print ic

    interConfianca = []
    interConfianca.append(media - ic) 
    interConfianca.append(media + ic)

    return interConfianca
