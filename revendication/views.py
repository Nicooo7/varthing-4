# coding: utf-8

from django.shortcuts import render
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
import urllib.request
import urllib.parse
import pickle
import os
from nltk import *
from bs4 import BeautifulSoup
from random import *

page = []
liste_des_elements_de_page = []


app_name = 'revendication'


  #..........................PROPOSITIONS.........................#



class Vocabulaire: #motclé et  son champs lexical.
	
	def __init__(self,motcle):
		base = "http://www.rimessolides.com/motscles.aspx?m="
		motcle = urllib.parse.quote(motcle)
		url = """{base}{motcle}""".format(base =base, motcle = motcle)
		with urllib.request.urlopen(url) as f:
		    print (f)
		    data = f.read().decode('utf-8')
		    soup = bs4.BeautifulSoup(data, 'html.parser')
		   
		champ_lexical =[]
		for d in soup.find_all('a'):
			mot= d.get_text() 
			champ_lexical.append(mot) 
		for i in range (1,12):
			del champ_lexical[0]
		champ_lexical.reverse()
		for i in range (1,5):
			del champ_lexical[0]	
		champ_lexical.reverse()


		self.motcle = motcle
		self.champ_lexical = champ_lexical

	
def afficher_bonjour():
	print ("bonjour")


def initialiser_le_fichier():
	with open('vocabulaire', 'wb') as fichier:
		mon_pickler = pickle.Pickler(fichier)
		le_mot = Vocabulaire("debut")
		mon_pickler.dump(le_mot)

def enregistrer_un_nouveau_mot(mot):
	print ("ca demarre")
	with open('vocabulaire', 'ab') as fichier:
		liste_des_vocabulaires = []
		le_mot = Vocabulaire(mot)
		mon_pickler = pickle.Pickler(fichier)
		print ("c'est ok")
		mon_pickler.dump(le_mot)

def acceder_aux_vocabulaires():
	with open('vocabulaire', 'rb') as fichier:
		mon_depickler = pickle.Unpickler(fichier)
		print (mon_depickler)
		un_mot = mon_depickler.load()
		while un_mot:
			un_mot = mon_depickler.load()
			print (un_mot.motcle)
			if un_mot.motcle == "fin":
				break

def implementer_la_liste_des_vocabulaires(la_liste_des_vocabulaires):

	with open('vocabulaire', 'rb') as fichier:
		mon_depickler = pickle.Unpickler(fichier)
		for i in range (1, 10):
			un_mot = mon_depickler.load()
		while un_mot:
			un_mot = mon_depickler.load()
			if un_mot.motcle == "fin":
				break
			else:
				une_liste = []
				une_liste.append(un_mot.motcle)
				for element in un_mot.champ_lexical:
					une_liste.append(element)
				la_liste_des_vocabulaires.append(une_liste)



def filtrer_ennonce(ennonce,filtrat):
	from nltk.tokenize import TreebankWordTokenizer
	from nltk.corpus import stopwords
	# On instancie notre tokenizer
	tokenizer = TreebankWordTokenizer()

	tokens = tokenizer.tokenize(ennonce)

	# chargement des stopwords français
	french_stopwords = set(stopwords.words('french'))

	# un petit filtre
	tokens = [token for token in tokens if token.lower() not in french_stopwords]
	for element in tokens:
		filtrat.append(element)
	print ("voici le resultat dans le premier programme {0}".format(filtrat))



def champ_lexical_des_propositions():
	#pour chaque proposition
	propositions = Proposition.objects.all()
	for proposition in propositions:
	#récupérer l'ennoncé de la propostion
		ennonce = proposition.ennonce
		filtrat = []
		filtrer_ennonce(ennonce,filtrat)

		initialiser_le_fichier()

		for mot in filtrat:
			print ("*****************")
			print ("on va enregister le mot {0}".format (mot))
			enregistrer_un_nouveau_mot(mot)
			print ("on a enregistre le mot")
		enregistrer_un_nouveau_mot("fin")

		la_liste_des_vocabulaires = []
		implementer_la_liste_des_vocabulaires (la_liste_des_vocabulaires)
		
		liste = ""
		for une_liste in la_liste_des_vocabulaires:
			for un_mot in une_liste:
				liste = liste + ' ,' + un_mot
		print (liste)

		proposition.champ_lexical = liste
		proposition.save()










