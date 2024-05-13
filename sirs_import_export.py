#Créé par Emilie BIGORNE, Etablissement public Loire, mai 2024
#emilie.bigorne@eptb-loire.fr
#v 1.0
try:
	# Pour Python 2
	from Tkinter import * 
	from Tkinter import ttk
	from Tkinter import messagebox
	import Tkinter.filedialog
except ImportError:
	# Pour Python 3
	from tkinter import *
	from tkinter import ttk
	from tkinter import messagebox
	import tkinter.filedialog
import couchdb2



def exp_directory():
	krepertoire = tkinter.filedialog.askdirectory ( initialdir = TKV_Chemin.get ( ) ,  mustexist = True )
	if krepertoire : 
		TKV_Chemin.set ( krepertoire )
		print(TKV_Chemin.get())
		ttk.Label(ongexport, text="Destination : ").grid(column=0, row=8)
		ttk.Label(ongexport, text=TKV_Chemin.get()).grid(column=1, row=8)


def file_import():
	file_name = tkinter.filedialog.askopenfilename ( initialdir = TKV_Chemin.get ( )  )
	if file_name : 
		TKV_Chemin.set ( file_name )
		print(TKV_Chemin.get())
		ttk.Label(ongimport, text="Fichier à importer : ").grid(column=0, row=7)
		ttk.Label(ongimport, text=TKV_Chemin.get()).grid(column=1, row=7)

def connect_couchdb():
	serveur=ip.get()
	user=usersirs.get()
	pw=pwdsirs.get()
	print(serveur)
	couch_serveur = couchdb2.Server('http://{}:{}@{}:5984/'.format(user, pw,serveur))
	try :
		print(couch_serveur)
		testcouchdb=True
		
	except:
		print('connexion couchDB échouée ' + serveur)
		testcouchdb=False
		listebase.insert(0,"aucune base trouvée")
	print(testcouchdb)
	if testcouchdb==True:
		liste_base(couch_serveur)
		return(couch_serveur)

def connect_couchdb_import():
	checknewbase=True
	serveur=ip.get()
	user=usersirs.get()
	pw=pwdsirs.get()
	couch_serveur = couchdb2.Server('http://{}:{}@{}:5984/'.format(user, pw,serveur))

	try :
		print(couch_serveur)
		testcouchdb=True
	except:
		print('connexion couchDB échouée ' + serveur)
		testcouchdb=False
	if testcouchdb==True:
		#verif que le nom de la base est saisi
		if len(nombase.get())==0 :
			tkinter.messagebox.showerror('Import base SIRS', 'Il faut saisir un nom de base')
		else:
			chemin=TKV_Chemin.get()
			#verif si une base du meme nom existe déjà
			for db in couch_serveur:
				if str(db)==nombase.get():
					tkinter.messagebox.showerror('Import base SIRS', 'La base de données existe déj, aucun import effectué')
					checknewbase=False
					
			#si nom base ok, création et import
			if checknewbase==True:
				try:
					dbsvg= couch_serveur.create(nombase.get()) 
					dbsvg.undump(chemin, callback=None, progressbar=False)
					tkinter.messagebox.showinfo('Import base SIRS', 'Import terminé')
					root.destroy()
				except:
					tkinter.messagebox.showerror('Import base SIRS', 'Erreur, Aucun import effectué')

def liste_base(couch_serveur):
	i=0
	for db in couch_serveur:
		listebase.insert(i,db)
		i=i+1

def export_base():
	couch_serveur=connect_couchdb()
	if couch_serveur is None:
		ttk.Button(ongexport, text="OK", command=tkinter.messagebox.showerror('Export base SIRS', 'Erreur, pas de base de données trouvée')).grid(column=1, row=9)
	else :	
		if len(listebase.curselection())>0 and TKV_Chemin.get()!='':
			db=couch_serveur[listebase.get(listebase.curselection()[0])]
			chemin=TKV_Chemin.get()+'/svg_'+listebase.get(listebase.curselection()[0])+'.tar'
			db.dump(chemin, callback=None, exclude_designs=False, progressbar=False)
			tkinter.messagebox.showinfo('Export base SIRS', 'Export terminé')
			root.destroy()
		else:
			if TKV_Chemin.get()=='':
				tkinter.messagebox.showinfo('Export base SIRS', 'Vous n\'avez pas choisi de répertoire')
			if len(listebase.curselection())==0:
				tkinter.messagebox.showinfo('Export base SIRS', 'Vous n\'avez pas sélectionné de base')


