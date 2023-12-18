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
        "Espagne":"ES",
        "Autriche":"AT"
        }

ville_coord={"Montpellier":"43.604652,3.907186",
             "Paris":"48.854461, 2.352326",
             "Toulouse":"43.604440, 1.444205",
             "Nimes":"43.836047, 4.359866",
             "Narbonne":"43.183461, 3.002915"
             }

game_Ids={"Super Smash Bros. Ultimate":"1386",
          "Super Smash Bros. Melee":"1",
          "Street Fighter 6":"43868",
          "DRAGON BALL FighterZ":"287",
          "Rivals of Aether":"24",
          "Rivals 2":"53945"
          }

tournois_sauf_flamingoat={1037013: 'The Roll’Inn#15', 1030149: 'Game of Crews', 1033029: 'Smash Downtown #19 - Smash à Lez x Meltdown', 1033454: "Miss'Tech#37", 1029130: 'The Roll’Inn#14', 1029133: "Miss'Tech#36", 1025228: 'Smash Downtown #18 - Smash à Lez x Meltdown', 1025804: "Miss'Tech#35", 1013195: 'Yggdrasil #1', 1021232: 'The Roll’Inn#13', 1021654: "Miss'Tech#34", 1016433: 'Smash Downtown #17 - Smash à Lez x Meltdown', 1016446: "Miss'Tech#33", 1011996: 'The Roll’Inn#12', 1012012: "Miss'Tech#32", 1007139: 'Smash Downtown #16 - Smash à Lez x Meltdown', 1007134: "Miss'Tech#31", 1003198: 'The Roll’Inn#11', 1002446: "Miss'Tech#30", 998559: 'Smash Downtown #15 - Smash à Lez x Meltdown', 997709: "Miss'Tech#29", 993670: "The Roll'Inn#10", 993112: "Miss'Tech#28", 988843: 'Smash Downtown #14 - Smash à Lez x Meltdown', 991376: 'La FamineGote 2', 986826: "Miss'Tech#27", 984298: 'The Roll’Inn#9', 982581: "Miss'Tech#26", 979103: 'Smash Downtown #13 - Smash à Lez x Meltdown', 974857: 'The Roll’Inn#8', 972395: "Miss'Tech #25", 969289: 'Smash Downtown #12 - Smash à Lez x Meltdown', 963898: 'The Roll’Inn#7', 959759: 'Smash Downtown #11 - Smash à Lez x Meltdown', 960038: 'Never Lose a Game', 955972: "The Roll'Inn #6", 952162: 'Smash Downtown #10 - Smash à Lez x Meltdown', 948595: "The Roll'Inn #5", 947155: "Miss'Tech #24", 944138: 'Smash Downtown #9 - Smash à Lez x Meltdown', 944136: "Miss'Tech #23", 940644: 'The Roll’Inn #4', 938859: "Miss'Tech #22", 936881: 'Smash Downtown #8 - Smash à Lez x Meltdown', 935500: "Miss'Tech #21", 932852: 'The Roll’Inn #3', 929738: 'Smash Downtown #7 - Smash à Lez x Meltdown', 928242: "Miss'Tech #20 Spécial Edition", 927588: 'Tournoi Smash Bros IUT Montpellier', 922974: "The Roll'Inn #2", 923624: "Miss'Tech #19", 920121: 'Smash Downtown #6 - Smash à Lez x Meltdown', 920118: "Miss'Tech #18", 915852: "The Roll'Inn #1", 917751: 'Miss’Tech #17', 915304: 'Smash Downtown #5 - Smash à Lez x Meltdown', 910646: "Miss'Tech #16", 911836: 'Her invitational !', 906569: "Miss'Tech #15 Spécial Edition", 901164: "Miss'Tech #14", 901171: 'Smash Downtown #4 - Smash à Lez x Meltdown', 897566: "Miss'Tech #13", 893191: 'Miss’Tech #12', 889062: "Miss'Tech #11", 885849: "Miss'Tech #10 Spécial Edition", 879995: 'Miss’Tech #9', 875863: "Miss'Tech #8", 856153: "Miss'Tech #7", 868040: 'Smash Downtown #3 - Smash à Lez x Meltdown', 855124: "Miss'Tech #6", 851926: "Miss'Tech #5", 847941: 'Smash Downtown #2 - Smash à Lez x Meltdown', 847351: 'Miss’Tech #4', 844806: 'Recover High !', 843178: "Miss'Tech #3", 838653: "Miss'Tech #2"}
tournois_sauf_flamingoatA={1037013: 'The Roll’Inn#15', 1030149: 'Game of Crews', 1033029: 'Smash Downtown #19 - Smash à Lez x Meltdown', 1033454: "Miss'Tech#37", 1029130: 'The Roll’Inn#14', 1029133: "Miss'Tech#36", 1025228: 'Smash Downtown #18 - Smash à Lez x Meltdown', 1025804: "Miss'Tech#35", 1013195: 'Yggdrasil #1', 1021232: 'The Roll’Inn#13', 1021654: "Miss'Tech#34", 1016433: 'Smash Downtown #17 - Smash à Lez x Meltdown', 1016446: "Miss'Tech#33", 1011996: 'The Roll’Inn#12', 1012012: "Miss'Tech#32", 1007139: 'Smash Downtown #16 - Smash à Lez x Meltdown', 1007134: "Miss'Tech#31", 1003198: 'The Roll’Inn#11', 1002446: "Miss'Tech#30", 998559: 'Smash Downtown #15 - Smash à Lez x Meltdown', 997709: "Miss'Tech#29", 993670: "The Roll'Inn#10", 993112: "Miss'Tech#28", 988843: 'Smash Downtown #14 - Smash à Lez x Meltdown', 991376: 'La FamineGote 2', 986826: "Miss'Tech#27", 984298: 'The Roll’Inn#9', 982581: "Miss'Tech#26", 979103: 'Smash Downtown #13 - Smash à Lez x Meltdown', 974857: 'The Roll’Inn#8', 972395: "Miss'Tech #25", 969289: 'Smash Downtown #12 - Smash à Lez x Meltdown', 963898: 'The Roll’Inn#7', 959759: 'Smash Downtown #11 - Smash à Lez x Meltdown', 960038: 'Never Lose a Game', 955972: "The Roll'Inn #6", 952162: 'Smash Downtown #10 - Smash à Lez x Meltdown', 948595: "The Roll'Inn #5", 947155: "Miss'Tech #24"}
tournois_sauf_flamingoatB={944138: 'Smash Downtown #9 - Smash à Lez x Meltdown', 944136: "Miss'Tech #23", 940644: 'The Roll’Inn #4', 938859: "Miss'Tech #22", 936881: 'Smash Downtown #8 - Smash à Lez x Meltdown', 935500: "Miss'Tech #21", 932852: 'The Roll’Inn #3', 929738: 'Smash Downtown #7 - Smash à Lez x Meltdown', 928242: "Miss'Tech #20 Spécial Edition", 927588: 'Tournoi Smash Bros IUT Montpellier', 922974: "The Roll'Inn #2", 923624: "Miss'Tech #19", 920121: 'Smash Downtown #6 - Smash à Lez x Meltdown', 920118: "Miss'Tech #18", 915852: "The Roll'Inn #1", 917751: 'Miss’Tech #17', 915304: 'Smash Downtown #5 - Smash à Lez x Meltdown', 910646: "Miss'Tech #16", 911836: 'Her invitational !', 906569: "Miss'Tech #15 Spécial Edition", 901164: "Miss'Tech #14", 901171: 'Smash Downtown #4 - Smash à Lez x Meltdown', 897566: "Miss'Tech #13", 893191: 'Miss’Tech #12', 889062: "Miss'Tech #11", 885849: "Miss'Tech #10 Spécial Edition", 879995: 'Miss’Tech #9', 875863: "Miss'Tech #8", 856153: "Miss'Tech #7", 868040: 'Smash Downtown #3 - Smash à Lez x Meltdown', 855124: "Miss'Tech #6", 851926: "Miss'Tech #5", 847941: 'Smash Downtown #2 - Smash à Lez x Meltdown', 847351: 'Miss’Tech #4', 844806: 'Recover High !', 843178: "Miss'Tech #3", 838653: "Miss'Tech #2"}

