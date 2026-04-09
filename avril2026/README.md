Défi d'Avril : Traître.exe
==========================

Le défi du mois de mars a pour thème : Dilemme du prisonnier!

Vous pouvez voir le classemement actuel [ici](./Soumissions.md)

Le Défi du Mois
---------------

Le ***Défi du Mois*** est un défi de programmation compétitif dans lequel vous aurez à construire un programme qui répond à certains critères. Vous soumetterez votre solution et elle serat jugée selon divers critères et la meilleure solution sera courronnée gagnante du défi. Soumettez vos solution à <uqode@uqo.ca>.

![Image promotionelle](./DéfiAvril.svg)

Les règles du jeu :
-------------------

Le dilemme du prisonnier est un problème célèbre en théorie des jeux. Deux prisonniers sont arrêtés pour deux crimes : un petit et un grave. En interrogatoire, ils se voient offerts une porte de sortie : si l'un d'eux trahis l'autre, sa petite peine lui sera pardonnée. La question est alors : faire confiance et risquer de se faire accuser pour le crime grave ou trahir et s'assurer la liberté? Les prisonniers font ainsi face à la matrice de décision suivante : 

|              | Faire Confiance                      | Trahir                              |
|--------------|:------------------------------------:|:-----------------------------------:|
| Est Confiant | 1 ans de prison pour le petit crime  | libertée                            |
| Trahit       | 5 ans de prison pour les deux crimes | 4 ans de prison pour le crime grave |

