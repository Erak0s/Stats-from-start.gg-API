# Une requête qui doit renvoyer les id des tournois qu'on veut analyser
get_all_events_location="""
query get_events_loc($name: String, $cCode: String, $distance: String, $city: String, $perPage: Int) {
  tournaments(
    query: {perPage: $perPage, filter: {name: $name, countryCode: $cCode, location: {distanceFrom: $city, distance: $distance}}}
  ) {
    nodes {
      name
      countryCode
      postalCode
      events (filter: {videogameId: 1386}) {
        name
        id
      }
    }
  }
}
"""

get_all_events_no_location="""
query get_events_no_loc($name: String, $cCode: String, $perPage: Int) {
  tournaments(
    query: {perPage: $perPage, filter: {name: $name, countryCode: $cCode}}
  ) {
    nodes {
      name
      countryCode
      postalCode
      events (filter: {videogameId: 1386}) {
        name
        id
      }
    }
  }
}
"""

# Requête donnant les standings et les seedings de toutes les phases de l'évènement dont on passe l'id.
get_standings_seed="""
query get_standings_seed($eventId: ID!, $perPage: Int, $page: Int) {
  event(id: $eventId) {
    id
    name
    standings(query: {perPage: $perPage}) {
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
      seeds(query: {perPage: $perPage, page: $page}, eventId: $eventId) {
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