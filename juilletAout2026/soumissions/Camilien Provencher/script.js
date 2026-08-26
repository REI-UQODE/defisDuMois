// Par Camilien, pour le défi du mois d'été Markdown :-)
// J'ai utilisé l'addon prettier pour que le code soit mieux organisé

// Affiche le texte de l'éditeur sur preview
const editor = document.getElementById("editor");
const preview = document.getElementById("preview");
editor.addEventListener("input", () => {
  preview.innerHTML = MarkdownLigne(editor.value); //  innerHTML est pour afficher l'html, j'ai précédement utilisé textContent mais innerHTML était meilleur dans ce contexte
});

// =====================================================================
// pour ne pas sortir avec tab
// SOURCE : https://stackoverflow.com/questions/6637341/use-tab-to-indent-in-textarea
// =====================================================================
editor.addEventListener("keydown", (event) => {
  if (event.key === "Tab") {
    event.preventDefault();
    const debut = editor.selectionStart;
    const fin = editor.selectionEnd;
    editor.value =
      editor.value.substring(0, debut) + "\t" + editor.value.substring(fin);
    editor.selectionStart = debut + 1;
    editor.selectionEnd = debut + 1;

    // preview à jour
    editor.dispatchEvent(new Event("input"));
  }
});
// =====================================================================
// Fin du code repris de kasgeda :)
// =====================================================================

/* Il y a deux grosse logique. 
1. Je traite les lignes (à la recherche de symboles comme # pour un titre en startant une ligne) (MarkdownLigne)
2. Des regex sur les textes (exemple, *italique*, voir comme sur Discord) (MarkdownText)*/
function MarkdownLigne(markdown) {
  const lignes = markdown.split("\n"); // tableau de lignes
  let html = "";

  // Gère, dans l'ordre, les backtics, le code indenté, les titres, les listes, les numbered listes et les ligne vide.
  // était autrefois  for(const ligne of lignes), mais ça ne prenais pas en compte le nombre de ligne
  for (let i = 0; i < lignes.length; i++) {
    const ligne = lignes[i];

    // 3 BACKTICS (bloc de code)
    if (ligne.trim() === "```") {
      html += "<pre><code>";
      i++;

      // toutes les lignes jusquau prochain ```
      while (i < lignes.length && lignes[i].trim() !== "```") {
        html += lignes[i];
        html += "\n";
        i++;
      }
      html += "</code></pre>";
      continue;
    }

    // INDENTÉ (tab)
    if (ligne.startsWith("\t")) {
      // retrait de tab comme d'hab
      const texte = ligne.substring(1);
      html += `<pre><code>${texte}</code></pre>`;
      continue;
    }

    // TITRE (#)
    if (ligne.startsWith("#")) {
      // je compte le nombre de #, je me fie à la logique html de titre H1/2/3 etc
      let h = 0;
      while (h < ligne.length && ligne[h] === "#") {
        h++;
      }
      // il doit avoir entre 1-6 '#', un espace aussi
      if (h >= 1 && h <= 6 && ligne[h] === " ") {
        const texte = ligne.substring(h + 1);
        html += `<h${h}>${MarkdownText(texte)}</h${h}>`;
        continue;
      }
    }

    // LISTE (- / *)
    if (
      ligne.trimStart().startsWith("- ") ||
      ligne.trimStart().startsWith("* ")
    ) {
      html += "<ul>"; // début de liste
      // on fait tous les éléments
      while (i < lignes.length) {
        const element = lignes[i];
        // je cleanup l'espace/tab et ensuite */-
        const texteElement = element.trimStart();
        if (
          !texteElement.trimStart().startsWith("- ") &&
          !texteElement.startsWith("* ")
        ) {
          break;
        }
        const espacesElement = element.length - element.trimStart().length;

        // jamais besoin des deux premiers caractères
        const texte = element.trimStart().substring(2);
        // début du li (termine plus bas)
        html += `<li>${MarkdownText(texte)}`;

        // je joue avec i au niveau du for principal, du for d'éléments et de la sous-liste*/
        if (i + 1 < lignes.length) {
          const prochaine = lignes[i + 1];
          const texteProchaine = prochaine.trimStart();
          const espacesProchaine =
            prochaine.length - prochaine.trimStart().length;
          // Début sous liste (prend juste un niveau de profondeur)
          if (
            (texteProchaine.startsWith("- ") ||
              texteProchaine.startsWith("* ")) &&
            espacesProchaine > espacesElement
          ) {
            html += "<ul>";
            i++; 
            while (i < lignes.length) {
              const sousElement = lignes[i];
              const sousTexte = sousElement.trimStart();
              const sousEspaces =
                sousElement.length - sousElement.trimStart().length; // dédicace à la fois que j'ai écris socus au lieu de sous et que ça m'a pris 30 minutes à voir
              // fin de sous liste
              if (!sousTexte.startsWith("- ") && !sousTexte.startsWith("* ")) {
                break;
              }
              if (sousEspaces <= espacesElement) {
                break;
              }
              html += `<li>${MarkdownText(sousTexte.substring(2))}</li>`;
              i++;
            }
            html += "</ul>";
            i--;
          }
        }
        html += `</li>`;
        i++; 
      }
      html += "</ul>"; // fin du ul
      i--; // je prend e n compte le i++ du for
      continue;
    }

    // NUMBERED LIST (le ol)
    /* Le pire regex du fichier, déguelasse à lire mais pas si complex. De la recherche de pattern (voir .test)
        ^ commence ici, \s* sont les white space (voir css, espace/tab), \d chiffre entre 0 et 9, + pour plusieurs fois, 
        \. pour ., \s pour l'espace (singulier) après le numéro
    */
    if (/^\s*\d+\.\s/.test(ligne)) {
      html += "<ol>";
      while (i < lignes.length) {
        const element = lignes[i];
        // voir que la ligne est numéroitée
        const match = element.match(/^(\s*)\d+\.\s(.*)$/); // pour récupérer une partie de la ligne, le plus important est (\s*) et (.*) (groupe capturés)

        if (!match) {
          break;
        }
        const texte = match[2]; // le deuxième groupe de mon (/^(\s*)\d+\.\s(.*)$/), 1 étant l'indentation, 2 est le texte
        html += `<li>${MarkdownText(texte)}</li>`;
        i++;
      }
      html += "</ol>";
      i--;
      continue;
    }

    // LIGNE VIDE
    if (ligne.trim() === "") {
      html += "<br>";
      continue;
    }

    html += `<p>${MarkdownText(ligne)}</p>`;
  }

  return html;
}