#..........................AUTRES.........................#





def creer_les_proximites():
	

	#compter_les_utilisateurs:
	utilisateurs = User.objects.all()
	for utilisateur in utilisateurs:
		liste_des_tuples = []
		liste_des_probabilites = []
		liste_des_utilisateurs = []
		utilisateurs = User.objects.all().exclude(id = utilisateur.id)
		i=0
		for element in utilisateurs:
			i= i+1
		nombre_utilisateur = i
		print ("nombre d'utilisateur :{0}".format(i))
		print ("propositions soutenues par moi :{0}".format(Proposition.objects.filter(soutien__user = utilisateur)))
		#recupérer la première revendication que j'ai en commun avec un utilisateur
		
		for un_utilisateur in utilisateurs:
			print ("ON VA DETERMINER LES PROXIMITES DE {0} avec {1} ".format(utilisateur, un_utilisateur))
			mes_propositions = Proposition.objects.filter(soutien__user = utilisateur).filter(soutien__user = un_utilisateur)
			print ("propositions soutenues par l'autre :{0}".format(Proposition.objects.filter(soutien__user = un_utilisateur)))

			print ("les propositions communes :{0}".format(mes_propositions))


			#pour chaque proposition:
			probabilite = 1
			for proposition in mes_propositions:
				#compter le nombre de soutien de la proposition
				soutiens = User.objects.filter (soutien__propositions = proposition)
				i=0
				for element in soutiens:
					print ("soutien :{0}".format(element.username))
					i= i+1
				nombre_soutien_proposition = i
				print ("nombre de soutien de la première proposition :{0}".format(i))
			#probabilité qu'un utilisateur lambda adhère à mes propositions
				proba = nombre_soutien_proposition/nombre_utilisateur
				probabilite = probabilite * proba
				print ("probabilité en cours de calcul :{0}".format(probabilite))
			print ("probabilité en cours de calcul concernant l'utilisateur {0} :{1}".format(un_utilisateur, probabilite))
			a = (un_utilisateur, probabilite)
			u = un_utilisateur
			p= probabilite
			liste_des_utilisateurs.append (u)
			liste_des_probabilites.append (p)
			liste_des_tuples.append(a)
			print ("liste des probabilites : {0} ".format(liste_des_probabilites))
			#recupere l'utilisateur avec lequel il y a la plus grande affinité.
			
		profile = Profile.objects.get(utilisateur = utilisateur)
		i=1

		#ecriture des proximites de l'utilisateur
		for u, p in liste_des_tuples:
			if Autre_utilisateur.objects.filter(user = u):
				autre_utilisateur = Autre_utilisateur.objects.get(user = u)
				print ("enregistrement numéro {0}".format(i))
				ancienne_proximite=Proximite.objects.filter (profile = profile, Autre_utilisateur =autre_utilisateur)
				if ancienne_proximite:
					ancienne_proximite = Proximite.objects.get (profile = profile, Autre_utilisateur =autre_utilisateur)
					print ("cette proximite existait deja et va etre remplacee par une nouvelle")
					ancienne_proximite.delete()
					proximite = Proximite.objects.create (profile = profile, Autre_utilisateur = autre_utilisateur, proba = p) 
					i = i+1
		

#classer_les_proximites (utilisateur):
	profile = Profile.objects.get(utilisateur =utilisateur)
	print ("profile concerné :{0}".format (profile))
	proximites = Proximite.objects.filter(profile = profile).exclude(Autre_utilisateur__user = utilisateur)
	ancienne_proba_max = 1
	ancien_utilisateur_prefere = utilisateur
	for proximite in proximites:
		print ("proximite concernée :{0}".format (proximite))
		if proximite.proba < ancienne_proba_max:
			ancienne_proba_max = proximite.proba
			ancien_utilisateur_prefere = proximite.Autre_utilisateur.user
			print ("ancien_utilisateur_prefere :{0}".format (ancien_utilisateur_prefere))
	utilisateur_le_plus_proche = ancien_utilisateur_prefere
	propositions_interessantes = Proposition.objects.filter(soutien__user = utilisateur_le_plus_proche).exclude(soutien__user = utilisateur)
	for proposition in propositions_interessantes:
		print ("proposition interessante: {0}".format(proposition.ennonce))



