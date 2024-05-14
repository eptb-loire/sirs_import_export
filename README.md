# sirs2postgis

Scripts créés par Emilie BIGORNE (Etablissement public Loire) en mai 2024.
 
Le script python permet d'exporter une base au format .tar et de la ré-importer dans la même base couchDb avec un nom différent ou dans une autre base CouchDB
Le scirpt est compilé en un exécutable autonome : sirs_import_export.exe

#sirs_import_export.py
 Saisies utilisateurs : 
 	- pour les exports : 
		- adresse du serveur sur lequel est installée la base à exporter
		- nom et mot de passe de l'administrateur général de CouchDB (avec SIRS, par défaut geouser / geopw)
		- choix de la base à exporter. Le bouton raffraichir permet de raffraichir la base après modification des champs précédents
		- choix du répertoire où stocker le fichier
	- pour les imports : 
		- adresse du serveur sur lequel est installée la base à exporter
		- nom et mot de passe de l'administrateur général de CouchDB (avec SIRS, par défaut geouser / geopw)
		- choix du fichier à importer
		- nom de la nouvelle base


Télécharger l'exécutable : https://github.com/eptb-loire/sirs_import_export/releases/tag/v1.0

