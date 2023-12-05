# Une requête qui doit renvoyer les id des tournois qu'on veut analyser
get_all_events_location="""
query get_events($name: String, $cCode: String, $distance: String, $city: String, $perPage: Int) {
  tournaments(
    query: {perPage: $perPage, filter: {name: $name, countryCode: $cCode, location: {distanceFrom: $city, distance: $distance}}}
  ) {
    nodes {
      name
      countryCode
      postalCode
      events {
        name
        id
      }
    }
  }
}
"""

get_all_events_no_location:"""
query get_events($name: String, $cCode: String, $perPage: Int) {
  tournaments(
    query: {perPage: $perPage, filter: {name: $name, countryCode: $cCode}}
  ) {
    nodes {
      name
      countryCode
      postalCode
      events {
        name
        id
      }
    }
  }
}
"""

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