def effacer_proximites():
	proximites =Proximite.objects.all()
	for proximite in proximites:
		proximite.delete()


def simulation1 ():
	liste_personnalite = ["lepen","sarkozy", "bayrou", "hollande", "melanchon"]
	liste_ennonce = ["s'en foutre de la planete", "faire comme si on s'en préoccupait de la planete", "se préoccuper de la planete", "faire de la planete sa priorité"] 
	"""for personnalite in liste_personnalite:
		utilisateur = User.objects.create (username = personnalite)
		utilisateur.save()
		autre_utilisateur = Autre_utilisateur.objects.create (user = utilisateur)
		autre_utilisateur.save()
		profile = Profile.objects.create (utilisateur = utilisateur)
		profile.save()"""
	for ennonce in liste_ennonce:
		proposition = Proposition.objects.create(ennonce = ennonce)


def simulation2():
	utilisateurs = User.objects.all().exclude(username ="nicolas").exclude(username = "nico")
	for utilisateur in utilisateurs:
		utilisateur.set_password("chienchat")
		utilisateur.password.save()





    #..........................REQUESTS.........................#


def consulter (request):


	def proximite_des_propositions():

		propositions = Proposition.objects.all()
		liste = []
		#on récupère la liste des soutiens des propositions que l'on veut comparer
		for proposition1 in propositions:
			soutiens1 = Soutien.objects.filter(propositions = proposition1, lien = 'SO')
			liste_soutiens1 = []
			for e in soutiens1:
				liste_soutiens1.append(e.user.username)



				
			for proposition2 in propositions:
				soutiens2 = Soutien.objects.filter(propositions = proposition2, lien = 'SO')
				liste_soutiens2 = []
				for e in soutiens2:
					liste_soutiens2.append(e.user.username)

				if proposition2 != proposition1:

					#on compare ces propositions
					liste_des_soutiens_communs = []
					for soutien in liste_soutiens1:
						"""print ("proposition1:{}".format(proposition1))
						print ("proposition2: {}".format(proposition2))
						print ("soutien1: {}".format(soutien))
						print ("soutiens2: {}".format(liste_soutiens2))"""
						if soutien in liste_soutiens2:
							liste_des_soutiens_communs.append(soutien)
							#print ("liste des soutiens communs : {}".format(liste_des_soutiens_communs))
					proximite = len(liste_des_soutiens_communs)/(len (soutiens1) + len(soutiens2))
					
					triplet = (proposition1, proposition2, proximite)
					liste.append(triplet)
		


		dictionnaire = sorted(liste, key=lambda x: x[2])
		dictionnaire.reverse()
		return dictionnaire

	proximite = proximite_des_propositions()	

	def affichage_graphique_des_proximite(proximite):

		import networkx as nx
		import matplotlib.pyplot as plt
		
		G = nx.Graph()

		
		propositions = Proposition.objects.all()
		for proposition in propositions:
			G.add_node(proposition)

		for triplet in proximite:
			if triplet[2] > 0.5: 
				G.add_edge(triplet[0], triplet[1], weight = triplet[2])

		pos = nx.spring_layout(G)
		print (pos)

		liste_noeud = []


		#ecriture des noeuds:
		noeuds = "{" + ' "nodes" : ' + "["
		i = "premier"
		for cle, valeur in pos.items():
			
			if i == "premier":
				noeud = "{"  + '"id" : ' + '"' + "{}".format(str(cle)) + '"' + "," + ' "label"  : ' + '"' + "{}".format(cle) + '"' + ","  + '"x" :' + "{}".format(valeur[0]) +  "," + ' "y" : ' + "{}".format (valeur[1]) + ","  + ' "size"  : 3 ' + "}" 
				noeuds = noeuds + "\n" + noeud
				i = "plus_premier"
			else :
				noeud = "{"  + '"id" : ' + '"' + "{}".format(str(cle)) + '"' + "," + ' "label"  : ' + '"' + "{}".format(cle) + '"' + ","  + '"x" :' + "{}".format(valeur[0]) +  "," + ' "y" : ' + "{}".format (valeur[1]) + ","  + ' "size"  : 3 ' + "}" 
				noeuds = noeuds + "\n" + "," + noeud

		noeuds = noeuds + "],"

	


		#ecriture des edges:
		edges = '"edges":'  + "["
		i = "premier"
		a = 0
		for triplet in proximite:
			if triplet[2]>0.25:
				if i == "premier":
					edge = "{"  +  ' "id" : ' + '"' + "{}".format(str(a)) + '"' + ","  + ' "source"  : ' + '"' + "{}".format(triplet[0]) + '"' + ","  + ' "target"  :'  + '"' + "{}".format(triplet[1]) + '"' + "}" 
					edges = edges + "\n" +  edge
					i= "plus_premier"
					a = a+1

				else:
					edge = "{"  +  ' "id" : ' + '"' + "{}".format(str(a)) + '"' + ","  + ' "source"  : ' + '"' + "{}".format(triplet[0]) + '"' + ","  + ' "target"  :'  + '"' + "{}".format(triplet[1]) + '"' + "}" 
					edges = edges + "\n" + "," + edge
					a = a+1

		edges = edges + "] }"

		



		#ecriture des data
		data = noeuds + "\n" + "\n" + edges



		#nx.draw_spring(G, with_labels = True, width = 0.1)
		#path = "/Users/nicolasvinurel/Desktop/graph/graph"
		#plt.savefig(path + ".png")
		#nx.write_gexf(G, path + ".gexf")
		return data
		

	data = affichage_graphique_des_proximite(proximite)
	fichier_data = open("/Users/nicolasvinurel/Desktop/depot/revendication/templates/revendications/fichier_data.json", "w")
	fichier_data.write(data)
	fichier_data.close()

	utilisateur= request.user
	
	return render (request, 'revendications/consulter.html', {"choix_menu": "consulter", 'data': data})


