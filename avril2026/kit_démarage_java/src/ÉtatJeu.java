import java.util.HashMap;

import org.json.JSONArray;
import org.json.JSONObject;

public class ÉtatJeu {
    public String[] erreurs;
    public String[] joueurs;
    public HashMap<String,JoueurInfos> joueurs_info;

    public class JoueurInfos{
        public int points;
        public int points_obtenus;
        public boolean action;
    }

    public void extraire(JSONObject json){
        JSONArray erreursJson = json.getJSONArray("erreurs");
        this.erreurs = new String[erreursJson.length()];
        for (int i = 0; i < erreursJson.length(); i++) {
            this.erreurs[i] = erreursJson.getString(i);
        }
        
        JSONArray joueursJson = json.getJSONArray("joueurs");
        this.joueurs = new String[joueursJson.length()];
        for (int i = 0; i < joueursJson.length(); i++) {
            this.joueurs[i] = joueursJson.getString(i);
        }

        JSONObject joueurs_infos_json = json.getJSONObject("joueurs_info");
        if(joueurs_info == null){
            joueurs_info = new HashMap<>();
        }
        joueurs_info.clear();

        for (String k : joueurs_infos_json.keySet()) {
            JSONObject joueurJson = joueurs_infos_json.getJSONObject(k);
            JoueurInfos joueur = new JoueurInfos();

            joueur.points = joueurJson.getInt("points");
            joueur.points_obtenus = joueurJson.getInt("points_obtenus");
            joueur.action = joueurJson.getBoolean("action");

            joueurs_info.put(k,joueur);
        }
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder();
        String erreurs_str = "";
        if (this.erreurs != null){
            for (String erreur : this.erreurs) {
                builder.append("\t\t\""+erreur+"\",\n");
            }
            erreurs_str = '\n'+builder.toString();
        }

        String joueurs_str = "";
        if(this.joueurs != null){
            builder.replace(0, builder.length(), "");
            for (String nom : joueurs) {
                builder.append("\t\t\""+nom+"\",\n");
            }
            joueurs_str = '\n'+builder.toString();
        }

        String joueurs_infos_str = "";
        if(this.joueurs_info != null){
            builder.replace(0, builder.length(), "");
            for (String k : joueurs_info.keySet()) {
                builder.append(
                    "\t\t"+k+": {\n"+
                    "\t\t\t\"points\": "+joueurs_info.get(k).points+",\n"+
                    "\t\t\t\"points_obtenus\": "+joueurs_info.get(k).points_obtenus+",\n"+
                    "\t\t\t\"action\": "+joueurs_info.get(k).action+",\n"+
                    "\t\t},\n"
                );
            }
            joueurs_infos_str = '\n'+builder.toString();
        }

        return 
        "{\n"+
        "\t\"erreurs\": ["+erreurs_str+"],\n"+
        "\t\"joueurs\": ["+joueurs_str+"],\n"+
        "\t\"joueurs_infos: {"+joueurs_infos_str+"}\n"+
        "}";
    }
}
