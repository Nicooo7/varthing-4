# coding: utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.template import loader
#from django.core.exceptions import ObjectDoesNotExist


from revendication.models import *
from django.contrib.auth.models import* 
from django.contrib.auth import *
from bs4 import BeautifulSoup
from django.template.response import *
import bs4
import re
import urllib.parse
import pickle
import os
from nltk import *
from bs4 import BeautifulSoup
from random import *
from datetime import datetime
from datetime import timedelta
from .fonctions.creation_graph import *
from unidecode import unidecode

page = []
liste_des_elements_de_page = []


app_name = 'accueil'










#__________________vues _______________________



def varthing(request):
	return render(request, 'revendications/varthing.html')



def accueil(request):


	from django.contrib.auth.models import User
	utilisateur = request.user.username
	#print ("voici l'utilisateur" , utilisateur)



	propositions = Proposition.objects.all()
	for proposition in propositions:
		p = Proposition.objects.get(id = proposition.id)
		p.ennonce = unidecode(p.ennonce).lower()
		p.save()

	
	#dernieres revendications crees:
	def dernieres_revendications():
		dernieres_revendication_creees = []
		liste = []
		propositions= []
		propositions = Proposition.objects.all()
		for proposition in propositions:
			liste.append((proposition, proposition.date_creation))
			
		lambda colonne: colonne[1]
		liste = sorted(liste, key=lambda colonnes: colonnes[1])
		print (liste)
		liste.reverse()
		print (liste)
		
		dernieres_revendication_creees = [t[0] for t in liste[0:4]]
		return dernieres_revendication_creees
	dernieres_revendication_creees = dernieres_revendications()	


	#acceleration des soutiens:
		#compter les soutiens des revendications à ce jour
	def acceleration_des_soutiens():
		liste_acceleration = []
		dictionnaire = {}
		dictionnaire2 = {}
		liste_finale = []

		propositions = Proposition.objects.all()
		for proposition in propositions:
			soutiens = Soutien.objects.filter(propositions = proposition)
			nb_soutien = soutiens.count()
			dictionnaire[proposition.id] =nb_soutien

		#compter les soutiens des revendications il y a 2 semaines
		liste2= []
		time_delta= timedelta(days=50)

		propositions = Proposition.objects.all()
		for proposition in propositions:
			soutiens = Soutien.objects.filter(propositions = proposition, date__lte= (datetime.now() - time_delta)) 
			nb_soutien = soutiens.count()
			dictionnaire2[proposition.id] = nb_soutien
		#calculer la proportion de soutien en plus entre ce jour et il y a deux semaines

		for proposition in propositions:
			nb_soutien_ce_jour = dictionnaire[proposition.id]
			#print ("nb soutien ce jour", nb_soutien_ce_jour)
			nb_soutien_avant = dictionnaire2[proposition.id]
			#print ("nb soutien avant", nb_soutien_avant)
			proportion = (nb_soutien_ce_jour - nb_soutien_avant)/nb_soutien_ce_jour
			liste_acceleration.append((proposition.id, proportion))
		
		lambda colonne: colonne[1]
		liste_acceleration = sorted(liste_acceleration, key=lambda colonnes: colonnes[1])
		liste_acceleration.reverse()
		liste_acceleration = liste_acceleration[0:4]
		print (liste_acceleration, "liste acceleration")
		for couple in liste_acceleration:
			print(couple)
			proposition = Proposition.objects.get (id = couple[0])
			liste_finale.append(proposition)
		print (liste_finale)
		return (liste_finale)
	proposition_en_acceleration = acceleration_des_soutiens()	

		


	#propositions triées selon leur nombre de soutien.
	def populaires():	
		liste = []
		propositions = Proposition.objects.all()
		for proposition in propositions:
			soutiens = Soutien.objects.filter(propositions = proposition)
			nb_soutien = soutiens.count()
			liste.append((proposition, nb_soutien))
			liste = sorted(liste, key=lambda colonnes: colonnes[1])
		liste.reverse()
		populaires = [t[0] for t in liste [0:3]]
		return populaires
	propositions_populaires = populaires()		



	graph_accueil()


	return render(request, 'revendications/page_accueil.html', {"utilisateur":utilisateur, "propositions_populaires":propositions_populaires,  "dernieres_revendication_creees" : dernieres_revendication_creees, "proposition_en_acceleration" : proposition_en_acceleration})