def data_json(request):
	
	return render(request, 'revendications/fichier_data.json')

	






def creation_utilisateur (request):
	if request.method == 'POST':
		form = UtilisateurForm(request.POST)
		if form.is_valid():
			nom = request.POST['nom']
			mot_de_passe = request.POST['mot_de_passe']
			mail = request.POST['mail']
			utilisateur = User.objects.create_user(nom, mail, mot_de_passe)
			autre_utilisateur = Autre_utilisateur.objects.create(user = utilisateur)
			profile = Profile.objects.create (utilisateur = utilisateur, organisation = False)

			return render(request, 'revendications/merci.html')
	else:
			form = UtilisateurForm()
	
	return render(request, 'revendications/creation_utilisateur.html', {'form': form, "choix_menu":"adhesion"})
	

def militer (request):
	#champ_lexical_des_propositions()

	return render (request, 'revendications/militer.html', {"choix_menu": "militer"})	

def organiser (request):
	return render (request, 'revendications/organiser.html', {"choix_menu": "organiser"})
		


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
				return render (request, 'revendications/accueil.html')	
			else:
				error = True
		else:
			form = AuthentificationForm()

	form = AuthentificationForm(request.POST)		
	return render(request, 'revendications/authentification.html', {'form': form, "choix_menu":"authentification"})


def merci (request):
	return render(request, 'revendications/merci.html')

def message (request, message):
	return render(request, 'revendications/message.html', {'message': message})


def deconnexion (request):
	from django.contrib.auth import logout
	from django.shortcuts import render
	from django.core.urlresolvers import reverse
	logout(request)
	return render(request, 'revendications/accueil.html', {"utilisateur":"inconnu"})

def accueil(request):
	from django.contrib.auth.models import User
	utilisateur = request.user.username
	print ("voici l'utilisateur" , utilisateur)
	return render(request, 'revendications/accueil.html', {"utilisateur":utilisateur})


def afficher_accueil_revendiquer (request):
	return render (request, 'revendications/accueil_revendiquer.html')



