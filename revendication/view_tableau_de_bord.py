# coding: utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.template import loader
#from django.core.exceptions import ObjectDoesNotExist


from .forms import *
from .models import *
from django.contrib.auth.models import* 
from django.contrib.auth import *
from bs4 import BeautifulSoup
from django.template.response import *
import bs4
import re
import pickle
import os
from nltk import *
from bs4 import BeautifulSoup
from random import *
from .fonctions.creation_graph import *




app_name = 'revendication'




#_____________________vue_______________________#



def tableau_de_bord(request):
	

	utilisateur = request.user



	def les_x_revendications_les_plus_proches_des_miennes(n):

		selection = data_propositions_proches_des_miennes(utilisateur)
		selection = sorted(selection, key=lambda x: x[2])
		selection.reverse()
		selection2= []
		liste_p = []
		#print ("selection:",selection)

		#eliminer les propositions dont je suis déjà supporter
		liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
		for p in liste_de_mes_propositions:
			liste_p.append(p.ennonce)

		print ("selection:", selection)
		for triplet in selection:
			if triplet[1] in liste_p:
				print ("le triplet contenant", triplet[1] , "va être enlevé.")
				selection.remove(triplet)
			else:
				if triplet[2] > 0:
					selection2.append(triplet[1])
		

		print ("______________", selection2)
		return selection2[0:n]	



	def trier_les_elements_par_dates(liste):
		liste = sorted(liste, key=lambda x: x[1])
		liste.reverse()
			


	def creer_les_datas(utilisateur):

		class Datas:
			def __init__ (self):
				self.evenements = Evenement.objects.filter(soutien__user = utilisateur)
				self.organisations = Organisation.objects.filter(soutien__user = utilisateur)
				#datas.documents = Documents.objects.filter(soutien__user = utilisateur)
				self.competence = Competence.objects.filter(soutien__user = utilisateur)
				self.petition = Petition.objects.filter(soutien__user = utilisateur)
				self.revendications = Proposition.objects.filter(soutien__user = utilisateur)
		
		datas = Datas()
		return datas


	def mes_revendications(utilisateur):
		mes_propositions = Proposition.objects.all(soutien__user = utilisateur, soutien__lien = 'SO')



 


	datas = creer_les_datas(utilisateur)	
	revendications_proches = les_x_revendications_les_plus_proches_des_miennes(4)	
	graph_utilisateur(utilisateur)


	return render(request, 'revendications/page_tableau_de_bord.html', {"datas":datas, "revendications_proches":revendications_proches})

