misstechs={1033454: "Miss'Tech#37", 1029133: "Miss'Tech#36", 1025804: "Miss'Tech#35", 1021654: "Miss'Tech#34", 1016446: "Miss'Tech#33", 1012012: "Miss'Tech#32", 1007134: "Miss'Tech#31", 1002446: "Miss'Tech#30", 997709: "Miss'Tech#29", 993112: "Miss'Tech#28", 986826: "Miss'Tech#27", 982581: "Miss'Tech#26", 972395: "Miss'Tech #25", 947155: "Miss'Tech #24", 944136: "Miss'Tech #23", 938859: "Miss'Tech #22", 935500: "Miss'Tech #21", 928242: "Miss'Tech #20 Spécial Edition", 923624: "Miss'Tech #19", 920118: "Miss'Tech #18", 917751: 'Miss’Tech #17', 910646: "Miss'Tech #16", 906569: "Miss'Tech #15 Spécial Edition", 901164: "Miss'Tech #14", 897566: "Miss'Tech #13", 893191: 'Miss’Tech #12', 889062: "Miss'Tech #11", 885849: "Miss'Tech #10 Spécial Edition", 879995: 'Miss’Tech #9', 875863: "Miss'Tech #8", 856153: "Miss'Tech #7", 855124: "Miss'Tech #6", 851926: "Miss'Tech #5", 847351: 'Miss’Tech #4', 843178: "Miss'Tech #3", 838653: "Miss'Tech #2"}
bars={1037013: 'The Roll’Inn#15', 1029130: 'The Roll’Inn#14', 1021232: 'The Roll’Inn#13', 1011996: 'The Roll’Inn#12', 1003198: 'The Roll’Inn#11', 993670: "The Roll'Inn#10", 984298: 'The Roll’Inn#9', 974857: 'The Roll’Inn#8', 963898: 'The Roll’Inn#7', 955972: "The Roll'Inn #6", 948595: "The Roll'Inn #5", 940644: 'The Roll’Inn #4', 932852: 'The Roll’Inn #3', 922974: "The Roll'Inn #2", 915852: "The Roll'Inn #1",1033029: 'Smash Downtown #19 - Smash à Lez x Meltdown', 1025228: 'Smash Downtown #18 - Smash à Lez x Meltdown', 1016433: 'Smash Downtown #17 - Smash à Lez x Meltdown', 1007139: 'Smash Downtown #16 - Smash à Lez x Meltdown', 998559: 'Smash Downtown #15 - Smash à Lez x Meltdown', 988843: 'Smash Downtown #14 - Smash à Lez x Meltdown', 979103: 'Smash Downtown #13 - Smash à Lez x Meltdown', 969289: 'Smash Downtown #12 - Smash à Lez x Meltdown', 959759: 'Smash Downtown #11 - Smash à Lez x Meltdown', 952162: 'Smash Downtown #10 - Smash à Lez x Meltdown', 944138: 'Smash Downtown #9 - Smash à Lez x Meltdown', 936881: 'Smash Downtown #8 - Smash à Lez x Meltdown', 929738: 'Smash Downtown #7 - Smash à Lez x Meltdown', 920121: 'Smash Downtown #6 - Smash à Lez x Meltdown', 915304: 'Smash Downtown #5 - Smash à Lez x Meltdown', 901171: 'Smash Downtown #4 - Smash à Lez x Meltdown', 868040: 'Smash Downtown #3 - Smash à Lez x Meltdown', 847941: 'Smash Downtown #2 - Smash à Lez x Meltdown'}


test={1029133: "Miss'Tech#36",838653: "Miss'Tech #2"}