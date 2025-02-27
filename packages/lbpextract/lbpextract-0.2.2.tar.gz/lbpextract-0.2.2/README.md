# LBP Extract

Cet outil permet de convertir vos relevés de compte PDF La Banque Postale en fichiers CSV lisibles dans des logiciels de type tableur comme Excel et LibreOffice Calc.
Il vous suffit d'installer l'outil, rassembler vos PDFs dans un dossier et executer l'outil, vous aurez alors un ensemble de fichiers CSV qui apparaitront dans le dossier contenant vos relevés. 

## Assembler vos relevés de compte

 1. Créez un dossier
 2. Allez sur votre espace client -> Documents et suivi -> Relevé et documents -> Recherche avancée
 3. Choisissez un compte et une année puis cliquez sur Rechercher
 4. Téléchargez les fichiers un par un (attention à ne pas en ouvrir plusieurs à la fois au risque de voir certains fichiers ne pas correspondre au bon mois)
 5. Déplacez tous ces fichiers dans le dossier initialement créé

## Installer LBPExtract

### Sur Linux

Ouvrez un terminal en appuyant sur Ctrl + Alt + T ou en cherchant "Terminal" dans votre menu.

Assurez-vous d'avoir pip installé. Si ce n'est pas le cas, vous pouvez l'installer en utilisant la commande sudo apt install python3-pip.

Utilisez la commande suivante pour installer le package "lbpextract" depuis PyPI :

```
pip install lbpextract
```

### Sur Windows

Si vous n'avez pas installé Python, [suivez ces instructions](python-on-windows.md) d'abord.

Ouvrez l'invite de commande en appuyant sur Win + R, tapez "cmd", puis appuyez sur Entrée.

Utilisez la commande suivante pour installer le package "lbpextract" depuis PyPI :

```
pip install lbpextract
```

### Utilisation de "lbpextract"

Maintenant que vous avez installé le package "lbpextract", voici comment l'utiliser pour convertir les PDFs en fichiers CSV.

Ouvrez un terminal (sous Linux) ou l'invite de commande (sous Windows).

Naviguez vers le répertoire où se trouvent vos fichiers PDF que vous souhaitez traiter. Vous pouvez utiliser la commande `cd` pour vous déplacer dans le répertoire souhaité. Par exemple :

```
cd /chemin/vers/votre/dossier
```

Alternativement, dans l'explorateur de fichiers, vous pouvez maintenir la touche "Maj" enfoncée tout en cliquant avec le bouton droit de la souris dans le répertoire, puis choisir "Ouvrir une fenêtre de commande ici" pour ouvrir l'invite de commande.

Une fois dans le répertoire cible, vous pouvez exécuter la commande suivante pour utiliser "lbpextract" et extraire des données à partir de tous les fichiers PDF présents :

```
lbpextract *.pdf
```

Les fichiers CSV seront générés dans le même répertoire. Attention, si vous voulez recommencer l'opération (après avoir ajouté de nouveau relevés par exemple), vous devez déplacer ou supprimer les anciens fichiers CSV.
