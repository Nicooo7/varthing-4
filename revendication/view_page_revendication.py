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
from unidecode import unidecode

app_name = 'revendication'


#_____________________vue_______________________#



    	

def page_revendication(request):

	ennonce = unidecode(request.GET ['ennonce'])
	print (ennonce)
	try:
		proposition = Proposition.objects.get(ennonce = ennonce)
	except Proposition.DoesNotExist:
		raise Http404



	def data_proposition(proposition):
		# Vérification identifiant valide ? si non, 404
		id_proposition = proposition.id

		class Data:
			def __init__ (self):	
				self.proposition = proposition
				self.soutiens= Soutien.objects.filter(propositions__id = id_proposition).filter(lien ='SO')
				self.createur= Soutien.objects.filter(propositions__id = id_proposition).filter(lien = 'CR')
				if len(self.createur)<1:
					self.createur = "inconnu"
				self.evenement = Evenement.objects.filter(proposition_id = id_proposition)
				self.petitions = proposition.petition_set.all()
				self.competences = proposition.competence_set.all()
				self.organisations = Evenement.objects.filter(proposition_id = id_proposition)
				#self.documents = proposition.document_set.all()


		data = Data()		
		return (data)


	def est_ce_que_je_soutiens(proposition):
		utilisateur = request.user
		supporters = Soutien.objects.filter(propositions = proposition, lien = 'SO')
		for supporter in supporters:
			print ("supporter" , supporter)
			if utilisateur == supporter.user:
				return "soutenue"

	s = est_ce_que_je_soutiens(proposition)	
	print ("s", s)


	graph_revendication(proposition)	
	data_p= []
	for triplet in data_propositions_proches(proposition):
		data_p.append (triplet[1])
	data_proposition = data_proposition (proposition)


	if s == "soutenue" :
		return render (request, 'revendications/page_revendication.html', {"propositions_proches": data_p, "data_proposition":data_proposition, "s":s})
	else:
		return render (request, 'revendications/page_revendication.html', {"propositions_proches": data_p, "data_proposition":data_proposition})	