def mes_revendications (request):
	#supprimer_les_propositions_doublons()
	utilisateur = request.user
	propositions = Proposition.objects.filter(soutien__user= utilisateur).filter(soutien__lien = 'CR')
	propositions2 = Proposition.objects.filter (soutien__user= utilisateur)


	
	#classer_les_proximites):
	profile = Profile.objects.get(utilisateur =utilisateur)
	print ("profile concerné :{0}".format (profile))
	proximites = Proximite.objects.filter(profile = profile).exclude(Autre_utilisateur__user = utilisateur)
	ancienne_proba_max = 1
	ancien_utilisateur_prefere = utilisateur
	for proximite in proximites:
		print ("proximite concernée :{0}".format (proximite))
		if proximite.proba < ancienne_proba_max:
			ancienne_proba_max = proximite.proba
			ancien_utilisateur_prefere = proximite.Autre_utilisateur.user
			print ("ancien_utilisateur_prefere :{0}".format (ancien_utilisateur_prefere))
	utilisateur_le_plus_proche = ancien_utilisateur_prefere
	propositions_interessantes = Proposition.objects.filter(soutien__user = utilisateur_le_plus_proche).exclude(soutien__user = utilisateur)
	for proposition in propositions_interessantes:
		print ("proposition interessante: {0}".format(proposition.ennonce))

	print ("propositions interessantes :{0}".format(propositions_interessantes))
	return render (request, 'revendications/mes_revendications.html', {"propositions" : propositions, "propositions2" : propositions2, 'choix_menu': "militer", "propositions_interessantes": propositions_interessantes , "utilisateur_le_plus_proche": utilisateur_le_plus_proche})
	

def affiche(mot):
	print ("voici l'élément demandé : {0}".format(mot))


def creer_une_revendication (request):


	utilisateur= request.user
	
	if request.method == 'POST':
		form = RevendicationForm(request.POST)

		if form.is_valid() :
			
			#si le theme n'existait pas, on en crée un, on l'enregistre et on le garde en variable	
			if request.POST["theme_existant"] == "aucun":
				intitule_du_theme = request.POST["nouveau_theme"]
				theme = Theme (intitule = intitule_du_theme)
				liste_des_themes_existants = Theme.objects.filter(intitule = intitule_du_theme)
				for element in liste_des_themes_existants:
					element.delete()
				theme.save()
			
			#si le thème existait, on le récupère en variable
			else:
				theme = Theme.objects.get(intitule = request.POST["theme_existant"])
			
			#on crée la proposition avec le thème en variable 
			la_proposition = Proposition.objects.create(ennonce = request.POST["intitule"], categorie=theme) 
			la_proposition.save()
			le_soutien = Soutien.objects.create(user=utilisateur, propositions = la_proposition, lien= 'CR')
			le_soutien.save()
			print ("soutien ajouté:{0} ".format(la_proposition.supporter))
			request.path = "revendications/mes_revendications.html"

			#on affiche la page "mes revendications"
			utilisateur = request.user
			propositions = Proposition.objects.filter(soutien__user= utilisateur)
			propositions2 = Proposition.objects.filter (soutien__user = utilisateur)
			num = 0
			return render (request, 'revendications/mes_revendications.html', {"propositions" : propositions, "propositions2" : propositions2, 'choix_menu': "militer", 'num':num})		
			
	else:
		form = RevendicationForm()
		return render(request, 'revendications/creer_une_revendication.html', {'form': form})
	


def consult_revendications (request):
	propositions = Proposition.objects.all

	return render (request, 'revendications/consult_revendications.html', {"propositions" :propositions})

def proposition_detail (request, id_proposition):
	# Vérification identifiant valide ? si non, 404
	try:
		proposition = Proposition.objects.get(id = id_proposition)
	except Proposition.DoesNotExist:
		raise Http404

	soutien= Soutien.objects.filter(propositions__id = id_proposition).filter(lien ='SO')
	createur= Soutien.objects.filter(propositions__id = id_proposition).filter(lien = 'CR')
	evenement = Evenement.objects.filter(proposition_id = id_proposition)
	petitions = proposition.petition_set.all()

	print (proposition)
	print (createur)
	return render (request, 'revendications/proposition_detail.html', {"createur" :createur, "proposition" :proposition, "soutien" :soutien, "evenement": evenement, "petitions": petitions})	


def soutenir_une_revendication (request, id_proposition):
	# Vérification identifiant valide ? si non, 404
	try:
		proposition = Proposition.objects.get(id = id_proposition)
	except Proposition.DoesNotExist:
		raise Http404

	utilisateur = request.user

	Soutien.objects.get_or_create(propositions = proposition, user= utilisateur, lien='SO')
	
	#request.path ="revendications/consult_revendications.html"
	
	propositions = Proposition.objects.all

	return render (request, 'revendications/consult_revendications.html', {"propositions" :propositions})



