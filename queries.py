# Une requête qui doit renvoyer les id des tournois qu'on veut analyser
get_all_events_location="""
query get_events_loc($name: String, $cCode: String, $distance: String, $city: String, $perPage: Int, $page: Int, $a_venir: Boolean, $gameId: [ID]) {
  tournaments(
    query: {perPage: $perPage, page: $page, filter: {name: $name, countryCode: $cCode, upcoming: $a_venir, location: {distanceFrom: $city, distance: $distance}}}
  ) {
    nodes {
      name
      countryCode
      postalCode
      events (filter: {videogameId: $gameId}) {
        name
        id
      }
    }
  }
}
"""

get_all_events_no_location="""
query get_events_no_loc($name: String, $cCode: String, $perPage: Int, $page: Int, $a_venir: Boolean, $gameId: [ID]) {
  tournaments(
    query: {perPage: $perPage, page: $page filter: {name: $name, countryCode: $cCode, upcoming: $a_venir}}
  ) {
    nodes {
      name
      countryCode
      postalCode
      events (filter: {videogameId: $gameId}) {
        name
        id
      }
    }
  }
}
"""

# Requête donnant les standings et les seedings de toutes les phases de l'évènement dont on passe l'id.
get_event_standings="""
query get_standings($eventId: ID!, $perPage: Int) {
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
  }
}
"""

get_event_seeding="""
query get_seeding($eventId: ID!, $perPage: Int) {
  event(id: $eventId) {
    id
    name
    phases {
      id
      seeds(query: {perPage: $perPage}, eventId: $eventId) {
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