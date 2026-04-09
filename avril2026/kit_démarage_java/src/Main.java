import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;

import org.json.JSONObject;

class Main{
    private static String botNom = Bot.NOM;
    private static String serveurRep = Bot.SERVEUR_REP;
    private static String adresse = Bot.ADRESSE;
    
    private static Bot bot = new Bot();
    private static ÉtatJeu dernier_tour = new ÉtatJeu();

    private static String jeton;

    private static HttpURLConnection connection;

    public static void main(String[] args){
        if(serveurRep != null){
            initServeur();
        }
        connecterServeur();
        boucle();
    }

    private static void initServeur(){
        try {
            if(System.getProperty("os.name").toLowerCase().contains("win")){
                try {
                    Runtime.getRuntime().exec(new String[]{"python", serveurRep});
                } catch (Exception e) {
                    Runtime.getRuntime().exec(new String[]{"py", serveurRep});
                }
            }else{
                Runtime.getRuntime().exec(new String[]{"python3", serveurRep});
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void connecterServeur(){
        while(true){
            try {
                // Connection
                connection = (HttpURLConnection) new URI(adresse+"/connection?nom="+botNom).toURL().openConnection();
                connection.setRequestMethod("GET");

                connection.setUseCaches(false);

                // Réponse
                if (connection.getResponseCode() != 200){
                    System.out.println(connection.getResponseCode()+": "+connection.getResponseMessage());
                    Thread.sleep(1000);
                    continue;
                }

                BufferedReader bis = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                jeton = new JSONObject(bis.readAllAsString()).getString("jeton");
                break;
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    private static void boucle(){
       
        boolean action = bot.tour(dernier_tour);
        String message = "{\"action\":"+action+"}";

        // Attendre le début de la partie
        while(true){
            try{
                // Envoyer le tour
                connection = (HttpURLConnection) new URI(adresse+"/tour").toURL().openConnection();
                connection.setRequestMethod("POST");

                connection.setUseCaches(false);
                connection.setDoOutput(true);

                connection.setRequestProperty("Authorization", "Bearer "+jeton);
                connection.setRequestProperty("Content-Type", "application/json");
                connection.setRequestProperty("Content-Length", Integer.toString(message.getBytes().length));

                DataOutputStream dos = new DataOutputStream(connection.getOutputStream());
                dos.writeBytes(message);
                dos.close();

                // Recevoir la réponse
                if (connection.getResponseCode() == 530){
                    System.out.println(connection.getResponseCode()+": "+connection.getResponseMessage());
                    Thread.sleep(100);
                    continue;
                }
                if (connection.getResponseCode() != 200){
                    System.out.println(connection.getResponseCode()+": "+connection.getResponseMessage());
                    continue;
                }

                BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                dernier_tour.extraire(new JSONObject(br.readAllAsString()));
                br.close();
                break;
            }catch(Exception e){
                e.printStackTrace();
            }
        }

        for (int i = 0; i < 250; i++) {
            System.out.println("Tour "+i);
            try {
                action = bot.tour(dernier_tour);
                message = "{\"action\":"+action+"}";

                connection =  (HttpURLConnection) new URI(adresse+"/tour").toURL().openConnection();

                connection.setRequestMethod("POST");

                connection.setUseCaches(false);
                connection.setDoOutput(true);

                connection.setRequestProperty("Authorization", "Bearer "+jeton);
                connection.setRequestProperty("Content-Type", "application/json");
                connection.setRequestProperty("Content-Length", Integer.toString(message.getBytes().length));

                DataOutputStream dos = new DataOutputStream(connection.getOutputStream());
                dos.writeBytes(message);
                dos.close();

                if (connection.getResponseCode() != 200){
                    System.out.println(connection.getResponseCode()+": "+connection.getResponseMessage());
                    continue;
                }

                BufferedReader br = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                dernier_tour.extraire(new JSONObject(br.readAllAsString()));
                br.close();
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}