def afficher_mon_profil (request):
	
	def creer_objet_profil_utilisateur (request):
		utilisateur = request.user
		propositions_soutenues = Proposition.objects.filter (soutien__user= utilisateur)
		militantisme = Militant.objects.filter (utilisateur = utilisateur)
		documents = "vide"
		organisations = "vide"
		actualites = "vide"
		suggestions = "vide"

		class Profil:
			
			def __init__ (self, utilisateur, propositions_soutenues, documents, organisations, actualites, suggestions):
				self.utilisateur = utilisateur
				self.revendications = propositions_soutenues
				self.documents = documents
				self.organisations = militantisme
				self.actualites= actualites
				self.suggestions = suggestions

		profil = Profil(utilisateur, propositions_soutenues, documents, organisations, actualites, suggestions)
		return profil

	profil = creer_objet_profil_utilisateur (request)
	return render (request, 'revendications/afficher_mon_profil.html', {"profil" :profil})


"""

	ORGANISATIONS (#organisations)

"""

def creer_une_organisation (request):
	if request.method == 'POST':
		form = OrganisationForm(request.POST)
		if form.is_valid():
			nom = request.POST['nom']
			mot_de_passe = request.POST['mot_de_passe']
			mail = request.POST['mail']
			description = request.POST['description']
			organisation = True
			utilisateur = User.objects.create_user(nom, mail, mot_de_passe)
			#autre_utilisateur = Autre_utilisateur.objects.create(user = utilisateur)
			profile = Profile.objects.create (utilisateur = utilisateur)
			organisation = Organisation.objects.create (profile = profile, description= description)
		

			return render(request, 'revendications/merci.html')
	else:
			form = OrganisationForm()
	
	return render(request, 'revendications/creer_une_organisation.html', {'form': form, "choix_menu":"adhesion"})


def afficher_une_organisation (request):

	id_organisation = request.GET['id_organisation']
	utilisateur = User.objects.get (id = id_organisation)
	profil = Profile.objects.get(utilisateur = utilisateur)
	organisation = Organisation.objects.get(profile = profil)


	print ("la description est  : {}".format(organisation.description))
	
	return render(request, 'revendications/afficher_une_organisation.html', {'organisation': organisation, 'profil': profil})



def adherer_a_une_organisation (request, id_organisation):
	# Vérification identifiant valide ? si non, 404
	try:
		organisation = Organisation.objects.get(id = id_organisation)
	except Organisation.DoesNotExist:
		raise Http404


	utilisateur = request.user
	
	soutien = Soutien.objects.get_or_create(organisation = organisation, user = utilisateur, lien = 'SO')
	organisation.soutien = soutien
	organisation.save()

	organisations = Organisation.objects.all

	return render (request, 'revendications/consult_organisations.html', {"organisations" :organisations})
	


def consulter_les_organisations (request):
	organisations = Organisation.objects.all

	return render (request, 'revendications/consult_organisations.html', {"organisations" :organisations})
	


def mes_organisations (request):
	utilisateur = request.user
	organisations = Organisation.objects.filter(soutien__user=utilisateur)
	print ("voici la liste des organisations : {}".format(organisations))
	
	return render(request, 'revendications/mes_organisations.html', {'organisations': organisations})


"""

	EVENEMENTS (#evenements)

"""

def creer_un_evenement (request):
	"""
	# Vérification identifiant valide ? si non, 404
	try:
		petition = Petition.objects.get(id = id_petition)	
	except Petition.DoesNotExist:
		raise Http404
	id_proposition = request.GET['id_proposition']
	"""

	if request.method == 'POST':
		form = EvenementForm(request.POST)
		if form.is_valid():
			lieu = request.POST['lieu']
			date = request.POST['date']
			description = request.POST['description']
			titre = request.POST['titre']
			id_proposition = request.GET['id_proposition']
			proposition = Proposition.objects.get(id = id_proposition)
				

			createur = request.user
		
			evenement = Evenement.objects.create (date = date, description = description, proposition =proposition, titre = titre)
			evenement.save()
			soutien = Soutien.objects.create (evenement = evenement, user = createur, lien = 'CR')
			soutien.save()


			return render(request, 'revendications/merci.html')
	else:
		id_proposition = request.GET['id_proposition']
		form = EvenementForm()
	
	print ("voici le formulaire = {}".format(form))

	return render(request, 'revendications/creer_un_evenement.html', {'form': form, 'id_proposition':id_proposition})

	
