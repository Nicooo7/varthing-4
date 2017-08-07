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
from unidecode import unidecode



app_name = 'revendication'
	

def creer_revendication(request):

	utilisateur= request.user

	if request.method == 'POST':
		form = RevendicationForm(request.POST)
		
		if form.is_valid():
			intitule = unidecode(request.POST["intitule"]).encode('utf-8')
			#on crée la proposition 
			la_proposition = Proposition.objects.create(ennonce = intitule, tags=request.POST["tags"]) 
			la_proposition.save()
			le_soutien = Soutien.objects.create(user=utilisateur, propositions = la_proposition, lien= 'CR')
			le_soutien = Soutien.objects.create(user=utilisateur, propositions = la_proposition, lien= 'SO')
			le_soutien.save()
			print ("soutien ajouté:{0} ".format(la_proposition.supporter))

			#on retourne à la page accueil
			return render (request, 'revendications/page_accueil.html')		
			
	else:
		liste = u""
		propositions = Proposition.objects.all()
		for proposition in propositions:
			ennonce = proposition.ennonce
			liste = liste + ennonce + u"_"


		
		liste = unidecode(liste)
		liste = liste.encode("utf-8")

		



		titre = "creer une revendication"
		form = RevendicationForm
		return render(request, 'revendications/page_creer_une_revendication.html', {"liste" : liste, "form": form, "titre": titre})


def creer_petition(request):

	utilisateur= request.user

	if request.user.is_authenticated:
		user = request.user
	else:
		render(request, 'authentification_necessaire.html')


	# Récups des infos GET si transmises
	if 'id_proposition' in request.GET:
		id_proposition = request.GET['id_proposition']
	else:
		id_proposition = ''


	if request.method == 'POST':
		#
		# Un formulaire a été envoyé !
		#
		form = PetitionForm(request.POST)
		if form.is_valid():
			#
			# Traitement du formulaire valide
			#
			titre = unidecode(form.cleaned_data['titre']).encode('utf-8')

			description = unidecode(form.cleaned_data['description']).encode('utf-8')
			date_echeance = form.cleaned_data['date_echeance']
			objectif_de_signataires = form.cleaned_data['objectif_de_signataires']

			#propositions = form.cleaned_data['propositions']

			#proposition = Proposition.objects.get(id = id_proposition)	

			# Récupération des propositions cochées
			# erreur si liste vide
			try:
				propositions = request.POST.getlist('propositions')
			except:
				raise Http404

			
			# Création de la pétition puis association à la proposition source
			petition = Petition.objects.create(titre=titre, description=description, date_echeance=date_echeance, objectif_de_signataires=objectif_de_signataires)

			for i in propositions:
				petition.propositions.add(i)
			
			#petition.propositions.add(proposition)
			petition.save()

			# Création de la relation de soutient (CR) entre l'user et la pétition
			soutien = Soutien.objects.create(petition = petition, user = user, lien = 'CR')

			#on retourne à la page accueil
			return render (request, 'revendications/page_accueil.html')	


	else:
		#
		# Pas de formulaire reçu...
		#

		form = PetitionForm()
		revendications_soutenues = Proposition.objects.filter(soutien__user = user)
		titre = u"creer une petition"
	
		return render(request, 'revendications/page_creer.html', {'form': form, 'id_proposition':id_proposition, 'revendications_soutenues':revendications_soutenues , "titre": titre})

		


def creer_evenement(request):

	utilisateur= request.user

	if request.user.is_authenticated:
		user = request.user
	else:
		print ('authentification necessaire')


	# Récups des infos GET si transmises
	if 'id_proposition' in request.GET:
		id_proposition = request.GET['id_proposition']
	else:
		id_proposition = ''


	if request.method == 'POST':
		#
		# Un formulaire a été envoyé !
		#
		form = EvenementForm(request.POST)
		if form.is_valid():
			#
			# Traitement du formulaire valide
			#
			titre = unidecode(form.cleaned_data['titre']).encode('utf-8')
			description = unidecode(form.cleaned_data['description']).encode('utf-8')
			date = form.cleaned_data['date']
				

			# Création de l'evenement'puis association à la proposition source
			evenement = Evenement.objects.create(titre=titre, description=description, date=date)

			
			#petition.propositions.add(proposition)
			evenement.save()

			# Création de la relation de soutient (CR) entre l'user et la pétition
			soutien = Soutien.objects.create(evenement = evenement, user = user, lien = 'CR')

			#on retourne à la page accueil
			return render (request, 'revendications/page_accueil.html')	
		

		else:
			#
			# Pas de formulaire reçu...
			#

			form = EvenementForm()
			revendications_soutenues = Proposition.objects.filter(soutien__user = user)
			titre = u"creer un evenement"
			return render(request, 'revendications/page_creer.html', {'form': form, 'id_proposition':id_proposition, 'revendications_soutenues':revendications_soutenues, "titre": titre})


def creer_competence(request):

	# Vérification de l'authentification utilisateur, redirection sinon
	#   -> voir https://docs.djangoproject.com/fr/1.10/topics/auth/default/#the-login-required-decorator
	if request.user.is_authenticated:
		user = request.user
	else:
		render(request, 'authentification_necessaire.html')


	# Récups des infos GET si transmises
	if 'id_proposition' in request.GET:
		id_proposition = request.GET['id_proposition']
	else:
		id_proposition = ''


	if request.method == 'POST':
		#
		# Un formulaire a été envoyé !
		#
		form = CompetenceForm(request.POST)
		if form.is_valid():
			#
			# Traitement du formulaire valide
			#
			titre = unidecode(form.cleaned_data['titre']).encode('utf-8')
			description = unidecode(form.cleaned_data['description']).encode('utf-8')
			date_echeance = form.cleaned_data['date_echeance']
			propositions = Proposition.objects.get(id = id_proposition)
	



			lieu = request.POST ['lieu']

			#propositions = form.cleaned_data['propositions']

			#proposition = Proposition.objects.get(id = id_proposition)	

			# Récupération des propositions cochées
			# erreur si liste vide
			try:
				propositions = request.POST.getlist('propositions')
			except:
				raise Http404

			#if not propositions:
				#return render(request, 'revendications/message.html', {'message':"Cocher au moins une proposition !"})

			

			"""
			"""
			# Création de la pétition puis association à la proposition source
			competence = Competence.objects.create(titre=titre, description=description, date_echeance=date_echeance, lieu=lieu )

			for i in propositions:
				competence.propositions.add(i)
			
			#competence.propositions.add(proposition)
			competence.save()

			# Création de la relation de soutient (CR) entre l'user et la competence
			soutien = Soutien.objects.create(competence = competence, user = user, lien = 'CR')
			return render (request, 'revendications/page_accueil.html')	

			
	else:
		#
		# Pas de formulaire reçu...
		#

		form = CompetenceForm()
		revendications_soutenues = Proposition.objects.filter(soutien__user = user)
		titre = u"demander une competence"
		return render(request, 'revendications/page_creer.html', {'form': form, 'id_proposition':id_proposition, 'revendications_soutenues':revendications_soutenues, "titre": titre})