Il peut sembler que la meilleure option pour le groupe est de collaborer, mais individuellement il est toujours plus avantageux de trahir que de collaborer ([plus d'information ici](https://fr.wikipedia.org/wiki/Dilemme_du_prisonnier)).

Ce dilemme peut être formulé de diverses façons, dans le défi de ce mois-ci vous êtes des compétiteurs dans un jeu télévisé où vous pouvez trahir ou collaborer pour gagner plus ou moins d'argent. De plus, cette édition vous vois compétitionner à trois et sur 250 tours. À chaque tours, vous avez le choix de collaborer ou de trahir. Votre jeu est simulé contre chaque compétiteur, gagnant ou perdant quelques dollars dans chaque confrontations. Votre objectif est de gagner le plus d'argent possible sur les 250 tours.

Comment participer : 
---------------------

Téléchargez le défi d'Avril 2026 de ce répo. Vous y trouverez trois dossiers : `serveur_src`, `kit_démarrage_python` `kit_démarrage_java`. Cette architecture client-serveur vous permet d'utiliser le langage de programmation de votre choix, cependant pour faciliter l'utilisation, une base de fonctionnement vous est fournie en Python et en Java.

Pour commencer, exécutez le serveur python situé dans `serveur_src`. Vous y trouverez la documentation nécessaire pour créer votre propre client si vous le souhaitez.

Ensuite, si vous souhaitez utiliser Java, n'oubliez pas d'inclure la bibliothèque dans le dossier `kit_démarrage_java/lib` dans votre CLASSPATH pour le projet. Vous aurez à connecter trois instances pour lancer la partie.

Finalement, lancez soit le client Java, soit le client Python. Dans tous les cas, vous n'aurez qu'à modifier le fichier `bot.py` ou `Bot.java`.

Chaque tour, votre fonction aura accès à l'état du jeu, formulé comme ceci :

```json
{
    "erreurs":[ // Liste des erreurs du serveur du dernier tours
        "<message>",
        "<message>",
        ...
    ],
    "joueurs":[/*Liste des noms des joueurs*/],
    "joueurs_info":{
        "<nom_joueur>":{
            "points":"<int>", // Points totaux du joueur
            "points_obtenus":"<int>", // Points obtenus dans le dernier tour
            "action":[true,false], // Action prise dans le dernier tour. True = A collaboré, False = A trahis
        },
        ...
    }
}
```

Et vous n'aurez qu'à répondre par vrai ou faux, vrai étant une collaboration et faux étant une trahison.

Les règles du défi : 
-----------------------

Soumettez vos solutions à <uqode@uqo.ca>.

- Faites un programme pour jouer au connect 4, tel que décrit ci-haut, dans le langage de programmation de votre choix.
- Les équipes sont permises. Informez-nous en clairement, s'il-vous plaît.
- Fournissez le code source de votre soumission.
- Fournissez une documentation claire et précise pour exécuter et/ou compiler votre programme. 
    - **TESTEZ CES INSTRUCTIONS SUR UN COLLÈGUE ET UNE MACHINE VIERGE AVANT DE SOUMETTRE.** 
    - Si les instructions ne fonctionnent pas, nous vous contacterons et nous vous donnerons une et une seule chance. Nous ne déboguerons pas votre programme.
    - Indice : Utilisez une machine virtuelle pour tester l'exécution de votre programme.
- Les instructions doivent permettre d'exécuter votre programme sur une machine Windows et GNU-Linux.
- Pour les soumissions par une plateforme git, nous prendrons la branche principale comme et le commit le plus récent avant la date limite comme étant la soumission. Toute modification après la date limite sera ignorée.
- Votre soumission doit être le produit de vos efforts. Le plagiat et la fraude sont interdits. Voir [notre politique d'intégrité des soumissions](#politique-dintégrité-des-soumissions-).
- La génération de code par l'intelligence artificielle est interdite. Voir [notre politique d'intégrité des soumissions](#politique-dintégrité-des-soumissions-).

**Votre soumission sera publiée à tous, assurez-vous de ne pas inclure des informations sensibles!**

Les critères de jugement : 
------------------------------

**Toute soumission qui ne respecte pas les règles ou le thème sera éliminée.**

- *Qualité du code.* Soumettez un code clair, maintenable et documenté qui respecte les bonnes pratiques.
- *Expérience utilisateur.* Assurez-vous d'avoir de bonnes performances, une interface intuitive et des contrôles efficaces.
- *L'originalité de la solution.* Vous êtes encouragés à dépasser la description du thème, tout en restant dans l'esprit du défi proposé.
- Bien que les dépendances soient permises, plus une solution en contient, moins elle sera jugée favorablement.

Politique d'intégrité des soumissions : 
------------------------------------------

- Votre soumission doit être le fruit de votre propre travail.
    - L'utilisation du travail d'autrui n'est autorisé que si l'auteur original permet une telle utilisation et est correctement et clairement cité.
    - Le travail d'autrui ne peut pas composer plus de 30% de votre soumission (ceci exclut les composantes intégrées de votre langage).
    - L'utilisation de bibliothèques sera traitée au cas par cas. Assurez-vous que votre soumission demeure en esprit le fruit de votre travail et que la bibliothèque ne fasse pas le travail à votre place. Nous vous avertirons d'avance de notre jugement et vous donnerons une chance de rectifier le tir.
- La génération de code à l'aide de l'intelligence artificielle est interdite.
    - Si nous soupçonnons de la génération à l'intelligence artificielle, vous pourrez être disqualifiés.
    - Nous vous avertirons d'avance et vous donnerons la chance de prouver que votre travail n'a pas utilisé l'intelligence artificielle. Nous fonctionnerons sur un principe de la prépondérance de la preuve.
    - L'utilisation de l'IA à toute autre fin est permise.
- Du code copié d'un autre auteur doit être correctement et clairement cité dans le format suivant : 

    ```C++
    //  +--- Caractère de commentaire de votre langage
    //  |
    //  V
        // =====================================================================
        // Merci à <Nom de l'auteur> pour <Description du code copié> (Optionel)
        // Source : <Nom/pseudo de l'auteur>, <date d'obtention>, <URL vers la source>
        // Licence : <Nom de licence> <URL vers la licence> (S'il y a lieu)
        // =====================================================================

        void fonction_exemple(){
            // Code copié
        }

        // =================================
        // Fin du code de <Nom/pseudo de l'auteur>
        // =================================
    ```

    - Ceci inclut toute solution copiée-collée de StackOverflow, Reddit ou autre. L'intelligence artificielle et le résumé google ne sont pas citables et ne sont pas des sources.
    - Si nous soupçonnons du plagiat, vous pourrez être disqualifié.