def detail_evenement(request, id_evenement):
	# Vérification identifiant valide ? si non, 404
	try:
		evenement = Evenement.objects.get(id = id_evenement)
	except Evenement.DoesNotExist:
		raise Http404


	participants= Soutien.objects.filter(evenement = evenement, lien= 'SO')

	print ("l'evenement est {}".format(evenement))

	return render(request, 'revendications/detail_evenement.html', {'evenement': evenement, 'participants':participants})



def participer_a_un_evenement (request):
	id_evenement = request.GET['id_evenement']
	signataire = request.user
	# Vérification identifiant valide ? si non, 404
	try:
		evenement = Evenement.objects.get(id = id_evenement)
	except Evenement.DoesNotExist:
		raise Http404

	participants= Soutien.objects.filter(evenement = evenement, lien = 'SO')
	utilisateur = request.user
	soutien = Soutien.objects.get_or_create(evenement= evenement, user = utilisateur, lien = 'SO')
	evenement.save()

	organisations = Organisation.objects.all


	#verifier si l'utilisateur est déjà participant et préparer un message d'alert le cas échéant
	for participant in participants:

		if participant.user == utilisateur:
			print ("ca match")
			message = "vous participez déjà à cet évenement"
			break
		else:
			message = "Vous participez désormais à cet évenement"

	print (message)

	return render (request, 'revendications/detail_evenement.html', {'evenement': evenement, 'participants':participants, 'message': message})


def mes_evenements(request):
	utilisateur = request.user
	evenements = Evenement.objects.filter(participants=utilisateur, soutien__lien = 'SO')
	print ("voici la liste des evenements : {}".format(evenements))
	
	return render(request, 'revendications/mes_evenements.html', {'evenements': evenements})


"""

	PETITION (#petition)

"""	

def creer_une_petition(request):
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
		form = PetitionForm(request.POST)
		if form.is_valid():
			#
			# Traitement du formulaire valide
			#
			titre = form.cleaned_data['titre']
			description = form.cleaned_data['description']
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

			if not propositions:
				return render(request, 'revendications/message.html', {'message':"Cocher au moins une proposition !"})

			

			"""
			"""
			# Création de la pétition puis association à la proposition source
			petition = Petition.objects.create(titre=titre, description=description, date_echeance=date_echeance, objectif_de_signataires=objectif_de_signataires)

			for i in propositions:
				petition.propositions.add(i)
			
			#petition.propositions.add(proposition)
			petition.save()

			# Création de la relation de soutient (CR) entre l'user et la pétition
			soutien = Soutien.objects.create(petition = petition, user = user, lien = 'CR')

			# Retour sur la page de la pétition créée -> !ToDo
			"""
			return render(request, 'revendications/merci.html')
			"""
			return render(request, 'revendications/message.html', {'message':"Pétition correctement créée... enfin, j'espère..."})

	else:
		#
		# Pas de formulaire reçu...
		#

		form = PetitionForm()
		revendications_soutenues = Proposition.objects.filter(soutien__user = user)
	
		return render(request, 'revendications/creer_une_petition.html', {'form': form, 'id_proposition':id_proposition, 'revendications_soutenues':revendications_soutenues})

def supprimer_une_petition(request, id_petition):
	# Vérification identifiant valide ? si non, 404
	try:
		petition = Petition.objects.get(id = id_petition)	
	except Petition.DoesNotExist:
		raise Http404

	# Vérification de l'authentification utilisateur, redirection sinon
	#   -> voir https://docs.djangoproject.com/fr/1.10/topics/auth/default/#the-login-required-decorator
	if request.user.is_authenticated:
		user = request.user
	else:
		return render(request, 'authentification_necessaire.html')



	# Vérification que l'utilisateur est bien le créateur de la pétition
	try:
		soutien = Soutien.objects.get(user = user, petition = petition, lien = 'CR')
	except Soutien.DoesNotExist:
		return render(request, 'revendications/message.html', {'message': "Vous ne pouvez pas supprimer cette pétition, vous n'en êtes pas le créateur."})

	
	# La confirmation de suppression a-t-elle été envoyée ?
	if request.method == 'POST':
		petition.delete()
		return render(request, 'revendications/message.html', {'message': "La pétition a bien été supprimée !"})
	else:
		return render(request, 'revendications/supprimer_une_petition.html', {'petition': petition})


