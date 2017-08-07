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



def page_organisation(request):
	

	utilisateur = request.user


	def data_propositions_proches_des_miennes (utilisateur):
		liste_proximites = creer_les_triplets()
		#selectionner ce qui concerne cette proposition:
		selection = []
		for triplet in liste_proximites:
			liste_de_mes_propositions = Proposition.objects.filter(soutien__user = utilisateur)
			proposition = triplet[0]
			if proposition in liste_de_mes_propositions:
				selection.append(triplet)
		#print ("triplets_des_prop_proches_des_miennes", selection)
		return selection


	def les_x_revendications_les_plus_proches_des_miennes(x):
		selection = data_propositions_proches_des_miennes(utilisateur)
		selection = selection[0:x][1]
		#print ("revendications proches", selection)
		return selection	


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
				self.revendications_proches = les_x_revendications_les_plus_proches_des_miennes(4)

		datas = Datas()
		return datas

 

	datas = creer_les_datas(utilisateur)	
	graph_utilisateur(utilisateur)
	#print ( "graph : __________________",graph)

	return render(request, 'revendications/page_tableau_de_bord.html', {"datas":datas})






