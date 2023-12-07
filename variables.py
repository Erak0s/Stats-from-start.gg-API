from datetime import *

# URL de l'API de start.gg
url = "https://api.start.gg/gql/alpha"

# Token d'authentification
headers = {
  "Authorization": "Bearer 3622a9c31282bd7cea09d8c9874f18c4"
}

today = int(datetime.now().timestamp())

############
## Listes ##
############

cCodes={"France":"FR",
        "Japon":"JP",
        "Etats-Unis":"US",
        "Autriche":"AT"
        }

ville_coord={"Montpellier":"43.604652,3.907186",
             "Paris":"48.854461, 2.352326",
             "Toulouse":"43.604440, 1.444205",
             "Nimes":"43.836047, 4.359866"
             }

game_Ids={"Super Smash Bros. Ultimate":"1386",
          "Super Smash Bros. Melee":"1",
          "Street Fighter 6":"43868",
          "DRAGON BALL FighterZ":"287",
          "Rivals of Aether":"24",
          "Rivals 2":"53945"
          }