def detail_petition(request, id_petition):
	# Vérification identifiant valide ? si non, 404
	try:
		petition = Petition.objects.get(id = id_petition)	
	except Petition.DoesNotExist:
		raise Http404
	
	propositions = petition.propositions.all()
	signataires = Soutien.objects.filter (petition = petition)


	print ("la pétition est {}".format(petition))

	return render(request, 'revendications/detail_petition.html', {'petition': petition, 'propositions': propositions, 'signataires': signataires})


def signer_une_petition(request):
	id_petition = request.GET['id_petition']
	signataire = request.user

	# Vérification identifiant valide ? si non, 404
	try:
		petition = Petition.objects.get(id = id_petition)	
	except Petition.DoesNotExist:
		raise Http404

	soutien = Soutien.objects.get_or_create(petition = petition, user = signataire, lien='SO')

	propositions = petition.propositions.all()
	signataires = Soutien.objects.filter(petition = petition)

	return render(request, 'revendications/detail_petition.html', {'petition': petition, 'propositions': propositions, 'signataires': signataires})


def mes_petitions(request):
	utilisateur = request.user
	petitions_crees = Petition.objects.filter(soutien__user=utilisateur, soutien__lien='CR')
	petitions_soutenues = Petition.objects.filter(soutien__user=utilisateur)

	return render(request, 'revendications/mes_petitions.html', {'petitions_crees': petitions_crees, 'petitions_soutenues':petitions_soutenues})


"""

	Graphe des propositions

"""

def afficher_le_graph_des_propositions(request):

	import networkx as nx


	def creer_un_dictionnaire_proposition_soutiens (propositions):
		dictionnaire_des_propositions = {}
		
		for proposition in propositions :
			soutiens = Soutien.objects.filter(propositions__id = proposition.id)
			soutiensl = []
			for soutien in soutiens:
				soutiensl.append(soutien.user)
			soutiens = soutiensl
			dictionnaire_des_propositions[proposition.id]=soutiens
		
		#print ("dictionnaire : {}".format(dictionnaire_des_propositions))
		return dictionnaire_des_propositions



	def lister_les_couples_de_proposition(propositions):
		liste_des_couples = []
		for proposition1 in propositions:
			for proposition2 in propositions:
				if proposition1 != proposition2:
					couple = (proposition1, proposition2)
					liste_des_couples.append(couple)
		return liste_des_couples




	def nb_utilisateur_communs_de_2_propositions(proposition1, proposition2, dictionnaire_des_propositions):
		liste_commune = []
		soutiens1 = dictionnaire_des_propositions[proposition1.id]
		#print ("soutiens1 : {}".format(soutiens1))
		soutiens2 = dictionnaire_des_propositions[proposition2.id]
		#print ("soutiens2 : {}".format(soutiens2))
		for soutien_a in soutiens1:
			#print ("soutiena : {}".format(soutien_a))
			for soutien2 in soutiens2:
				#print ("soutient2 : {}".format(soutien2))
				if soutien_a == soutien2:
					#print ("ca appartient")
					liste_commune.append(soutien_a)
					#print("liste commune : {}".format(liste_commune))
			#else:		
				#print ("ca n'appartient pas")
		#print ("nombre d'utilisateur commun : {}".format(len(liste_commune)))
		return len(liste_commune)




	def creer_les_noeuds(G, propositions):
		for proposition in propositions:
			G.add_node(proposition)


	def creer_les_liens (G, liste_des_couples, dictionnaire_des_propositions):
		for couple in liste_des_couples:
			force = nb_utilisateur_communs_de_2_propositions(*couple, dictionnaire_des_propositions)
			print ("************************** couple : {}, force : {}".format(couple, force))
			if force != 0:
				G.add_edge(*couple, weight = force)
			
	G = nx.Graph()
	propositions = Proposition.objects.all()
	dictionnaire_des_propositions = creer_un_dictionnaire_proposition_soutiens(propositions)
	liste_des_couples = lister_les_couples_de_proposition(propositions)

	creer_les_noeuds(G, propositions)
	creer_les_liens (G, liste_des_couples, dictionnaire_des_propositions)

	nx.write_gexf(G, "propositions.gexf")









