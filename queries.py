# Une requête qui doit renvoyer les id des tournois qu'on veut analyser
get_all_events="""
query get_events($name: String!) {
 tournaments(query: {page: 1, perPage: 2, filter: {name: $name}}) {
   nodes {
     name
     events {
       name
       id
     }
   }
 }
}
"""
# Les paramètres de la requête précédente
params={
  "name": "Miss'Tech"
}

# Requête donnant les standings et les seedings de toutes les phases de l'évènement dont on passe l'id.
get_standings_seed="""
query get_standings_seed($eventId: ID!, $page: Int!, $perPage: Int!) {
  event(id: $eventId) {
    id
    name
    standings(query: {perPage: $perPage, page: $page}) {
      nodes {
        placement
        entrant {
          id
          name
        }
      }
    }
    phases {
      id
      seeds(query: {page: 1, perPage: 50}, eventId: $eventId) {
        nodes {
          id
          seedNum
          entrant {
            id
            name
          }
        }
      }
    }
  }
}
"""