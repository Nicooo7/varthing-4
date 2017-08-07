# coding: utf-8

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, Http404
from django.template import loader
from .forms import *
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


app_name = 'revendication'


#__________________vues _______________________



def authentification(request):
	error = False
	
	if request.method == 'POST':
		form = AuthentificationForm(request.POST)
		if form.is_valid():
			username = request.POST["nom"]
			password = request.POST["mot_de_passe"]
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				print ("authentification réussie")
				return redirect ('page_accueil')
				
			else:
				error = True
		else:
			form = AuthentificationForm()
	else:		
		form = AuthentificationForm()		
		return render(request, 'revendications/page_authentification.html', {'form': form})



def deconnexion (request):
	from django.contrib.auth import logout
	from django.shortcuts import render
	from django.core.urlresolvers import reverse
	logout(request)
	return redirect ('page_accueil')



def creer_utilisateur (request):
	if request.method == 'POST':
		form = UtilisateurForm(request.POST)
		if form.is_valid():
			nom = request.POST['nom']
			mot_de_passe = request.POST['mot_de_passe']
			mail = request.POST['mail']
			utilisateur = User.objects.create_user(nom, mail, mot_de_passe)
			autre_utilisateur = Autre_utilisateur.objects.create(user = utilisateur)
			profile = Profile.objects.create (utilisateur = utilisateur)

			return render(request, 'revendications/page_accueil.html')
	else:
			form = UtilisateurForm()
	
	titre = "nouvel utilisateur"
	return render(request, 'revendications/page_creer.html', {'form': form, "titre": titre, "url" : "page_creer_utilisateur"})
	