// Source qui m'a assez aidé : https://stackoverflow.com/questions/73002812/regex-accurately-match-bold-and-italics-items-from-the-input
function MarkdownText(texte) {
  // rappel que \* est le symbole astérix
  // ***gras + italique***
  texte = texte.replace(/\*\*\*(.*?)\*\*\*/g, "<i><strong>$1</strong></i>");
  // **gras**
  texte = texte.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  // *italique*
  texte = texte.replace(/\*(.*?)\*/g, "<i>$1</i>");
  // `ptit`
  texte = texte.replace(/`(.*?)`/g, "<code>$1</code>");
  // [](lien), en deux partie mais c'est pareil hahaha
  texte = texte.replace(/\[(.*?)\]\((.*?)\)/g, '<a href="$2">$1</a>');
  return texte;
}

// Mon ancienne fonction MarkdownCaractere. Super fonctionnelle, pas compliquée, je sais même comment faire le reste, mais j'avais envie d'essayer davantage les expressions régulière. 
// Remplacée par MarkdownText.
// function MarkdownCaractere(texte){
//     let html = "";
//     for (let i = 0; i < texte.length; i++) {
//         // premier * et le prochain *
//         if(texte[i] === "*"){
//             let end = i + 1;
//             while (end < texte.length && texte[end] !== "*") {
//                 end++;
//             }
//             // * 2
//             if (end < texte.length) {
//                 const contenu = texte.substring(i+1, end);
//                 html += `<em>${contenu}</em>`;
//                 i = end;
//                 continue;
//             }
//         }
//         html += texte[i];
//     }
//     return html;
// }

// =====================================================================
// Merci au site mozilla, c'était pas la priorité, mais le chargement de fichier txt était un peu loin dans ma tête.
// Source : https://developer.mozilla.org/en-US/docs/Web/API/FileReader 
// Voir aussi la sous-page (readastext)
// =====================================================================
const loading = document.getElementById("load");

loading.addEventListener("click", () => {
  // le file select
  const inputFichier = document.createElement("input");
  inputFichier.type = "file";

  // lecture du fichier (txt ou md)
  inputFichier.addEventListener("change", () => {
    const file = inputFichier.files[0];
    if (file) {
      const lecteur = new FileReader();
      // lit le fichier, texte dans l'éditeur et mis à jour
      lecteur.onload = () => {
        editor.value = lecteur.result;
        editor.dispatchEvent(new Event("input"));
      };
      lecteur.readAsText(file); // texte lu
    }
  });
  inputFichier.click();
});