root = Tk()
root.title('Utilitaire d''import/export de bases SIRS')
style = ttk.Style(root)

ip = StringVar() 
ip.set("localhost")
nombase=StringVar()
nombase.set("")
usersirs = StringVar() 
usersirs.set("geouser")
pwdsirs = StringVar() 
pwdsirs.set("geopw")

TKV_Chemin=  tkinter.StringVar ( )
testcouchdb=False

#onglets
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)

ongimport = ttk.Frame(notebook, width=400, height=280)
ongexport = ttk.Frame(notebook, width=400, height=280)

ongimport.pack(fill='both', expand=True)
ongexport.pack(fill='both', expand=True)

notebook.add(ongimport, text='Import')
notebook.add(ongexport, text='Export')

ttk.Label(ongexport, text="Utilitaire d'import/export de bases SIRS").grid(column=0, row=0)
#boutons d'action

#sortir
ttk.Button(ongexport, text="Sortir", command=root.destroy).grid(column=2, row=9)
ttk.Button(ongimport, text="Sortir", command=root.destroy).grid(column=2, row=9)

#export#############################################
#IP BASE
ttk.Label(ongexport, text="Adresse de la base SIRS : ").grid(column=0, row=3)
ttk.Entry(ongexport, textvariable=ip, width=30).grid(column=1, row=3)
#USER
ttk.Label(ongexport, text="Utilisateur SIRS : ").grid(column=0, row=4)
ttk.Entry(ongexport, textvariable=usersirs, width=30).grid(column=1, row=4)	
#pwd
ttk.Label(ongexport, text="pwd SIRS : ").grid(column=0, row=5)
ttk.Entry(ongexport, textvariable=pwdsirs, width=30).grid(column=1, row=5)	
#liste des bases
ttk.Label(ongexport, text="Base à exporter ").grid(column=0, row=6)
if testcouchdb==False:
	ttk.Button(ongexport, text="Raffraichir", command=connect_couchdb).grid(column=2, row=6)
listebase=Listbox(ongexport)
listebase.grid(column=1, row=6)
#destination
ttk.Button(ongexport, text="...", command=exp_directory).grid(column=1, row=7)
#OK	
try:
	print(couch_serveur)
	print('on peut y aller')
except:
	print ('base non connectée')
ttk.Button(ongexport, text="OK", command=export_base).grid(column=1, row=9)

#import#################################
#IP BASE
ttk.Label(ongimport, text="Adresse de la base SIRS : ").grid(column=0, row=3)
ttk.Entry(ongimport, textvariable=ip, width=30).grid(column=1, row=3)
#USER
ttk.Label(ongimport, text="Utilisateur SIRS : ").grid(column=0, row=4)
ttk.Entry(ongimport, textvariable=usersirs, width=30).grid(column=1, row=4)	
#pwd
ttk.Label(ongimport, text="pwd SIRS : ").grid(column=0, row=5)
ttk.Entry(ongimport, textvariable=pwdsirs, width=30).grid(column=1, row=5)	

#fichier
ttk.Button(ongimport, text="...", command=file_import).grid(column=1, row=6)
#nom de la base
ttk.Label(ongimport, text="nom de la base à créer ").grid(column=0, row=8)
ttk.Entry(ongimport, textvariable=nombase,width=30).grid(column=1, row=8)
#OK	
ttk.Button(ongimport, text="OK", command=connect_couchdb_import).grid(column=1, row=9)
	

connect_couchdb()

root.mainloop()

