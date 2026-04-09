public class Bot {
    public static final String NOM = "SuperJavaBot"+Long.toString(System.currentTimeMillis());
    public static final String SERVEUR_REP = null;
    public static final String ADRESSE = "http://127.0.0.1:5000";

    public Bot(){}

    public boolean tour(ÉtatJeu jeu){
        System.out.println(jeu);
        // Vous pouvez faire mieux ;)
        return Math.random() > 0.5;
    }
}
